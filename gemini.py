import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

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
    """Función para interactuar con Gemini (ya existente en tu código)"""
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_KEY"))  # API key desde .env
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def recomendar_peliculas(generos, año_min, año_max,):
    """Genera recomendaciones personalizadas"""
    prompt = f"""
    Recomienda 3 películas que mezclen los géneros {", ".join(generos)} 
    (entre {año_min} y {año_max}).
    Incluye:
    1. Título y año.
    2. Breve reseña (sin spoilers).
    3. Una curiosidad o dato interesante.
    Formatea la respuesta en markdown.
    """
    return generar_respuesta(prompt)

# --- Sidebar (Configuración) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    generos_seleccionados = st.multiselect(
        "Géneros favoritos:", 
        GENEROS, 
        default=["Comedia", "Sci-Fi"]
    )
    año_min, año_max = st.slider(
        "Rango de años:", 
        1970, 2025, (1990, 2020)
    )

# --- Pestañas Principales ---
tab1, tab2 = st.tabs(["🎥 Recomendador", "💬 Chat Cinéfilo"])

with tab1:
    # --- Sección de Recomendaciones ---
    st.subheader(f"🍿 Para tu combo {', '.join(generos_seleccionados)}")
    if st.button("Generar Recomendaciones", type="primary"):
        if not generos_seleccionados:
            st.warning("Selecciona al menos un género.")
        else:
            with st.spinner("Buscando joyas cinematográficas..."):
                recomendaciones = recomendar_peliculas(
                    generos_seleccionados, año_min, año_max,
                )
                st.markdown(recomendaciones)
    
    # --- Ejemplos guardados (Session State) ---
    if "historial_recomendaciones" not in st.session_state:
        st.session_state.historial_recomendaciones = []
    
    if st.button("Guardar estas recomendaciones"):
        st.session_state.historial_recomendaciones.append(recomendaciones)
        st.success("¡Guardado en historial!")
    
    if st.session_state.historial_recomendaciones:
        with st.expander("📜 Historial de Recomendaciones"):
            for idx, rec in enumerate(st.session_state.historial_recomendaciones):
                st.markdown(f"**Recomendación {idx+1}**")
                st.markdown(rec)

with tab2:
    # --- Chat Cinéfilo -----
    st.subheader("💬 Pregúntame sobre cine")
    pregunta = st.text_input(
        "Escribe tu pregunta (ej: 'Explica el final de Inception'):",
        placeholder="¿Qué película...?"
    )
    if st.button("Enviar Pregunta"):
        with st.spinner("Pensando como un crítico..."):
            respuesta = generar_respuesta(
                f"Responde como experto en cine: {pregunta}. "
                "Sé conciso pero detallado. Usa emojis si es apropiado."
            )
            st.markdown("**Respuesta:**")
            st.markdown(respuesta)


    ##AIzaSyBB3qCacAwI5KIavgbNgKCsgPv4iyfsQG8