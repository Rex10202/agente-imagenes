import re
from typing import List, Tuple, Set

VOCAB_ES = {
    # objetos comunes (es -> conjunto de sinónimos/inglés aproximado)
    "gato": {"cat", "kitten"},
    "perro": {"dog", "puppy"},
    "silla": {"chair"},
    "mesa": {"table", "desk"},
    "coche": {"car", "vehicle"},
    "árbol": {"tree"},
    "cielo": {"sky"},
    "mar": {"sea", "ocean"},
    "montaña": {"mountain"},
    "persona": {"person", "human", "man", "woman", "boy", "girl"},
    "hombre": {"man"},
    "mujer": {"woman"},
    "niño": {"boy", "child"},
    "niña": {"girl", "child"},
    "flor": {"flower"},
    "pájaro": {"bird"},
}

ESTILOS = {"realista", "minimalista", "acrílico", "acuarela", "pixel art", "3d", "boceto"}

def normalize_text(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\wáéíóúñü\s-]", " ", s, flags=re.UNICODE)
    s = re.sub(r"\s+", " ", s)
    return s

def extract_requirements(desc: str) -> Tuple[List[str], List[str]]:
    """
    Extrae elementos requeridos y estilos muy simple (sin LLM).
    Regresa (elementos_es, estilos_es).
    """
    s = normalize_text(desc)
    elems = [w for w in VOCAB_ES.keys() if re.search(rf"\b{re.escape(w)}\b", s)]
    estilos = [e for e in ESTILOS if re.search(rf"\b{re.escape(e)}\b", s)]
    return sorted(set(elems)), sorted(set(estilos))

def to_english_labels(elems_es: List[str]) -> Set[str]:
    """Mapea requisitos en español a etiquetas en inglés para match con clasificadores."""
    eng = set()
    for es in elems_es:
        eng |= VOCAB_ES.get(es, set())
    return eng

def refine_prompt(base_prompt: str, missing_es: List[str]) -> str:
    """Estrategia de refinamiento simple: añadir los elementos faltantes al prompt."""
    if not missing_es:
        return base_prompt
    extra = ", incluir " + ", ".join(missing_es)
    if extra in base_prompt:
        return base_prompt
    return f"{base_prompt}{extra}"
