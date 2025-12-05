from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rdflib import Graph
from src.config import TTL_PATH

def run():
    assert TTL_PATH.exists(), f"Falta: {TTL_PATH}"
    g = Graph().parse(TTL_PATH.as_posix(), format="turtle")
    print(f"TTL cargado OK ({len(g)} triples) -> {TTL_PATH}")

if __name__ == "__main__":
    run()
