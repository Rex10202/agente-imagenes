import requests

def create_image(prompt: str, base_url: str) -> dict:
    """Realiza la solicitud de imagen. Devuelve dict con URL/bytes según API."""
    url = f"{base_url.rstrip('/')}/prompt/{requests.utils.quote(prompt)}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    # Dependiendo de la API, aquí podría venir un JSON o bytes de imagen:
    return {"status": resp.status_code, "content": resp.content}
