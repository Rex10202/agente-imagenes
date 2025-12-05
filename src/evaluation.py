from typing import Dict, List, Optional, Set, Tuple
from PIL import Image, ImageStat
import numpy as np
from pathlib import Path

try:
    from transformers import ViTImageProcessor, ViTForImageClassification, AutoImageProcessor
    import torch
    _HAS_TRANSFORMERS = True
except Exception:
    _HAS_TRANSFORMERS = False

from .utils import to_english_labels

# Cache de modelo (si disponible)
_VIT = None
_VIT_PROC = None
_IMAGENET_LABELS = None

def _load_vit():
    global _VIT, _VIT_PROC, _IMAGENET_LABELS
    if _VIT is not None:
        return
    name = "google/vit-base-patch16-224"
    _VIT_PROC = AutoImageProcessor.from_pretrained(name)
    _VIT = ViTForImageClassification.from_pretrained(name)
    _IMAGENET_LABELS = _VIT.config.id2label

def _topk_labels(img: Image.Image, k: int = 10) -> List[str]:
    _load_vit()
    inputs = _VIT_PROC(images=img, return_tensors="pt")
    with torch.no_grad():
        logits = _VIT(**inputs).logits
    topk = torch.topk(logits, k).indices[0].tolist()
    return [str(_IMAGENET_LABELS[i]).lower() for i in topk]

def _coverage_from_labels(required_eng: Set[str], labels: List[str]) -> float:
    if not required_eng:
        return 1.0
    labels_set = set()
    for lab in labels:
        labels_set |= set(lab.split(","))
    labels_set = {w.strip().lower() for w in labels_set}
    hits = 0
    for tgt in required_eng:
        # hit si alguna palabra del target aparece como substring
        if any(tgt in lab for lab in labels_set):
            hits += 1
    return hits / max(1, len(required_eng))

def _similarity_jaccard(required_tokens: Set[str], labels: List[str]) -> float:
    if not required_tokens:
        return 0.5
    labels_tokens = set()
    for lab in labels:
        labels_tokens |= {w.strip().lower() for w in lab.replace(",", " ").split()}
    inter = len(required_tokens & labels_tokens)
    union = len(required_tokens | labels_tokens)
    return inter / union if union else 0.0

def _aesthetic_simple(img: Image.Image) -> float:
    # Brillo/contraste simplificado [0..1]
    stat = ImageStat.Stat(img.convert("L"))
    mean = stat.mean[0]      # 0..255
    std = stat.stddev[0]     # 0..~128
    # Normalizaciones heurísticas
    bright = abs(mean - 127.5) / 127.5  # 0 -> gris medio, 1 -> extremos
    contr = min(std / 64.0, 1.0)        # ~0..1
    return float(0.4*bright + 0.6*contr)

def evaluate_image(img_path: Path, required_es: List[str], estilos_es: List[str]) -> Dict:
    """
    Devuelve dict con: coverage, similarity, aesthetic y labels detectadas.
    Si no hay transformers/torch, usa un evaluador de reserva (estética + labels vacías),
    y calcula similarity como 0.5 por defecto si no hay labels.
    """
    img = Image.open(img_path).convert("RGB")
    req_eng = to_english_labels(required_es)
    req_tokens = req_eng | set(estilos_es)

    if _HAS_TRANSFORMERS:
        labels = _topk_labels(img, k=10)
        cov = _coverage_from_labels(req_eng, labels)
        sim = _similarity_jaccard(req_tokens, labels)
    else:
        labels = []
        cov = 1.0 if not req_eng else 0.0
        sim = 0.5

    aes = _aesthetic_simple(img)
    return {"coverage": cov, "similarity": sim, "aesthetic": aes, "labels": labels}
