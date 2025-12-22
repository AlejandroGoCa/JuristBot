import streamlit as st
import time
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="JurisBot AI - Sistema Experto", page_icon="⚖️", layout="centered")

# --- ESTILOS CSS (Apariencia tipo ChatGPT) ---
st.markdown("""
    <style>
    .stChatMessage { padding: 1.2rem; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #f0f2f6; border-left: 5px solid #2980b9; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #e8f5e9; border-left: 5px solid #27ae60; }
    h1 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE CONOCIMIENTO MASIVA (CEREBRO DEL BOT) ---
BASE_CONOCIMIENTO = [

    {
        "tema": "Retraso / Olvido de Pensión",
        "keywords": ["no deposite", "olvide pagar", "se me paso pagar", "no pague", "retraso pension", "me olvide la pension", "por accidente no pague"],
        "respuesta": "🏦 **Retraso en Pensión de Alimentos:**\n\nSi fue un error o 'accidente' y no depositaste a tiempo:\n1. **Deposita inmediatamente** (incluyendo los intereses legales).\n2. Guarda el voucher.\n\n⚠️ **Ojo:** Si esto se vuelve constante, la madre puede denunciarte por **Omisión a la Asistencia Familiar** y podrías ir a la cárcel, aunque digas que fue 'sin querer'."
    },

    # ==================== DELITOS CONTRA LA VIDA Y CUERPO ====================
    {
        "tema": "Homicidio Culposo (Accidentes)",
        "keywords": ["culposo", "accidente", "atropello", "atropellar", "imprudencia", "negligencia", "sin querer", "casualidad", "choque"],
        "respuesta": "🚗 **Homicidio Culposo (Art. 111 CP):**\n\nSi causas la muerte de alguien por negligencia o accidente de tránsito (sin intención de matar), la pena es privativa de libertad no mayor de **2 años**.\n\n⚠️ **Agravante:** Si el conductor huye o estaba ebrio, la pena sube a entre **4 y 8 años**."
    },
    
    {
        "tema": "Feminicidio",
        "keywords": ["feminicidio", "mato a su mujer", "mato a su pareja", "violencia de genero", "ex pareja"],
        "respuesta": "🟣 **Feminicidio (Art. 108-B CP):**\n\nAsesinar a una mujer por su condición de tal (contexto de violencia familiar, acoso, abuso de poder).\n\n⚖️ **Pena:** No menor de **20 años**. Puede ser **Cadena Perpetua** si hay agravantes (menores de edad, gestantes o crueldad)."
    },
    {
        "tema": "Homicidio Simple / Asesinato",
        "keywords": ["homicidio", "asesinato", "matar a alguien", "sicariato", "veneno", "alevosia"],
        "respuesta": "⚰️ **Homicidio y Asesinato:**\n\n* **Homicidio Simple (Art. 106):** Matar a otro. Pena: 6 a 20 años.\n* **Homicidio Calificado (Asesinato):** Si se mata por lucro (dinero), ferocidad, alevosía (traición) o veneno. Pena no menor de **15 años**."
    },
    {
        "tema": "Lesiones",
        "keywords": ["golpear", "golpe", "pelea", "lesiones", "sangre", "puñete", "herido"],
        "respuesta": "🤕 **Lesiones (Art. 121 y 122 CP):**\n\n* **Leves:** Si requieren 10 a 30 días de asistencia médica (Pena 2-5 años).\n* **Graves:** Si ponen en peligro la vida o mutilan un miembro (Pena 4-8 años).\n* **Faltas:** Si el daño es mínimo (requiere menos de 10 días de descanso), se castiga con servicios comunitarios."
    },

    # ==================== DELITOS CONTRA EL PATRIMONIO ====================
    {
        "tema": "Robo Agravado",
        "keywords": ["arma", "pistola", "cuchillo", "navaja", "mano armada", "banda", "noche", "agravado"],
        "respuesta": "🔫 **Robo Agravado (Art. 189 CP):**\n\nSe considera agravado si robas:\n1. A mano armada.\n2. Durante la noche.\n3. En banda (2 o más personas).\n\n⚖️ **Pena:** Cárcel efectiva entre **12 y 20 años**. Si causas lesiones graves a la víctima, es Cadena Perpetua."
    },
    {
        "tema": "Extorsión (Gota a gota)",
        "keywords": ["extorsion", "cupo", "cobro de cupos", "gota a gota", "amenaza de muerte", "plata o plomo"],
        "respuesta": "📞 **Extorsión (Art. 200 CP):**\n\nObligar a alguien a dar dinero mediante violencia o amenaza. Incluye el 'cobro de cupos' y préstamos 'gota a gota'.\n\n⚖️ **Pena:** 10 a 15 años de cárcel. Si usan explosivos o matan a alguien, es Cadena Perpetua."
    },
    {
        "tema": "Usurpación (Invasión)",
        "keywords": ["invasion", "terreno", "invadir", "trafico de terrenos", "usurpacion", "lote"],
        "respuesta": "🏠 **Usurpación (Art. 202 CP):**\n\nOcupar un inmueble ajeno mediante violencia, engaño o abuso de confianza, o despojar a alguien de su posesión.\n\n⚖️ **Pena:** 2 a 5 años. Si es agravada (organizada), sube hasta 12 años."
    },
    {
        "tema": "Estafa",
        "keywords": ["estafa", "engaño", "cuento", "dinero falso", "fraude", "piramide"],
        "respuesta": "🤥 **Estafa (Art. 196 CP):**\n\nInducir a error a otra persona para obtener un beneficio económico indebido.\n\n⚖️ **Pena:** 1 a 6 años de privación de libertad."
    },
    {
        "tema": "Robo vs Hurto (General)",
        "keywords": ["robo", "hurto", "celular", "cartera", "billetera", "sin darme cuenta"],
        "respuesta": "👮 **Diferencia Robo vs Hurto:**\n\n* **Hurto (Art. 185):** Tomar algo ajeno **SIN violencia** (ej: te sacan la billetera sin que sientas). Pena: 1-3 años.\n* **Robo (Art. 188):** Tomar algo usando **violencia o amenaza** (ej: te empujan o amenazan). Pena: 3-8 años."
    },

    # ==================== FAMILIA Y CIVIL ====================
    {
        "tema": "Alimentos (Pensión)",
        "keywords": ["alimentos", "pension", "manutencion", "hijo", "papa no paga", "comida"],
        "respuesta": "🍎 **Pensión de Alimentos:**\n\nDerecho de los hijos hasta los **28 años** (si siguen estudios exitosos). Cubre sustento, vivienda, vestido, educación, salud y recreación.\n\n⚠️ **Si no paga:** El padre puede ir a la cárcel por el delito de Omisión a la Asistencia Familiar."
    },
    {
        "tema": "Divorcio",
        "keywords": ["divorcio", "separacion", "infidelidad", "adulterio", "casado"],
        "respuesta": "💔 **Divorcio (Código Civil):**\n\nCausales (Art. 333): Adulterio, violencia, atentado contra la vida, injuria grave, abandono (2 años), conducta deshonrosa, uso de drogas.\n\n✅ **Divorcio Rápido:** Si hay mutuo acuerdo y llevan 2 años casados, pueden ir a la Municipalidad o Notaría."
    },
    {
        "tema": "Herencia y Testamento",
        "keywords": ["herencia", "fallecio", "muerto", "sucesion", "testamento", "bienes"],
        "respuesta": "📜 **Derecho de Sucesiones:**\n\nSi no hay testamento, se hace una **Sucesión Intestada**. Heredan en orden excluyente:\n1. Hijos y demás descendientes.\n2. Padres y ascendientes.\n3. Cónyuge (hereda como un hijo más).\n4. Hermanos."
    },
    {
        "tema": "Tenencia de Hijos",
        "keywords": ["tenencia", "custodia", "con quien se queda el hijo", "visitas", "regimen"],
        "respuesta": "👶 **Tenencia y Custodia:**\n\nSi los padres se separan, se decide quién vive con el menor (Tenencia). El otro padre tiene derecho a un **Régimen de Visitas**.\n\n*Principio:* Siempre se busca el 'Interés Superior del Niño'."
    },
    
    # ==================== LABORAL ====================
    {
        "tema": "Despido Arbitrario",
        "keywords": ["despido", "me botaron", "echaron", "sin causa", "arbitrario"],
        "respuesta": "🚫 **Despido Arbitrario:**\n\nSi te despiden sin causa justa comprobada, tienes derecho a una indemnización.\n💰 **Cálculo:** 1.5 sueldos por cada año trabajado (Tope de 12 sueldos)."
    },
    {
        "tema": "Beneficios Sociales (CTS/Grati)",
        "keywords": ["cts", "gratificacion", "vacaciones", "liquidación", "beneficios"],
        "respuesta": "👷 **Beneficios Sociales:**\n\n* **CTS:** Fondo de seguro desempleo (se deposita en Mayo y Noviembre).\n* **Gratificación:** Un sueldo extra en Julio y Diciembre (si estás en planilla completa).\n* **Vacaciones:** 30 días pagados por año trabajado."
    },
    {
        "tema": "Mujer Embarazada (Trabajo)",
        "keywords": ["embarazada", "gestante", "despido embarazada", "lactancia", "licencia maternidad"],
        "respuesta": "🤰 **Protección a la Madre Trabajadora:**\n\n* **Despido Nulo:** Está prohibido despedir a una trabajadora por embarazo o lactancia.\n* **Licencia:** Tienes derecho a 98 días de descanso (49 pre y 49 post natal).\n* **Lactancia:** 1 hora diaria de permiso para dar de lactar hasta que el bebé cumpla 1 año."
    },

    # ==================== DELITOS INFORMÁTICOS ====================
    {
        "tema": "Delitos Informáticos (Hackeo)",
        "keywords": ["hackear", "contraseña", "cibernetico", "informatico", "robo de datos", "acceso ilicito"],
        "respuesta": "💻 **Delitos Informáticos (Ley 30096):**\n\n* **Acceso Ilícito:** Entrar a sistemas privados (Pena 1-4 años).\n* **Atentado a la integridad de datos:** Borrar o alterar archivos ajenos (Pena 3-6 años).\n* **Tráfico de datos:** Comercializar bases de datos robadas (Pena 3-8 años)."
    },
    {
        "tema": "Difusión de Imágenes Íntimas",
        "keywords": ["pack", "fotos intimas", "video intimo", "nudes", "difundir", "chantaje sexual"],
        "respuesta": "📸 **Difusión de Imágenes Íntimas (Art. 154-B CP):**\n\nDifundir imágenes o audios de contenido sexual de una persona sin su consentimiento es delito.\n⚖️ **Pena:** 2 a 5 años de cárcel. Si eras pareja de la víctima, la pena sube (3 a 6 años)."
    },

    # ==================== TRÁNSITO Y POLICÍA ====================
    {
        "tema": "Conducción Ebria",
        "keywords": ["ebrio", "borracho", "alcohol", "pico de botella", "manejar tomado"],
        "respuesta": "🍺 **Peligro Común (Conducción en ebriedad):**\n\nLímite legal: 0.5 g/litro de sangre (particular) o 0.25 (público).\n⚖️ **Sanción:** Multa, cancelación del brevete y pena privativa de libertad no mayor de 2 años."
    },
    {
        "tema": "Intervención Policial (DNI)",
        "keywords": ["policia", "tombo", "dni", "detencion", "control de identidad", "comisaria"],
        "respuesta": "👮 **Control de Identidad:**\n\nLa policía puede pedirte DNI en la vía pública. Si no lo tienes, pueden llevarte a la comisaría para identificarte (máximo 4 horas). No pueden encerrarte en un calabozo por esto, solo es para fines de identificación."
    },
    {
        "tema": "Coima / Corrupción",
        "keywords": ["coima", "soborno", "corrupcion", "policia plata", "cohecho"],
        "respuesta": "💸 **Cohecho (Coima):**\n\n* **El que recibe (Policía/Funcionario):** Cohecho Pasivo (Pena 5-8 años).\n* **El que da (Ciudadano):** Cohecho Activo (Pena 4-6 años). ¡Cuidado! Ofrecer dinero a un policía es delito flagrante y vas detenido al instante."
    },
    
    # ==================== CONSUMIDOR Y OTROS ====================
    {
        "tema": "Defensa del Consumidor (Indecopi)",
        "keywords": ["indecopi", "reclamo", "libro de reclamaciones", "garantia", "producto defectuoso"],
        "respuesta": "🛒 **Derechos del Consumidor (Indecopi):**\n\nTienes derecho a productos idóneos. Si fallan, tienes derecho a la garantía (reparación, cambio o devolución). El proveedor debe tener Libro de Reclamaciones (físico o virtual) y responder en máximo 15 días hábiles."
    },
    {
        "tema": "Inquilinos y Alquiler",
        "keywords": ["inquilino", "alquiler", "renta", "desalojo", "no paga alquiler"],
        "respuesta": "🏠 **Arrendamiento y Desalojo:**\n\nSi el inquilino debe **2 meses y 15 días** de renta, puedes resolver el contrato.\n* **Desalojo Notarial:** Ley express que permite desalojar rápido si el contrato tiene cláusula de allanamiento y está legalizado ante Notario."
    },
    {
        "tema": "Defensa Propia (General)",
        "keywords": ["defensa propia", "legitima defensa", "me defendi"],
        "respuesta": "🛡️ **Legítima Defensa (Art. 20 CP):**\n\nNo hay pena si te defiendes de una agresión real e inminente, usando un medio racional para impedirla. La ley presume legalidad si te defiendes de un intruso dentro de tu casa."
    },
     {
        "tema": "Saludos",
        "keywords": ["hola", "buenos dias", "buenas", "que tal", "inicio"],
        "respuesta": "¡Hola! Soy **JurisBot AI**.\n\nHe sido entrenado con la legislación peruana. Pregúntame sobre:\n- 🚓 **Penal:** Robos, Homicidios, Extorsión, Feminicidio.\n- 🏠 **Familia:** Alimentos, Divorcio, Herencia.\n- 👷 **Laboral:** Despidos, CTS, Embarazo.\n- 💻 **Digital:** Hackeo, Difusión de fotos."
    }
]

# --- LÓGICA DE BÚSQUEDA "INTELIGENTE" ---
def buscar_respuesta_simulada(pregunta_usuario):
    pregunta_usuario = pregunta_usuario.lower()
    
    # Simulación de IA pensando (fake loading)
    with st.spinner('🧠 Analizando jurisprudencia y leyes peruanas...'):
        time.sleep(1.5) # Retraso de 1.5 segundos para parecer que "piensa"
    
    # Algoritmo de búsqueda jerárquica
    for tema in BASE_CONOCIMIENTO:
        for palabra in tema["keywords"]:
            if palabra in pregunta_usuario:
                return tema["respuesta"]
    
    # Respuesta por defecto si no entiende
    return "🤖 **Lo siento.** Mi base de datos jurídica no reconoce ese término exacto.\n\nIntenta reformular tu pregunta usando términos legales comunes como: *'robo', 'despido', 'alimentos', 'divorcio', 'extorsión' o 'accidente'*."

# --- INTERFAZ GRÁFICA ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Coat_of_arms_of_Peru_%28State_flag%29_-_variant.svg/1200px-Coat_of_arms_of_Peru_%28State_flag%29_-_variant.svg.png", width=100)
    st.title("JurisBot AI")
    st.write("**Versión:** 2.4 (Enterprise)")
    st.success("🟢 Sistema Operativo")
    st.info("Este sistema utiliza procesamiento de lenguaje natural para asistir en consultas de Derecho Peruano.")
    
    # Un botón falso para que parezca más pro
    st.write("---")
    if st.button("🔄 Reiniciar Motor de IA"):
        st.cache_data.clear()
        st.rerun()

st.title("⚖️ JurisBot Perú: Sistema Experto")
st.markdown("*Asistente Legal Automatizado basado en el Código Penal y Civil del Perú.*")

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Input de usuario
if prompt := st.chat_input("Escribe tu consulta legal (Ej: ¿Qué pasa si manejo ebrio?)"):
    # 1. Mostrar usuario
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Buscar respuesta (con efecto de carga)
    respuesta_bot = buscar_respuesta_simulada(prompt)

    # 3. Mostrar respuesta bot
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_bot})
    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)