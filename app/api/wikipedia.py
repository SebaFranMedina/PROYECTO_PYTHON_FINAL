# app/api/wikipedia.py
from fastapi import APIRouter
import requests
import urllib.parse

router = APIRouter(tags=["Wikipedia"])

@router.get("/book_summary/{title}")
def book_summary(title: str):
    """
    Busca un resumen de Wikipedia de un libro dado su título.
    Devuelve JSON con la información de la página.
    """
    # Codifica correctamente el título para URL
    title_encoded = urllib.parse.quote(title)
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{title_encoded}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"No se encontró información para '{title}'"}
    
    return response.json()
