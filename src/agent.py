from dataclasses import dataclass, asdict
from pathlib import Path
import json, time
from typing import Dict, List

from .config import OUT_DIR, W_SIM, W_COV, W_AES, Q_STAR, MAX_ITERS
from .utils import extract_requirements, refine_prompt
from .generator import create_image
from .evaluation import evaluate_image
from .ontology import build_graph, shacl_validate

@dataclass
class AgentState:
    prompt_base: str
    prompt_actual: str
    iter: int = 0
    mejor_U: float = 0.0
    mejor_img: str = ""
    log: List[Dict] = None

def utilidad(sim: float, cov: float, aes: float) -> float:
    return float(W_SIM*sim + W_COV*cov + W_AES*aes)

def run_agent(descripcion: str) -> Dict:
    req_es, est_es = extract_requirements(descripcion)
    st = AgentState(prompt_base=descripcion, prompt_actual=descripcion, log=[])

    for k in range(1, MAX_ITERS+1):
        st.iter = k
        img_path = create_image(st.prompt_actual)
        metrics = evaluate_image(img_path, req_es, est_es)
        U = utilidad(metrics["similarity"], metrics["coverage"], metrics["aesthetic"])
        metrics["U"] = U

        # SHACL (construye grafo y valida)
        g = build_graph(img_path, req_es, metrics)
        sh = shacl_validate(g)

        step = {
            "iter": k,
            "prompt": st.prompt_actual,
            "image": str(img_path),
            "metrics": metrics,
            "shacl": {"conforms": sh["conforms"]}
        }
        st.log.append(step)

        # criterio de paro: U >= Q* y SHACL conforme
        if U >= Q_STAR and sh["conforms"]:
            st.mejor_U = U
            st.mejor_img = str(img_path)
            break

        # Refinamiento: si cobertura < 1.0, forzar elementos faltantes en el prompt
        missing = []
        if metrics["coverage"] < 1.0:
            # estrategia simple: vuelve a pedir explícitamente los elementos requeridos
            missing = req_es
        st.prompt_actual = refine_prompt(st.prompt_actual, missing)

        if U > st.mejor_U:
            st.mejor_U = U
            st.mejor_img = str(img_path)

    # Guardar traza
    OUT_DIR.mkdir(exist_ok=True, parents=True)
    out_json = OUT_DIR / f"trace_{int(time.time())}.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "descripcion": descripcion,
            "requeridos_es": req_es,
            "estilos_es": est_es,
            "mejor_U": st.mejor_U,
            "mejor_img": st.mejor_img,
            "historial": st.log
        }, f, ensure_ascii=False, indent=2)
    return {"trace": str(out_json), "best_image": st.mejor_img, "best_U": st.mejor_U}
