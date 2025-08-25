# app/api/wikipedia.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import requests
from requests.exceptions import RequestException, Timeout
import urllib.parse

router = APIRouter(prefix="/wikipedia", tags=["Wikipedia"])

WIKI_API_BASE = "https://es.wikipedia.org/api/rest_v1/page/summary/"
WIKI_PAGE_BASE = "https://es.wikipedia.org/wiki/"
HEADERS = {"User-Agent": "MiApp/1.0 (contacto@example.com)"}


@router.get("/book_summary/{title}")
def book_summary(title: str):
    """Devuelve el JSON de resumen de Wikipedia para un título."""
    title_encoded = urllib.parse.quote(title)
    url = f"{WIKI_API_BASE}{title_encoded}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
    except (RequestException, Timeout):
        raise HTTPException(status_code=502, detail="Error consultando Wikipedia")
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No se encontró información para '{title}'")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Respuesta inesperada de Wikipedia ({r.status_code})")
    return r.json()


@router.get("/autor_wiki/{title}")
def autor_wiki(title: str):
    """
    Redirige a la página de Wikipedia si existe, 
    o a la búsqueda de Wikipedia si no.
    """
    title_encoded = urllib.parse.quote(title.replace(" ", "_"))
    wiki_url = f"{WIKI_PAGE_BASE}{title_encoded}"
    api_url = f"{WIKI_API_BASE}{title_encoded}"

    try:
        r = requests.get(api_url, headers=HEADERS, timeout=5)
    except (RequestException, Timeout):
        raise HTTPException(status_code=502, detail="Error consultando Wikipedia")

    if r.status_code == 404:
        # Redirijo a la búsqueda en Wikipedia
        search_url = f"https://es.wikipedia.org/w/index.php?search={urllib.parse.quote(title)}"
        return RedirectResponse(url=search_url, status_code=307)

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Respuesta inesperada de Wikipedia ({r.status_code})")

    # Redirijo a la página del artículo
    return RedirectResponse(url=wiki_url, status_code=307)
