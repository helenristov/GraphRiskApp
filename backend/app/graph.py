GRAPH_DB = {"nodes": [], "edges": []}

def merge_into_graph(extracted):
    for tp in extracted["third_parties"]:
        if not any(n["id"] == tp["id"] for n in GRAPH_DB["nodes"]):
            GRAPH_DB["nodes"].append({"id": tp["id"], "type": "ThirdParty", "label": tp["name"]})
    for r in extracted["risks"]:
        if not any(n["id"] == r["id"] for n in GRAPH_DB["nodes"]):
            GRAPH_DB["nodes"].append({"id": r["id"], "type": "Risk", "label": r["label"]})
    for rel in extracted["relations"]:
        GRAPH_DB["edges"].append(rel)
