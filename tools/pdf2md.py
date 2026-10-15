#!/usr/bin/env python3
"""pdf2md.py - Conversor PDF -> Markdown en Python puro (solo stdlib).

Sustituto local de MarkItDown para este caso: extrae la capa de texto,
reconstruye lineas usando las coordenadas del text matrix y emite Markdown
con marcadores de pagina.

Uso:
    python pdf2md.py entrada.pdf salida.md
"""
from __future__ import annotations

import bisect
import json
import os
import re
import statistics
import sys
import zlib

WS = b"\x00\t\n\x0c\r "


# --------------------------------------------------------------------------
# Lexer / parser de objetos PDF
# --------------------------------------------------------------------------

class Name(bytes):
    """Nombre PDF, p.ej. /F1  ->  Name(b'F1')."""
    __slots__ = ()


class Keyword(bytes):
    """Operador o palabra clave suelta, p.ej. 'BT' o 'true'."""
    __slots__ = ()


class PdfString:
    __slots__ = ("raw",)

    def __init__(self, raw: bytes):
        self.raw = raw

    def __repr__(self) -> str:
        return f"Str({self.raw[:40]!r})"


def _is_ref(tok) -> bool:
    return (isinstance(tok, list) and len(tok) == 3
            and isinstance(tok[0], int) and isinstance(tok[1], int)
            and isinstance(tok[2], Keyword) and tok[2] == b"R")


