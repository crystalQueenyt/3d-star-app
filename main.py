import streamlit as st
import time
import os
from PIL import Image
from openai import OpenAI # La nueva librería para la IA
import base64
import io
import json

# --- FUNCIÓN DE CONVERSIÓN A BASE64 (Necesaria para la API de OpenAI Vision) ---
def encode_image_to_base64(image_file):
    """Convierte un archivo de imagen subido por Streamlit a Base64."""
    img = Image.open(image_file)
    buffered = io.BytesIO()
    # Usamos JPEG para reducir el tamaño del archivo para la API
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="3D STAR App",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURACIÓN DE IA (OPENAI) ---
try:
    if "OPENAI_API_KEY" in st.secrets:
        # Usamos la nueva llave guardada
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        st.session_state.api_ok = True
    else:
        st.session_state.api_ok = False
except Exception:
    st.session_state.api_ok = False

# --- ESTÉTICA Y DISEÑO (CSS) ---
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        .stApp { background: linear-gradient(135deg, #1a0b2e 0%, #ff00cc 100%); color: white; font-family: 'Press Start 2P', cursive; }
        h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; font-family: 'Press Start 2P', cursive !important; text-shadow: 2px 2px #000000; }
        .stButton > button { background-color: #2b1055; color: white; border: 3px solid #00FFFF !important; border-radius: 0px; padding: 15px 30px; font-family: 'Press Start 2P', cursive; box-shadow: 4px 4px 0px #00FFFF; }
        .stButton > button:hover { background-color: #00FFFF; color: #1a0b2e; box-shadow: 6px 6px 0px #ff00cc; }
        .stTextInput > div > div > input, .stFileUploader { background-color: rgba(0, 0, 0, 0.5); border: 2px solid #00FFFF; color: white; }
        .stToast { background-color: #1a0b2e !important; border: 2px solid #00FFFF !important; color: white !important; }
        .generated-info { border: 2px dashed #ff00cc; padding: 20px; background: rgba(0,0,0,0.4); margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)
local_css()

# --- ESTADOS ---
if 'phase' not in st.session_state: st.session_state.phase = 0
if 'char_info' not in st.session_state: st.session_state.char_info = "Esperando análisis..."

def set_phase(phase_number):
    st.session_state.phase = phase_number
    st.rerun()

# --- FASE 0: INICIO ---
if st.session_state.phase == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 80px;'>🪐</h1>", unsafe_allow_html=True)
        st.title("3D STAR IA")
        st.markdown("### Generador de Perfiles (OpenAI)")
        
        if not st.session_state.api_ok:
            st.warning("⚠️ OJO: No detecté la llave de OpenAI. La IA no funcionará.")
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("ESPAÑOL"):
                st.session_state.language = 'ES'
                set_phase(1)
        with c_btn2:
            if st.button("ENGLISH"):
                st.session_state.language = 'EN'
                set_phase(1)

# --- FASE 1: LABORATORIO (IA) ---
elif st.session_state.phase == 1:
    st.title("🧪 LABORATORIO DE IA (OpenAI)")
    st.write("Sube tu dibujo. La IA lo analizará para crear el perfil.")
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        front_file = st.file_uploader("Vista Frontal", type=['png', 'jpg', 'jpeg'], key="front")
    
    # Placeholder for file uploader (removed, as we only need one file for vision analysis)
    with col_up2:
        st.markdown("#### 🚀 Ready to Analyze!")
        st.write("Solo necesitamos la vista frontal para el análisis de IA.")
    
    st.markdown("---")
    
    if st.button("✨ ANALIZAR CON IA ✨", use_container_width=True):
        if front_file:
            if st.session_state.api_ok:
                with st.spinner("🤖 IA Analizando tu dibujo..."):
                    try:
                        base64_image = encode_image_to_base64(front_file)
                        
                        prompt_text = "Eres un experto en videojuegos. Analiza este personaje y genera un perfil corto estilo RPG: 1. Nombre 2. Clase (Mago, Guerrero, etc.) 3. Elemento (Fuego, Agua, Sombra) 4. Una descripción de personalidad de 2 líneas. Responde solo con el perfil."

                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Genera el perfil del personaje en el formato solicitado, sin añadir introducciones ni conclusiones. Se breve."},
                                {"role": "user", "content": [
                                    {"type": "text", "text": prompt_text},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]}
                            ]
                        )
                        
                        st.session_state.char_info = response.choices[0].message.content
                        st.success("¡Análisis Completado!")
                        time.sleep(2)
                        set_phase(2)
                    except Exception as e:
                        # Error handling for API call (invalid key, etc.)
                        st.error(f"Error en la llamada a la IA: {e}")
                        st.error("Revisa que tu clave de OpenAI sea correcta y que no se haya agotado el crédito gratuito.")
            else:
                st.error("⚠️ Error: La llave de OpenAI no se cargó correctamente en Streamlit Secrets.")
        else:
            st.warning("⚠️ Sube al menos la imagen frontal.")

# --- FASE 2: RESULTADOS ---
elif st.session_state.phase == 2:
    with st.sidebar:
        st.title("🛠️ EDICIÓN")
        st.write("Herramientas visuales")
        if st.button("Reiniciar"): set_phase(0)

    st.title("👾 PERFIL GENERADO")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("""
        <div style="border: 4px solid #00FFFF; padding: 20px; text-align: center; background: rgba(0,0,0,0.3);">
            <div style="font-size: 100px;">🛡️</div>
            <p>VISUALIZACIÓN 3D (Simulada)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="generated-info">', unsafe_allow_html=True)
        st.subheader("🧠 ANÁLISIS DE LA IA:")
        # Aquí mostramos lo que escribió la IA
        st.markdown(st.session_state.char_info)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("💾 GUARDAR PERSONAJE", use_container_width=True):
        # 1. Muestra un mensaje de confirmación
        st.toast("✅ Personaje guardado (Simulado)!")
        
        # 2. Transiciona a la Fase 3
        time.sleep(1)
        set_phase(3)
