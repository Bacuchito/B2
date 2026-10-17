# -*- coding: utf-8 -*-
"""Prueba de regresion del extractor de PDF (tools/pdf2md.py).

El fallo que la motivó: se ignoraba el estado grafico q/Q, así que la fuente
elegida dentro de un bloque q...Q se filtraba a los textos siguientes. En las
paginas con capa de texto mezclada eso convertia texto ASCII en codigos de dos
bytes y se perdia silenciosamente (p. ej. «nehmen, da keine neuen
Mitarbeitenden» en la tabla de Forumsbeitrag).

Uso: python tools/test_pdf2md.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdf2md as p  # noqa: E402


def fuente(base, two_byte=False, tounicode=None):
    f = p.Font()
    f.base = base
    f.two_byte = two_byte
    f.tounicode = tounicode
    f.widths = {c: 500 for c in range(256)}
    return f


def extrae(flujo, fonts):
    runs = []
    p.extract_runs(flujo, fonts, runs)
    return [(r.font, r.text) for r in runs]


fallos = []


def check(nombre, cond, detalle=''):
    print('  {} {} {}'.format('OK  ' if cond else 'FALLO', nombre, detalle))
    if not cond:
        fallos.append(nombre)


# 1. La fuente de dentro de q...Q no debe salir del bloque.
fonts = {'F1': fuente('uno'), 'F2': fuente('dos')}
flujo = (b'BT /F1 10 Tf (hola) Tj ET\n'
         b'q BT /F2 10 Tf (adios) Tj ET Q\n'
         b'BT (vuelta) Tj ET\n')
check('q/Q restaura la fuente anterior',
      extrae(flujo, fonts) == [('uno', 'hola'), ('dos', 'adios'), ('uno', 'vuelta')],
      str(extrae(flujo, fonts)))

# 2. Los q/Q anidados tambien se restauran en orden.
flujo = (b'BT /F1 10 Tf (a) Tj ET\n'
         b'q BT /F2 10 Tf (b) Tj ET\n'
         b'q BT (c) Tj ET Q\n'
         b'BT (d) Tj ET Q\n'
         b'BT (e) Tj ET\n')
check('los q/Q anidados vuelven en orden',
      extrae(flujo, fonts) == [('uno', 'a'), ('dos', 'b'), ('dos', 'c'),
                               ('dos', 'd'), ('uno', 'e')],
      str(extrae(flujo, fonts)))

# 3. Un texto ASCII con fuente de dos bytes sigue perdiendose: es lo esperado,
#    pero no debe arrastrar al texto con la fuente correcta.
fonts3 = {'F1': fuente('uno'), 'F2': fuente('dos', two_byte=True, tounicode={0x41: 'A'})}
flujo = b'BT /F1 10 Tf (bien) Tj ET\nq BT /F2 10 Tf <0041> Tj ET Q\nBT (sigue) Tj ET\n'
check('la fuente de dos bytes no contamina al texto siguiente',
      extrae(flujo, fonts3) == [('uno', 'bien'), ('dos', 'A'), ('uno', 'sigue')],
      str(extrae(flujo, fonts3)))

print('\n{}/{} comprobaciones superadas'.format(3 - len(fallos), 3))
sys.exit(1 if fallos else 0)