class Lexer:
    def __init__(self, data: bytes, pos: int = 0):
        self.d = data
        self.i = pos
        self.n = len(data)

    def skip_ws(self) -> None:
        d, i, n = self.d, self.i, self.n
        while i < n:
            c = d[i]
            if c in WS:
                i += 1
            elif c == 0x25:  # '%' comentario
                while i < n and d[i] not in b"\r\n":
                    i += 1
            else:
                break
        self.i = i

    # ---------- tokens de bajo nivel ----------
    def token(self):
        self.skip_ws()
        d, i, n = self.d, self.i, self.n
        if i >= n:
            return None
        c = d[i]

        if c == 0x2F:  # '/'
            i += 1
            start = i
            while i < n and d[i] not in WS and d[i] not in b"()<>[]{}/%":
                i += 1
            self.i = i
            return Name(d[start:i])

        if c == 0x28:  # '('
            return self._read_literal_string()

        if c == 0x3C:  # '<'
            if i + 1 < n and d[i + 1] == 0x3C:
                self.i = i + 2
                return Keyword(b"<<")
            return self._read_hex_string()

        if c == 0x3E:  # '>'
            if i + 1 < n and d[i + 1] == 0x3E:
                self.i = i + 2
                return Keyword(b">>")
            self.i = i + 1
            return Keyword(b">")

        if c == 0x5B:  # '['
            self.i = i + 1
            return Keyword(b"[")
        if c == 0x5D:  # ']'
            self.i = i + 1
            return Keyword(b"]")
        if c in b"{}":
            self.i = i + 1
            return Keyword(bytes([c]))

        start = i
        while i < n and d[i] not in WS and d[i] not in b"()<>[]{}/%":
            i += 1
        if i == start:
            self.i = start + 1
            return None
        self.i = i
        raw = d[start:i]
        try:
            if b"." in raw or b"e" in raw or b"E" in raw:
                return float(raw)
            return int(raw)
        except ValueError:
            return Keyword(raw)

    def _read_literal_string(self) -> PdfString:
        d, i, n = self.d, self.i, self.n
        i += 1  # '('
        depth = 1
        out = bytearray()
        while i < n:
            c = d[i]
            if c == 0x5C:  # backslash
                i += 1
                if i >= n:
                    break
                e = d[i]
                if e in b"nrtbf":
                    out.append({0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12}[e])
                    i += 1
                elif e in b"()\\":
                    out.append(e)
                    i += 1
                elif 0x30 <= e <= 0x37:
                    oct_digits = bytearray()
                    while i < n and len(oct_digits) < 3 and 0x30 <= d[i] <= 0x37:
                        oct_digits.append(d[i])
                        i += 1
                    out.append(int(oct_digits, 8) & 0xFF)
                elif e in b"\r\n":
                    if e == 13 and i + 1 < n and d[i + 1] == 10:
                        i += 1
                    i += 1
                else:
                    out.append(e)
                    i += 1
            elif c == 0x28:
                depth += 1
                out.append(c)
                i += 1
            elif c == 0x29:
                depth -= 1
                i += 1
                if depth == 0:
                    break
                out.append(c)
            else:
                out.append(c)
                i += 1
        self.i = i
        return PdfString(bytes(out))

    def _read_hex_string(self) -> PdfString:
        d, i, n = self.d, self.i, self.n
        i += 1  # '<'
        digits = bytearray()
        while i < n and d[i] != 0x3E:
            c = d[i]
            if c not in WS:
                digits.append(c)
            i += 1
        i += 1
        if len(digits) % 2:
            digits.append(0x30)
        try:
            raw = bytes.fromhex(digits.decode("ascii"))
        except (ValueError, UnicodeDecodeError):
            raw = b""
        self.i = i
        return PdfString(raw)

    # ---------- parser de alto nivel ----------
    def parse_object(self):
        tok = self.token()
        if tok is None:
            return None

        if isinstance(tok, Keyword) and tok == b"[":
            arr = []
            guard = 0
            while guard < 100000:
                guard += 1
                save = self.i
                probe = self.token()
                if probe is None:
                    break
                if isinstance(probe, Keyword) and probe in (b"]", b">>", b"<<"):
                    if probe == b"]":
                        break
                    self.i = save
                    v = self.parse_object()
                    if v is None:
                        break
                    arr.append(v)
                    continue
                self.i = save
                v = self.parse_object()
                if v is None:
                    break
                arr.append(v)
            return arr

        if isinstance(tok, Keyword) and tok == b"<<":
            return self._read_dict()

        if isinstance(tok, Keyword) and tok in (b"]", b">>"):
            return tok

        if isinstance(tok, int):
            # posible referencia indirecta 'N G R'
            save = self.i
            t2 = self.token()
            if isinstance(t2, int):
                save3 = self.i
                t3 = self.token()
                if isinstance(t3, Keyword) and t3 == b"R":
                    return [tok, t2, t3]
                self.i = save3
            self.i = save
            return tok

        return tok

    def _read_dict(self) -> dict:
        out = {}
        while True:
            save = self.i
            k = self.token()
            if k is None:
                break
            if isinstance(k, Keyword) and k == b">>":
                break
            if not isinstance(k, Name):
                self.i = save
                if self.token() is None:
                    break
                continue
            v = self.parse_object()
            if v is None:
                break
            if isinstance(v, Keyword) and v == b">>":
                break
            out[k.decode("latin-1")] = v
        return out


def parse_full(data: bytes):
    return Lexer(data).parse_object()


# --------------------------------------------------------------------------
# Documento PDF
# --------------------------------------------------------------------------

STREAM_RE = re.compile(rb"\bstream\b")


