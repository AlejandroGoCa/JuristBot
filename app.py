import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="JurisBot Perú", page_icon="⚖️", layout="centered")

# --- BASE DE DATOS DE CONOCIMIENTO ---
# Aquí configuramos los temas. El bot buscará estas palabras clave.
BASE_CONOCIMIENTO = [
    {
        "tema": "Delitos Informáticos (Hackeo/Datos)",
        "keywords": ["robo de informacion", "datos", "hackear", "contraseña", "informatico", "cibernetico", "acceso ilicito", "redes sociales"],
        "respuesta": "💻 **Delitos Informáticos (Ley N° 30096):** \n\nEl acceso ilícito a sistemas o el robo de datos tiene pena privativa de libertad. Si robas información de un usuario, la pena puede ser **entre 3 y 8 años de cárcel**, especialmente si afectas la intimidad o secreto de las comunicaciones."
    },
    {
        "tema": "Robo y Hurto (Físico)",
        "keywords": ["robo", "asalto", "celular", "cartera", "armada", "hurto", "pistola", "ladron"],
        "respuesta": "👮 **Robo vs Hurto (Código Penal):** \n\n* **Hurto (Sin violencia):** Pena de 1 a 3 años (Art. 185).\n* **Robo (Con violencia/amenaza):** Pena de 3 a 8 años (Art. 188).\n* **Robo Agravado:** Si usan armas o es de noche, la pena sube a **12 a 20 años**."
    },
    {
        "tema": "Homicidio / Vida",
        "keywords": ["matar", "homicidio", "asesinato", "feminicidio", "muerte"],
        "respuesta": "⚰️ **Delitos contra la Vida:** \n\n* **Homicidio Simple:** 6 a 20 años.\n* **Asesinato (Homicidio Calificado):** No menor de 15 años (por lucro, ferocidad, fuego, veneno).\n* **Feminicidio:** Pena no menor de 20 años."
    },
    {
        "tema": "Divorcio / Familia",
        "keywords": ["divorcio", "separacion", "infidelidad", "adulterio", "esposo", "esposa"],
        "respuesta": "💔 **Divorcio (Código Civil Art. 333):** \n\nLas causales principales son: Adulterio, violencia física/psicológica, abandono del hogar (2 años) e injuria grave. También existe el Divorcio Municipal (Rápido) si ambos están de acuerdo."
    },
    {
        "tema": "Alimentos (Pensión)",
        "keywords": ["alimentos", "pension", "hijos", "comida", "manutencion", "papa no paga"],
        "respuesta": "🍎 **Pensión de Alimentos:** \n\nEs un derecho de los hijos hasta los 28 años (si estudian). Incluye: Comida, casa, ropa, salud y recreación. Se calcula según las necesidades del niño y la capacidad del padre."
    },
    {
        "tema": "Trabajo / Despido",
        "keywords": ["despido", "trabajo", "sueldo", "laboral", "jornada", "horas extra", "liquidacion"],
        "respuesta": "👷 **Derecho Laboral:** \n\n* **Jornada:** Máximo 48 horas semanales.\n* **Despido Arbitrario:** Tienes derecho a indemnización (1.5 sueldos por año).\n* **Beneficios:** Tienes derecho a Gratificación (Julio/Diciembre) y CTS."
    },
     {
        "tema": "Saludos",
        "keywords": ["hola", "buenos dias", "buenas tardes", "que tal", "inicio"],
        "respuesta": "¡Hola! Soy **JurisBot**. Tu asistente en Derecho Peruano. Pregúntame sobre robos, informática, familia o trabajo."
    }
]

def buscar_respuesta(pregunta_usuario):
    pregunta_usuario = pregunta_usuario.lower() # Todo a minúsculas
    
    # 1. Buscamos en cada tema
    for tema in BASE_CONOCIMIENTO:
        for palabra in tema["keywords"]:
            if palabra in pregunta_usuario:
                return tema["respuesta"]
    
    # 2. Si no encuentra nada
    return "🤔 No tengo esa información exacta. Intenta preguntar sobre: 'robo de datos', 'divorcio', 'despido' o 'alimentos'."

# --- INTERFAZ GRÁFICA ---

st.title("⚖️ JurisBot Perú")
st.markdown("### Asistente Legal para Estudiantes")
st.info("Escribe tu duda legal abajo. Ejemplo: *'¿Cuál es la pena por robo de información?'*")

# Historial de chat
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Capturar entrada
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    # Guardar y mostrar mensaje usuario
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Buscar respuesta
    respuesta_bot = buscar_respuesta(prompt)

    # Guardar y mostrar respuesta bot
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_bot})
    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)

# Pie de página
st.write("---")
st.caption("Proyecto Universitario - Derecho & Tecnología")