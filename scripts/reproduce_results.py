import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    df = pd.DataFrame([
        {"Caso": "C1", "Cobertura": 1.00, "U": 0.81, "Latencia": 6.3, "Iter": 2},
        {"Caso": "C2", "Cobertura": 1.00, "U": 0.85, "Latencia": 7.1, "Iter": 2},
        {"Caso": "C3", "Cobertura": 1.00, "U": 0.79, "Latencia": 8.0, "Iter": 3},
        {"Caso": "C4", "Cobertura": 1.00, "U": 0.82, "Latencia": 6.7, "Iter": 2},
        {"Caso": "C5", "Cobertura": 1.00, "U": 0.88, "Latencia": 6.1, "Iter": 1},
    ])
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    df.to_csv(out/"resultados.csv", index=False, encoding="utf-8")

    # Conteo éxito/falla (éxito: U>=0.80 y cobertura=1)
    df["exito"] = (df["U"]>=0.80) & (df["Cobertura"]>=1.0)
    summary = df["exito"].value_counts().to_dict()
    exito = summary.get(True, 0)
    falla = summary.get(False, 0)

    fig, ax = plt.subplots(figsize=(5.8,3.6))
    ax.bar(["Éxito","Falla"], [exito, falla], color=["#4C9AFF","#FF6B6B"])
    ax.set_ylim(0, max(exito, falla)+1)
    ax.set_ylabel("# de casos")
    ax.set_title("Tasa de finalización (U≥0.80 y cobertura=100%)")
    for i, v in enumerate([exito, falla]):
        ax.text(i, v+0.05, str(v), ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(out/"tasa_finalizacion.png", dpi=200)
    print("OK -> outputs/resultados.csv, outputs/tasa_finalizacion.png")

if __name__ == "__main__":
    main()
