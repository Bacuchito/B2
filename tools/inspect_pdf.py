"""Inspecciona la estructura interna del PDF para planear el extractor.

Solo stdlib. Objetivo: saber cuantos objetos hay, cuales son fuentes,
que subtipos (Type0/Type1/TrueType), si tienen ToUnicode, y cuantos
content streams hay que decodificar.
"""
import re
import sys
import zlib
import collections
import os

PDF = sys.argv[1]


def find_objects(data: bytes) -> dict:
    """Extrae objetos de nivel superior por fuerza bruta: 'N G obj ... endobj'."""
    objs = {}
    for m in re.finditer(rb"(?m)^\s*(\d+)\s+(\d+)\s+obj\b", data):
        num = int(m.group(1))
        start = m.end()
        end = data.find(b"endobj", start)
        if end == -1:
            end = len(data)
        objs[num] = data[start:end]
    return objs


def decompress_stream(body: bytes) -> bytes | None:
    """Localiza 'stream...endstream' y descomprime si es FlateDecode."""
    i = body.find(b"stream")
    if i == -1:
        return None
    j = body.find(b"endstream", i)
    if j == -1:
        return None
    raw = body[i + 6:j]
    # salta CRLF o LF inicial
    if raw.startswith(b"\r\n"):
        raw = raw[2:]
    elif raw.startswith(b"\n"):
        raw = raw[1:]
    if raw.endswith(b"\r\n"):
        raw = raw[:-2]
    elif raw.endswith(b"\n"):
        raw = raw[:-1]
    try:
        return zlib.decompress(raw)
    except zlib.error:
        try:
            return zlib.decompressobj().decompress(raw)
        except zlib.error:
            return None


def main() -> None:
    data = open(PDF, "rb").read()
    print(f"file bytes: {len(data):,}")

    print("\n--- header / xref style ---")
    print("header:", data[:16])
    print("has /XRef (cross-ref stream):", b"/XRef" in data)
    print("has trailer keyword:", data.rfind(b"trailer") != -1)
    print("startxref count:", len(re.findall(rb"startxref", data)))
    print("ObjStm count:", len(re.findall(rb"/ObjStm", data)))

    objs = find_objects(data)
    print(f"\ntop-level objects found by scan: {len(objs)}")
    if objs:
        nums = sorted(objs)
        print("object number range:", nums[0], "-", nums[-1])

    # clasifica por /Type
    types = collections.Counter()
    for num, body in objs.items():
        m = re.search(rb"/Type\s*/(\w+)", body)
        types[m.group(1).decode() if m else "<none>"] += 1
    print("\nobject /Type histogram:", dict(types.most_common()))

    # fuentes
    fonts = {n: b for n, b in objs.items() if re.search(rb"/Type\s*/Font", b)}
    print(f"\nfont objects (top-level): {len(fonts)}")
    sub = collections.Counter()
    for n, b in fonts.items():
        m = re.search(rb"/Subtype\s*/(\w+)", b)
        sub[m.group(1).decode() if m else "?"] += 1
    print("font /Subtype:", dict(sub))

    with_tounicode = sum(1 for b in fonts.values() if b"/ToUnicode" in b)
    print(f"fonts with /ToUnicode: {with_tounicode}/{len(fonts)}")
    print("fonts with /Encoding:", sum(1 for b in fonts.values() if b"/Encoding" in b))
    print("fonts with /Differences:", sum(1 for b in fonts.values() if b"/Differences" in b))

    print("\n--- sample font objects ---")
    for n in list(fonts)[:6]:
        print(f"\nobj {n}: {fonts[n][:400]!r}")

    # content streams
    streams = [n for n, b in objs.items() if b"stream" in b]
    print(f"\nobjects with streams: {len(streams)}")
    ok = 0
    for n in streams:
        if decompress_stream(objs[n]) is not None:
            ok += 1
    print(f"successfully Flate-decompressed: {ok}")

    print("\n--- sample content stream (decompressed) ---")
    for n in streams:
        d = decompress_stream(objs[n])
        if d and (b"BT" in d or b"Tj" in d or b"TJ" in d):
            print(f"obj {n}, {len(d)} bytes:")
            print(d[:1200])
            break
    else:
        print("no obvious text content stream among top-level streams")


if __name__ == "__main__":
    main()