class PDF:
    def __init__(self, path: str):
        self.path = path
        self.data = open(path, "rb").read()
        self.raw: dict[int, bytes] = {}
        self._parsed: dict[int, object] = {}
        self._stream_cache: dict[int, bytes | None] = {}
        self._resolve_stream_meta()
        self._build_objects()

    # ---- localizacion de los bytes de stream ----
    def _resolve_stream_meta(self) -> None:
        self.regions = []
        for m in STREAM_RE.finditer(self.data):
            e = self.data.find(b"endstream", m.end())
            if e != -1:
                self.regions.append((m.start(), e))
        self.regions.sort()
        self._region_starts = [r[0] for r in self.regions]

    def _in_stream(self, pos: int) -> bool:
        idx = bisect.bisect_right(self._region_starts, pos) - 1
        return idx >= 0 and self.regions[idx][0] < pos < self.regions[idx][1]

    def _build_objects(self) -> None:
        data = self.data
        obj_re = re.compile(rb"(?m)(?<![0-9])(\d+)\s+(\d+)\s+obj\b")
        for m in obj_re.finditer(data):
            if self._in_stream(m.start()):
                continue
            k = m.end()
            while k < len(data) and data[k] in WS:
                k += 1
            if k >= len(data) or data[k] not in b"<[/(+-0123456789":
                continue
            end = data.find(b"endobj", k)
            if end == -1:
                end = len(data)
            self.raw[int(m.group(1))] = data[k:end]
        self._extract_objstms()

    def _extract_objstms(self) -> None:
        for num, body in list(self.raw.items()):
            if b"/ObjStm" not in body:
                continue
            try:
                dec = self.decode_stream(body)
            except Exception:
                continue
            if not dec:
                continue
            mn = re.search(rb"/N\s+(\d+)", body)
            mf = re.search(rb"/First\s+(\d+)", body)
            if not (mn and mf):
                continue
            count, first = int(mn.group(1)), int(mf.group(1))
            nums = dec[:first].split()
            if len(nums) < 2 * count:
                count = len(nums) // 2
            offs = []
            for i in range(count):
                try:
                    offs.append((int(nums[2 * i]), int(nums[2 * i + 1])))
                except (ValueError, IndexError):
                    break
            if not offs:
                continue
            bounds = [o for _, o in offs] + [len(dec)]
            for i, (objnum, off) in enumerate(offs):
                if objnum in self.raw:
                    continue
                start = first + off
                stop = first + bounds[i + 1]
                self.raw[objnum] = dec[start:stop].strip()

    # ---- acceso ----
    def decode_stream(self, body: bytes) -> bytes | None:
        i = body.find(b"stream")
        if i == -1:
            return None
        j = body.find(b"endstream", i)
        raw = body[i + 6: j if j != -1 else len(body)]
        if raw.startswith(b"\r\n"):
            raw = raw[2:]
        elif raw[:1] in (b"\n", b"\r"):
            raw = raw[1:]
        if raw.endswith(b"\r\n"):
            raw = raw[:-2]
        elif raw[-1:] in (b"\n", b"\r"):
            raw = raw[:-1]
        head = body[:i]
        if b"/FlateDecode" in head:
            try:
                return zlib.decompress(raw)
            except zlib.error:
                try:
                    return zlib.decompressobj().decompress(raw)
                except zlib.error:
                    return None
        return raw

    def obj(self, num: int):
        if num in self._parsed:
            return self._parsed[num]
        body = self.raw.get(num)
        val = parse_full(body) if body is not None else None
        self._parsed[num] = val
        return val

    def stream_of(self, num: int) -> bytes | None:
        if num in self._stream_cache:
            return self._stream_cache[num]
        body = self.raw.get(num)
        out = self.decode_stream(body) if body is not None else None
        self._stream_cache[num] = out
        return out

    def deref(self, tok):
        if _is_ref(tok):
            return self.obj(tok[0])
        return tok

    @staticmethod
    def ref_num(tok) -> int | None:
        return tok[0] if _is_ref(tok) else None

    # ---- arbol de paginas ----
    def catalog_num(self) -> int | None:
        for num in sorted(self.raw):
            v = self.obj(num)
            if isinstance(v, dict) and v.get("Type") == Name(b"Catalog"):
                return num
        return None

    def pages(self) -> list[int]:
        cat_num = self.catalog_num()
        out: list[int] = []
        seen: set[int] = set()

        def walk(num: int | None):
            if num is None or num in seen:
                return
            seen.add(num)
            d = self.obj(num)
            if not isinstance(d, dict):
                return
            if d.get("Type") == Name(b"Page"):
                out.append(num)
                return
            kids = d.get("Kids")
            if _is_ref(kids):
                kids = self.deref(kids)
            if isinstance(kids, list):
                for k in kids:
                    walk(self.ref_num(k))

        if cat_num is not None:
            cat = self.obj(cat_num)
            walk(self.ref_num(cat.get("Pages")))

        if not out:
            out = [n for n in sorted(self.raw)
                   if isinstance(self.obj(n), dict)
                   and self.obj(n).get("Type") == Name(b"Page")]
        return out

    def inherited(self, page_num: int, key: str):
        cur = page_num
        for _ in range(64):
            d = self.obj(cur)
            if not isinstance(d, dict):
                return None
            if key in d:
                return d[key]
            parent = self.ref_num(d.get("Parent"))
            if parent is None:
                return None
            cur = parent
        return None


