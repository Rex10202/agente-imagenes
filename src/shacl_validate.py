from rdflib import Graph
from pyshacl import validate
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "data" / "ontologia_agente_imagenes.ttl"

def run():
    assert TTL.exists(), f"Falta archivo: {TTL}"
    g = Graph().parse(TTL.as_posix(), format="turtle")
    conforms, rgraph, rtext = validate(
        data_graph=g, shacl_graph=g,  
        inference="rdfs",
        abort_on_first=False
    )
    print("Conforms:", conforms)
    print(rtext)

if __name__ == "__main__":
    run()
