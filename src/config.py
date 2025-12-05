from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Ontología/Turtle 
TTL_PATH = DATA_DIR / "ontologia_agente_imagenes.ttl"

# Pesos de la utilidad U = w1*sim + w2*cov + w3*aes (todas en [0,1])
W_SIM, W_COV, W_AES = 0.4, 0.4, 0.2
Q_STAR = 0.80                     # umbral de calidad
MAX_ITERS = 3                     # iteraciones de refinamiento

# Generación de imágenes:
# 1) Si corre n8n, exponga un endpoint y defínalo aquí:
N8N_IMAGE_ENDPOINT = os.getenv("N8N_IMAGE_ENDPOINT", "").strip()
# 2) Fallback: servicio público de ejemplo (Pollinations):
POLLINATIONS_BASE = "https://image.pollinations.ai/prompt"

# Dimensiones por defecto:
WIDTH, HEIGHT = 768, 768
MODEL_HINT = os.getenv("GEN_MODEL", "stable-diffusion")
