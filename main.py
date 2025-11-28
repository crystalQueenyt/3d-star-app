import streamlit as st
import time
import os
from PIL import Image
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="3D STAR App",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURACIÓN DE IA (GEMINI) ---
# Intentamos conectar la llave secreta
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        st.session_state.api_ok = True
    else:
        st.session_state.api_ok = False
except:
    st.session_state.api_ok = False

# --- ESTÉTICA (CSS) ---
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
        st.markdown("### Generador de Personajes")
        
        if not st.session_state.api_ok:
            st.warning("⚠️ OJO: No detecté la API Key en los Secrets. La IA no funcionará.")
        
        if st.button("COMENZAR / START"):
            set_phase(1)

# --- FASE 1: LABORATORIO (IA) ---
elif st.session_state.phase == 1:
    st.title("🧪 LABORATORIO DE IA")
    st.write("Sube tu dibujo. Gemini lo analizará para crear el perfil.")
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        front_file = st.file_uploader("Vista Frontal", type=['png', 'jpg', 'jpeg'], key="front")
    
    if st.button("✨ ANALIZAR CON GEMINI ✨", use_container_width=True):
        if front_file:
            with st.spinner("🤖 Gemini está mirando tu dibujo..."):
                try:
                    # 1. Cargar imagen
                    image = Image.open(front_file)
                    
                    # 2. Llamar a la IA
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "Eres un experto en videojuegos. Analiza este personaje visualmente. Genera un perfil corto estilo RPG: Nombre sugerido, Clase (ej: Guerrero), Elemento (ej: Fuego) y una descripción de personalidad de 2 lineas. Usa formato simple."
                    
                    response = model.generate_content([prompt, image])
                    st.session_state.char_info = response.text
                    
                    st.success("¡Análisis Completado!")
                    time.sleep(2)
                    set_phase(2)
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
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
        st.subheader("🧠 ANÁLISIS DE GEMINI:")
        # Aquí mostramos lo que escribió la IA
        st.write(st.session_state.char_info)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.button("💾 GUARDAR PERSONAJE", use_container_width=True)
