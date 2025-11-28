import streamlit as st
import time
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="3D STAR App",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 1. ESTÉTICA Y DISEÑO (CSS INYECTADO) ---
def local_css():
    st.markdown("""
    <style>
        /* Importar fuente Pixelada */
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        /* Fondo General: Degradado Morado a Rosa Neón */
        .stApp {
            background: linear-gradient(135deg, #1a0b2e 0%, #ff00cc 100%);
            color: white;
            font-family: 'Press Start 2P', cursive;
        }

        /* Textos y Títulos */
        h1, h2, h3, p, label, .stMarkdown {
            color: #FFFFFF !important;
            font-family: 'Press Start 2P', cursive !important;
            text-shadow: 2px 2px #000000;
        }

        /* Botones Estilo Bloque Gamer */
        .stButton > button {
            background-color: #2b1055;
            color: white;
            border: 3px solid #00FFFF !important; /* Borde CIAN Brillante */
            border-radius: 0px; /* Cuadrados */
            padding: 15px 30px;
            font-family: 'Press Start 2P', cursive;
            transition: all 0.3s ease;
            box-shadow: 4px 4px 0px #00FFFF; /* Sombra sólida cian */
        }

        .stButton > button:hover {
            background-color: #00FFFF;
            color: #1a0b2e;
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0px #ff00cc;
        }

        /* Inputs y File Uploader */
        .stTextInput > div > div > input, .stFileUploader {
            background-color: rgba(0, 0, 0, 0.5);
            border: 2px solid #00FFFF;
            color: white;
            font-family: 'Press Start 2P', cursive;
        }

        /* Checkbox */
        .stCheckbox {
            color: white !important;
        }

        /* Mensajes Toast/Success */
        .stToast {
            background-color: #1a0b2e !important;
            border: 2px solid #00FFFF !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- GESTIÓN DE ESTADO (STATE MACHINE) ---
if 'phase' not in st.session_state:
    st.session_state.phase = 0
if 'language' not in st.session_state:
    st.session_state.language = 'ES'
if 'model_ready' not in st.session_state:
    st.session_state.model_ready = False

# Función para cambiar de fase
def set_phase(phase_number):
    st.session_state.phase = phase_number
    st.rerun() # Recarga inmediata

# --- FASE 0: EL MUNDO (INICIO) ---
if st.session_state.phase == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🌍 3D STAR 🌍")
        st.markdown("### Selecciona tu idioma / Select Language")
        
        # Animación simple usando un emoji gigante centrado
        st.markdown("<h1 style='text-align: center; font-size: 100px;'>🪐</h1>", unsafe_allow_html=True)
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("ESPAÑOL"):
                st.session_state.language = 'ES'
                set_phase(1)
        with c_btn2:
            if st.button("ENGLISH"):
                st.session_state.language = 'EN'
                set_phase(1)

# --- FASE 1: EL LABORATORIO (GENERACIÓN) ---
elif st.session_state.phase == 1:
    st.title("🧪 LABORATORIO DE CREACIÓN")
    st.write("Sube tus referencias para generar el modelo.")
    
    col_up1, col_up2 = st.columns(2)
    
    with col_up1:
        st.markdown("#### 📷 VISTA FRONTAL")
        front_img = st.file_uploader("Sube PNG Frontal", type=['png'], key="front")
    
    with col_up2:
        st.markdown("#### 📷 VISTA TRASERA")
        back_img = st.file_uploader("Sube PNG Trasera", type=['png'], key="back")
    
    st.markdown("---")
    
    # Botón Central Grande
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        if st.button("✨ PROCESAR 3D STAR ✨", use_container_width=True):
            if front_img and back_img:
                with st.spinner("🤖 IA Trabajando... Generando vértices..."):
                    time.sleep(3) # Simulación de IA
                    st.session_state.model_ready = True
                    st.success("¡Modelo Generado con éxito!")
                    time.sleep(1)
                    set_phase(2)
            else:
                st.error("⚠️ Por favor sube ambas imágenes.")

# --- FASE 2: EL TALLER (EDICIÓN) ---
elif st.session_state.phase == 2:
    
    # Barra Lateral Personalizada
    with st.sidebar:
        st.title("🛠️ HERRAMIENTAS")
        
        with st.expander("👤 CABEZA", expanded=True):
            if st.button("Pintar Cara"): st.toast("🖌️ Pincel Cabeza Activado")
            if st.button("Zoom Cabeza"): st.toast("🔍 Zoom Cabeza")
            
        with st.expander("👕 TORSO"):
            if st.button("Pintar Torso"): st.toast("🖌️ Pincel Torso Activado")
            if st.button("Separar Brazos"): st.toast("✂️ Brazos Separados")

        with st.expander("👖 PIERNAS"):
            if st.button("Pintar Piernas"): st.toast("🖌️ Pincel Piernas Activado")

    # Área Principal
    st.title("🎨 EL TALLER 3D")
    
    col_visor, col_info = st.columns([3, 1])
    
    with col_visor:
        # Placeholder del Visor 3D (Simulado con imagen giratoria o estática por ahora)
        st.markdown("""
        <div style="border: 4px solid #00FFFF; padding: 20px; text-align: center; background: rgba(0,0,0,0.3);">
            <h3 style="color:cyan;">VISOR 3D STAR</h3>
            <div style="font-size: 150px;">👾</div>
            <p>Modelo: STAR-CHIBI-01</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info:
        st.info("Usa la barra lateral para editar las partes.")

    st.markdown("---")
    
    # Zona de Guardado
    st.subheader("💾 GUARDAR PROGRESO")
    c_save1, c_save2 = st.columns([2, 1])
    
    with c_save1:
        save_mode = st.checkbox("Guardar pintado completo (Full Texture)")
        save_parts = st.checkbox("Guardar por partes (Split Mesh)")
    
    with c_save2:
        if st.button("GUARDAR EN GALERÍA", use_container_width=True):
            # Lógica de guardado simulada
            folder_name = "Galeria_3D_Star"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # Crear un archivo dummy
            with open(f"{folder_name}/modelo_{int(time.time())}.txt", "w") as f:
                f.write("Datos del modelo 3D")
                
            st.toast("💾 ¡Guardado en Galería!")
            time.sleep(1.5)
            set_phase(3)

# --- FASE 3: LA GALERÍA (FINAL) ---
elif st.session_state.phase == 3:
    st.title("🏆 GALERÍA 3D STAR")
    
    folder_name = "Galeria_3D_Star"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    files = os.listdir(folder_name)
    
    if len(files) == 0:
        st.warning("No hay modelos guardados aún.")
    else:
        st.write(f"Modelos encontrados: {len(files)}")
        
        # Grid de visualización
        cols = st.columns(4)
        for i, file in enumerate(files):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="border: 2px solid #00FFFF; padding: 10px; margin-bottom: 10px; text-align: center;">
                    <div style="font-size: 50px;">📦</div>
                    <p style="font-size: 10px;">{file}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 VOLVER AL INICIO"):
        st.session_state.model_ready = False
        set_phase(0)
