import json, re, sys

p = r"C:\Users\sergi\Documents\Code\B2\quiz\data\ls_c.json"
d = json.load(open(p, encoding="utf-8"))
src = open(r"C:\Users\sergi\Documents\Code\B2\quiz\src\ls_c.md", encoding="utf-8").read()

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

print("block:", d["block"], "| section:", d["section"], "| variantes:", len(d["variants"]))
ok = True
for v in d["variants"]:
    assert v["kind"] == "text", v["id"]
    np_ = norm(v["passage"])
    print("\n%s | page %s | %s | topic=%s | items=%d" % (v["id"], v["page"], v["label"], v.get("topic"), len(v["items"])))
    for it in v["items"]:
        keys = [o["key"] for o in it["options"]]
        assert it["answer"] in keys, (v["id"], it["n"], it["answer"], keys)
        q = norm(it["quote"])
        inside = q in np_
        prompt_inside = norm(it["prompt"]) in np_
        print("  n=%s ans=%s conf=%s keys=%s quote_in_passage=%s prompt_literal_in_md=%s" % (
            it["n"], it["answer"], it["confidence"], keys, inside, norm(it["prompt"]) in norm(src)))
        if not inside:
            ok = False
            print("    !! QUOTE NOT IN PASSAGE:", q[:100])
    for bad in ["Computerproblem", "kümmer", "Schreiben Sie eine E-Mail", "Teamleiter", "Nummer 21"]:
        if bad in v["passage"]:
            ok = False
            print("    !! passage contiene material del correo interno:", bad)
print("\nQUOTES OK" if ok else "\nPROBLEMAS")
