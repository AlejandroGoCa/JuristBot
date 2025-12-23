import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
from PIL import Image
import PyPDF2
from io import BytesIO

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(
    page_title="JurisBot Pro", 
    page_icon="⚖️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. CONEXIÓN A LA IA ---
API_KEY_GOOGLE = "AIzaSyAdKwvOTdeTW77zd2_QFlyYrPpvlwIyWwQ"
genai.configure(api_key=API_KEY_GOOGLE)

def conectar_modelo():
    nombres = ['models/gemini-flash-latest', 'models/gemini-pro-latest', 'gemini-pro']
    for n in nombres:
        try:
            return genai.GenerativeModel(n)
        except:
            continue
    return None

model = conectar_modelo()

# --- 3. FUNCIONES INTELIGENTES ---
def leer_documento(uploaded_file):
    texto = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                texto += page.extract_text() + "\n"
        elif uploaded_file.type == "text/plain":
            texto = str(uploaded_file.read(), "utf-8")
    except:
        return None
    return texto

def transcribir_voz(audio_file):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            return r.recognize_google(audio_data, language="es-PE")
    except:
        return None

def cerebro_jurisbot(texto, archivo=None, tipo=None):
    contenido = []
    if tipo == "imagen" and archivo:
        contenido = [f"Actúa como perito legal. Analiza esta imagen y responde: {texto}", archivo]
    elif tipo == "doc" and archivo:
        contenido = f"Actúa como abogado. Analiza este documento: {archivo[:10000]}. Pregunta: {texto}"
    else:
        contenido = f"Soy JurisBot, abogado peruano. Responde: {texto}"

    if model:
        try:
            return model.generate_content(contenido).text
        except Exception as e:
            return f"❌ Error: {str(e)}"
    return "🤖 Desconectado."

# --- 4. CSS CORREGIDO (MICROFONO A LA DERECHA) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@500;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8f9fa; }

    /* Estilo del Título */
    .titulo-container {
        background: white; padding: 2rem; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center;
        margin-bottom: 2rem; border-bottom: 4px solid #880e4f;
    }
    .titulo-principal { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 2.5rem; color: #880e4f; margin: 0; }
    
    /* Burbujas de Chat */
    .stChatMessage { border-radius: 20px; margin-bottom: 15px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    div[data-testid="stChatMessageUser"] { background: #e3f2fd; color: #0d47a1; border-left: 4px solid #1565c0; }
    div[data-testid="stChatMessageAssistant"] { background: white; color: #212121; border-left: 4px solid #880e4f; }

    /* --- 🎙️ POSICIÓN DEL MICRÓFONO (LATERAL DERECHO) --- */
    [data-testid="stAudioInput"] {
        position: fixed;
        bottom: 90px;            /* Un poco más arriba para no chocar con el input */
        right: 30px;             /* PEGADO A LA DERECHA */
        left: auto;              /* Quitamos el centrado */
        transform: none;         /* Quitamos el centrado */
        
        width: 300px !important; /* Tamaño compacto */
        z-index: 1000;
        
        background-color: white; 
        border: 2px solid #880e4f;
        border-radius: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        padding: 5px 15px;
    }
    
    /* Ocultar etiqueta de texto del micro */
    [data-testid="stAudioInput"] label { display: none; }

    /* Padding extra para que el último mensaje se lea bien */
    .main .block-container {
        padding-bottom: 150px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. BARRA LATERAL ---
with st.sidebar:
    try:
        st.image("logo.png", width=110)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/Escudo_UNJFSC.png", width=110)
        
    st.markdown("### ⚖️ JurisBot AI")
    st.info("👇 **Modo de Análisis:**")
    opcion = st.radio("", ["💬 Solo Chat", "📸 Imagen (Evidencia)", "📄 Documento (PDF/TXT)"])
    
    archivo_proc = None
    tipo_proc = None

    if opcion == "📸 Imagen (Evidencia)":
        f = st.file_uploader("Sube foto:", type=["jpg", "png", "jpeg"])
        if f:
            st.image(f, caption="Evidencia", use_column_width=True)
            archivo_proc = Image.open(f)
            tipo_proc = "imagen"
            st.success("✅ Imagen lista")

    elif opcion == "📄 Documento (PDF/TXT)":
        f = st.file_uploader("Sube contrato:", type=["pdf", "txt"])
        if f:
            t = leer_documento(f)
            if t:
                archivo_proc = t
                tipo_proc = "doc"
                st.success("✅ Documento leído")

    st.markdown("---")
    if st.button("🗑️ Limpiar Chat", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

# --- 6. INTERFAZ PRINCIPAL ---
st.markdown("""
    <div class="titulo-container">
        <h1 class="titulo-principal">JurisBot Perú</h1>
        <p style="color:#666;">Asistente Legal Inteligente (Voz • Visión • Texto)</p>
    </div>
""", unsafe_allow_html=True)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [{"role": "assistant", "content": "👋 **¡Hola!**\n\nSoy JurisBot. Puedes escribirme o usar el **micrófono** 🎙️ que está a la derecha para hablarme."}]

# Historial
for m in st.session_state.mensajes:
    with st.chat_message(m["role"], avatar="⚖️" if m["role"] == "assistant" else "👤"):
        st.markdown(m["content"])

# --- 7. ZONA DE ENTRADA ---
audio = st.audio_input("Grabar") # Flota a la derecha por CSS
texto = st.chat_input("Escribe tu consulta legal aquí...") # Se queda fijo abajo al centro

prompt = None

if audio:
    with st.spinner("👂 Transcribiendo..."):
        t = transcribir_voz(audio)
        if t: prompt = t
        else: st.warning("⚠️ No se escuchó bien.")

if texto:
    prompt = texto

if prompt:
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.spinner("⚖️ Analizando..."):
        res = cerebro_jurisbot(prompt, archivo_proc, tipo_proc)

    st.session_state.mensajes.append({"role": "assistant", "content": res})
    with st.chat_message("assistant", avatar="⚖️"):
        st.markdown(res)