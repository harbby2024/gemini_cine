import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Intentar importar genai y mostrar mensaje si falla
try:
    from google import genai
    GENAI_IMPORT_OK = True
except ImportError as e:
    GENAI_IMPORT_OK = False
    st.error(f"Error al importar 'genai': {e}\n"
             "Asegúrate de instalar 'google-generativeai' con:\n"
             "pip install google-generativeai")

# --- Configuración ---
load_dotenv()
st.set_page_config(page_title="CineBot 🎬", layout="wide")
st.title("🎬 CineBot: Recomendador + Chat Cinéfilo")

# --- Variables Globales ---
GENEROS = [
    "Acción", "Comedia", "Drama", "Sci-Fi", "Fantasía",
    "Terror", "Romance", "Animación", "Documental", "Thriller"
]

# --- Funciones ---
def generar_respuesta(prompt):
    if not GENAI_IMPORT_OK:
        return "Error: El módulo 'genai' no está disponible. Verifica la instalación."
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_KEY"))  # API key desde .env
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def recomendar_peliculas(generos, año_min, año_max):
    prompt = f"""
    Recomienda 3 películas que mezclen los géneros {", ".join(generos)} 
    (entre {año_min} y_
