from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]   # .../Agente
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.agent import run_agent

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--descripcion", required=True)
    args = p.parse_args()

    res = run_agent(args.descripcion)
    print("OK")
    print(f"Best U: {res['best_U']:.3f}")
    print(f"Imagen: {res['best_image']}")
    print(f"Traza:  {res['trace']}")

if __name__ == "__main__":
    main()