# --------------------------------------------------------------------------
# Fuentes
# --------------------------------------------------------------------------

def _hex_to_text(h: str) -> str:
    try:
        b = bytes.fromhex(h)
    except ValueError:
        return ""
    if len(b) % 2 == 0:
        try:
            return b.decode("utf-16-be")
        except UnicodeDecodeError:
            pass
    return b.decode("latin-1", "replace")


def parse_tounicode(cmap: bytes) -> dict[int, str]:
    m: dict[int, str] = {}
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", cmap, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            try:
                m[int(src, 16)] = _hex_to_text(dst.decode("ascii"))
            except ValueError:
                pass
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", cmap, re.S):
        consumed = []
        for mm in re.finditer(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]", blk, re.S):
            consumed.append(mm.span())
            try:
                lo_i = int(mm.group(1), 16)
            except ValueError:
                continue
            for idx, item in enumerate(re.findall(rb"<([0-9A-Fa-f]+)>", mm.group(3))):
                m[lo_i + idx] = _hex_to_text(item.decode("ascii"))
        for mm in re.finditer(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            if any(a <= mm.start() < b for a, b in consumed):
                continue
            try:
                lo_i = int(mm.group(1), 16)
                hi_i = int(mm.group(2), 16)
                base = int(mm.group(3), 16)
            except ValueError:
                continue
            for k in range(lo_i, min(hi_i, lo_i + 65535) + 1):
                try:
                    m[k] = chr(base + (k - lo_i))
                except (ValueError, OverflowError):
                    break
    return m


class Font:
    __slots__ = ("base", "bold", "two_byte", "tounicode", "differences",
                 "widths", "default_width")

    def __init__(self):
        self.base = ""
        self.bold = False
        self.two_byte = False
        self.tounicode: dict[int, str] | None = None
        self.differences: dict[int, str] = {}
        self.widths: dict[int, float] = {}
        self.default_width = 500.0


def _glyph_name_to_char(gname: str) -> str:
    if not gname:
        return ""
    if len(gname) == 1:
        return gname
    m = re.fullmatch(r"uni([0-9A-Fa-f]{4})", gname)
    if m:
        return chr(int(m.group(1), 16))
    return ""


def _read_w_array(pdf: PDF, w, font: Font) -> None:
    w = pdf.deref(w)
    if not isinstance(w, list):
        return
    i = 0
    while i < len(w):
        first = w[i]
        if not isinstance(first, (int, float)):
            i += 1
            continue
        if i + 1 < len(w) and isinstance(w[i + 1], list):
            for j, v in enumerate(w[i + 1]):
                if isinstance(v, (int, float)):
                    font.widths[int(first) + j] = float(v)
            i += 2
        elif i + 2 < len(w) and isinstance(w[i + 1], (int, float)) and isinstance(w[i + 2], (int, float)):
            last, val = int(w[i + 1]), float(w[i + 2])
            for c in range(int(first), min(last, int(first) + 65535) + 1):
                font.widths[c] = val
            i += 3
        else:
            i += 1


def build_font(pdf: PDF, num: int) -> Font:
    f = Font()
    d = pdf.obj(num)
    if not isinstance(d, dict):
        return f
    subtype = d.get("Subtype")
    base = d.get("BaseFont")
    if isinstance(base, Name):
        full = base.decode("latin-1")
        f.base = full.split("+", 1)[-1]
        f.bold = "Bold" in full or "Black" in full or "Semibold" in full

    fd = pdf.deref(d.get("FontDescriptor"))
    if isinstance(fd, dict):
        flags = fd.get("Flags")
        if isinstance(flags, (int, float)) and (int(flags) & 0x40000):
            f.bold = True
        if not f.base:
            fn = fd.get("FontName")
            if isinstance(fn, Name):
                f.base = fn.decode("latin-1").split("+", 1)[-1]

    tu_num = pdf.ref_num(d.get("ToUnicode"))
    if tu_num is not None:
        blob = pdf.stream_of(tu_num)
        if blob:
            f.tounicode = parse_tounicode(blob)

    if subtype == Name(b"Type0"):
        f.two_byte = True
        desc = pdf.deref(d.get("DescendantFonts"))
        cid = None
        if isinstance(desc, list) and desc:
            cid = pdf.deref(desc[0])
        if isinstance(cid, dict):
            dw = cid.get("DW")
            f.default_width = float(dw) if isinstance(dw, (int, float)) else 1000.0
            _read_w_array(pdf, cid.get("W"), f)
            if not f.base:
                b2 = cid.get("BaseFont")
                if isinstance(b2, Name):
                    f.base = b2.decode("latin-1").split("+", 1)[-1]
    else:
        fc = d.get("FirstChar")
        first_char = int(fc) if isinstance(fc, (int, float)) else 0
        w = pdf.deref(d.get("Widths"))
        if isinstance(w, list):
            for i, v in enumerate(w):
                if isinstance(v, (int, float)):
                    f.widths[first_char + i] = float(v)
        enc = pdf.deref(d.get("Encoding"))
        if isinstance(enc, dict):
            diff = pdf.deref(enc.get("Differences"))
            if isinstance(diff, list):
                cur = 0
                for item in diff:
                    if isinstance(item, (int, float)):
                        cur = int(item)
                    elif isinstance(item, Name):
                        ch = _glyph_name_to_char(item.decode("latin-1"))
                        if ch:
                            f.differences[cur] = ch
                        cur += 1
    return f


def code_width(f: Font, code: int) -> float:
    if code in f.widths:
        return f.widths[code]
    return f.default_width if f.two_byte else 500.0


def decode_string(f: Font, raw: bytes) -> tuple[str, float]:
    """Devuelve (texto, ancho_total_en_milesimas_de_em)."""
    out = []
    width = 0.0
    if f.two_byte:
        for i in range(0, len(raw) - 1, 2):
            code = (raw[i] << 8) | raw[i + 1]
            if f.tounicode is not None:
                out.append(f.tounicode.get(code, ""))
            else:
                try:
                    out.append(bytes([raw[i], raw[i + 1]]).decode("utf-16-be"))
                except UnicodeDecodeError:
                    out.append("")
            width += code_width(f, code)
    else:
        for b in raw:
            if b in f.differences:
                out.append(f.differences[b])
            elif f.tounicode is not None and b in f.tounicode:
                out.append(f.tounicode[b])
            else:
                out.append(bytes([b]).decode("cp1252", "replace"))
            width += code_width(f, b)
    return "".join(out), width


# --------------------------------------------------------------------------
# Extraccion de texto
# --------------------------------------------------------------------------

class Run:
    __slots__ = ("x", "x1", "y", "text", "size", "font", "bold")

    def __init__(self, x, x1, y, text, size, font, bold):
        self.x = x        # posicion inicial (text matrix e)
        self.x1 = x1      # posicion final real tras el avance
        self.y = y
        self.text = text
        self.size = size
        self.font = font
        self.bold = bold


def extract_runs(data: bytes, fonts: dict[str, Font], runs: list[Run]) -> None:
    lx = Lexer(data)
    stack: list = []
    cur_font = Font()
    size = 10.0
    tm = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    tlm = list(tm)
    leading = 0.0
    char_sp = 0.0
    word_sp = 0.0
    hscale = 100.0

    def advance(dx: float) -> None:
        tm[4] += dx * tm[0]
        tm[5] += dx * tm[1]

    def next_line() -> None:
        nonlocal tm, tlm
        tlm = [tlm[0], tlm[1], tlm[2], tlm[3],
               tlm[4] - leading * tlm[2], tlm[5] - leading * tlm[3]]
        tm = list(tlm)

    while True:
        tok = lx.parse_object()
        if tok is None:
            break
        if not isinstance(tok, Keyword):
            stack.append(tok)
            if len(stack) > 32:
                del stack[:-16]
            continue

        op = tok
        try:
            if op == b"BT":
                tm = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
                tlm = list(tm)
            elif op == b"Tm" and len(stack) >= 6:
                tm = [float(v) for v in stack[-6:]]
                tlm = list(tm)
            elif op in (b"Td", b"TD") and len(stack) >= 2:
                if op == b"TD":
                    leading = -float(stack[-1])
                tx, ty = float(stack[-2]), float(stack[-1])
                tlm = [tlm[0], tlm[1], tlm[2], tlm[3],
                       tlm[0] * tx + tlm[2] * ty + tlm[4],
                       tlm[1] * tx + tlm[3] * ty + tlm[5]]
                tm = list(tlm)
            elif op == b"T*":
                next_line()
            elif op == b"TL" and stack:
                leading = float(stack[-1])
            elif op == b"Tc" and stack:
                char_sp = float(stack[-1])
            elif op == b"Tw" and stack:
                word_sp = float(stack[-1])
            elif op == b"Tz" and stack:
                hscale = float(stack[-1])
            elif op == b"Tf" and len(stack) >= 2:
                fname = stack[-2]
                if isinstance(fname, Name):
                    cur_font = fonts.get(fname.decode("latin-1"), Font())
                size = float(stack[-1])
            elif op in (b"Tj", b"'", b'"'):
                if op in (b"'", b'"'):
                    next_line()
                    if op == b'"' and len(stack) >= 3:
                        word_sp = float(stack[-3])
                        char_sp = float(stack[-2])
                        if len(stack) >= 1:
                            s = stack[-1]
                s = stack[-1] if stack else None
                if isinstance(s, PdfString):
                    _emit(cur_font, s.raw, size, tm, runs, char_sp, word_sp, hscale, advance)
            elif op == b"TJ":
                arr = stack[-1] if stack else None
                if isinstance(arr, list):
                    for el in arr:
                        if isinstance(el, PdfString):
                            _emit(cur_font, el.raw, size, tm, runs, char_sp, word_sp, hscale, advance)
                        elif isinstance(el, (int, float)):
                            advance(-float(el) / 1000.0 * size * (hscale / 100.0))
        except (IndexError, ValueError, TypeError):
            pass

        stack = []


def _emit(f: Font, raw: bytes, size: float, tm, runs, char_sp, word_sp, hscale, advance) -> None:
    text, width = decode_string(f, raw)
    x0, y0 = tm[4], tm[5]
    adv = width / 1000.0 * size * (hscale / 100.0)
    adv += char_sp * len(raw) * (hscale / 100.0)
    if word_sp:
        adv += word_sp * raw.count(0x20) * (hscale / 100.0)
    if text.strip():
        runs.append(Run(x0, x0 + adv, y0, text, size, f.base, f.bold))
    advance(adv)


def page_runs(pdf: PDF, page_num: int, font_cache: dict) -> list[Run]:
    page = pdf.obj(page_num)
    if not isinstance(page, dict):
        return []

    res = pdf.deref(page.get("Resources"))
    if res is None:
        res = pdf.deref(pdf.inherited(page_num, "Resources"))
    if not isinstance(res, dict):
        res = {}

    fonts: dict[str, Font] = {}
    fonts_raw = pdf.deref(res.get("Font"))
    if isinstance(fonts_raw, dict):
        for k, v in fonts_raw.items():
            rn = pdf.ref_num(v)
            if rn is None:
                continue
            f = font_cache.get(rn)
            if f is None:
                f = build_font(pdf, rn)
                font_cache[rn] = f
            fonts[k] = f

    contents = page.get("Contents")
    if isinstance(contents, list) and not _is_ref(contents):
        parts = [pdf.ref_num(c) for c in contents]
    else:
        parts = [pdf.ref_num(contents)]

    runs: list[Run] = []
    for part in parts:
        if part is None:
            continue
        data = pdf.stream_of(part)
        if data:
            extract_runs(data, fonts, runs)
    return runs


# --------------------------------------------------------------------------
# Reconstruccion de lineas
# --------------------------------------------------------------------------

def build_lines(runs: list[Run]):
    if not runs:
        return []
    heights = [r.size for r in runs if r.size > 0]
    med = statistics.median(heights) if heights else 10.0
    tol = max(1.6, med * 0.45)

    ordered = sorted(runs, key=lambda r: (-r.y, r.x))
    groups: list[list[Run]] = []
    for r in ordered:
        if groups and abs(groups[-1][0].y - r.y) <= tol:
            groups[-1].append(r)
        else:
            groups.append([r])

    out = []
    for grp in groups:
        grp.sort(key=lambda r: r.x)
        parts = []
        prev_end = None
        for r in grp:
            if prev_end is not None:
                gap = r.x - prev_end
                # un espacio tipografico real mide >= ~0.18 em;
                # los huecos de kerning se quedan por debajo.
                if gap > max(1.2, r.size * 0.18):
                    parts.append(" ")
            parts.append(r.text)
            prev_end = max(r.x1, r.x)
        text = re.sub(r"[ \t]+", " ", "".join(parts)).strip()
        if not text:
            continue
        out.append({
            "y": grp[0].y,
            "x": grp[0].x,
            "text": text,
            "size": max(r.size for r in grp),
            "bold": any(r.bold for r in grp),
        })
    out.sort(key=lambda d: -d["y"])
    return out


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    pdf = PDF(src)
    page_nums = pdf.pages()
    print(f"[i] paginas en el arbol: {len(page_nums)}", file=sys.stderr)
    if not page_nums:
        print("[!] no se encontro ninguna pagina", file=sys.stderr)
        return

    font_cache: dict = {}
    doc = []
    index = []
    all_sizes = []

    for i, pnum in enumerate(page_nums, 1):
        lines = build_lines(page_runs(pdf, pnum, font_cache))
        index.append({"page": i, "obj": pnum, "lines": len(lines),
                      "chars": sum(len(l["text"]) for l in lines)})
        doc.append((i, lines))
        all_sizes.extend(l["size"] for l in lines if l["size"] > 0)

    body = statistics.median(all_sizes) if all_sizes else 11.0
    total_chars = sum(e["chars"] for e in index)

    md = [f"# {os.path.basename(src)}\n"]
    md.append(f"> Convertido con pdf2md.py (Python puro, sin dependencias). "
              f"{len(page_nums)} paginas, {total_chars:,} caracteres de texto.\n")
    md.append(f"> Fuente dominante: {body:.1f} pt.\n")

    for pageno, lines in doc:
        md.append(f"\n<!-- page: {pageno} -->\n")
        for ln in lines:
            t = ln["text"]
            if len(t) < 120 and ln["size"] >= body * 1.35:
                md.append(f"\n### {t}\n")
            elif ln["bold"] and 2 < len(t) < 90 and ln["size"] >= body * 1.02:
                md.append(f"\n**{t}**\n")
            else:
                md.append(t + "\n")

    text = "".join(md)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(text)

    idx_path = os.path.splitext(dst)[0] + ".index.json"
    with open(idx_path, "w", encoding="utf-8") as fh:
        json.dump({"source": src, "body_size": body, "pages": index},
                  fh, ensure_ascii=False, indent=1)

    chars = [e["chars"] for e in index]
    print(f"[ok] {dst} ({len(text):,} chars, {os.path.getsize(dst):,} bytes)")
    print(f"[ok] {idx_path}")
    print(f"[i] chars/pagina: min={min(chars)} max={max(chars)} "
          f"mediana={statistics.median(chars):.0f} total={total_chars:,}")
    empty = [e["page"] for e in index if e["chars"] < 20]
    print(f"[i] paginas casi vacias ({len(empty)}): {empty[:40]}")


if __name__ == "__main__":
    main()
