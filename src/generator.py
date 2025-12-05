import time
import uuid
import requests
from pathlib import Path
from .config import IMG_DIR, POLLINATIONS_BASE, N8N_IMAGE_ENDPOINT, WIDTH, HEIGHT, MODEL_HINT

def _save_bytes_as_png(content: bytes, stem: str) -> Path:
    p = IMG_DIR / f"{stem}.png"
    with open(p, "wb") as f:
        f.write(content)
    return p

def create_image(prompt: str, width: int = WIDTH, height: int = HEIGHT) -> Path:
    """
    Genera imagen usando:
    - n8n (si N8N_IMAGE_ENDPOINT está configurado), o
    - Pollinations (fallback público).
    Devuelve la ruta del archivo PNG guardado.
    """
    stem = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    if N8N_IMAGE_ENDPOINT:
        # Se asume un endpoint POST JSON de n8n que devuelve bytes o URL.
        payload = {"prompt": prompt, "width": width, "height": height, "model": MODEL_HINT}
        r = requests.post(N8N_IMAGE_ENDPOINT, json=payload, timeout=90)
        r.raise_for_status()
        # Si devuelve JSON con 'image' en base64 o URL, modifique según su flujo:
        # --- ejemplo genérico: si ya retorna bytes PNG ---
        return _save_bytes_as_png(r.content, stem)
    else:
        # Pollinations: imagen directa por GET
        url = f"{POLLINATIONS_BASE}/{requests.utils.quote(prompt)}?width={width}&height={height}"
        r = requests.get(url, timeout=90)
        r.raise_for_status()
        return _save_bytes_as_png(r.content, stem)
