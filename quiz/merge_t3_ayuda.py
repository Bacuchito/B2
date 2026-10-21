import json
import sys

salida = {}
for ruta in sys.argv[1:-1]:
    datos = json.load(open(ruta, encoding="utf-8"))
    repetidos = set(datos) & set(salida)
    if repetidos:
        raise SystemExit(f"situaciones repetidas en {ruta}: {sorted(repetidos)}")
    salida.update(datos)
json.dump(salida, open(sys.argv[-1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(salida)} situaciones de ayuda -> {sys.argv[-1]}")
