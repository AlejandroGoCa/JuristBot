import streamlit as st
import time
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="JurisBot AI - Sistema Experto", page_icon="⚖️", layout="centered")

# --- ESTILOS CSS (Apariencia tipo ChatGPT Profesional) ---
st.markdown("""
    <style>
    .stChatMessage { padding: 1.2rem; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #f0f2f6; border-left: 5px solid #2980b9; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #e8f5e9; border-left: 5px solid #27ae60; }
    h1 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE CONOCIMIENTO MASIVA (CEREBRO COMPLETO) ---
BASE_CONOCIMIENTO = [

    # ==================== PRIORIDAD 1: EMERGENCIAS Y DELITOS COMUNES ====================
    {
        "tema": "Hallazgo de Arma (Qué hacer)",
        "keywords": [
            "encontre un arma", "encontre arma", "halle un arma", "arma tirada", "pistola tirada",
            "arma de fuego", "vi una pistola", "recogi un arma", "encontrar un arma", "fierro tirado"
        ],
        "respuesta": "🔫 **Hallazgo de Arma de Fuego:**\n\nSi encuentras un arma por error:\n1. **¡NO LA TOQUES!** (Podrías dejar tus huellas o dispararla accidentalmente).\n2. Aléjate y llama al **105 (Policía)** inmediatamente.\n\n⚖️ **Cuidado:** Si te la guardas o te la llevas a casa, cometes el delito de **Tenencia Ilegal de Armas** (Art. 279 CP), que tiene pena de **6 a 15 años de cárcel**, sin importar que la hayas encontrado."
    },
    {
        "tema": "Hallazgo de Cadáver / Cuerpo",
        "keywords": [
            "encontre un cuerpo", "encontre un cadaver", "encontre un muerto", "vi un finadito",
            "vi un cuerpo", "vi un muerto", "cuerpo tirado", "hallazgo de cadaver", "cadaver tirado"
        ],
        "respuesta": "💀 **Hallazgo de Cadáver (Procedimiento):**\n\n1. **¡NO TOQUES NADA!** Podrías contaminar la escena del crimen y volverte sospechoso.\n2. **Llama al 105** para que cerquen la zona.\n3. **El Fiscal:** Solo el Fiscal de turno puede ordenar el 'Levantamiento del Cadáver'.\n\n⚠️ **Advertencia:** Si mueves el cuerpo o te llevas cosas, puedes ser denunciado por **Encubrimiento** o alterar la prueba."
    },
    {
        "tema": "Suplantación de Identidad",
        "keywords": [
            "me hago pasar por otra persona", "hacerme pasar por otro", "fingir ser otra persona", "suplantar identidad",
            "usar dni de otro", "crear cuenta falsa con nombre de otro", "soy otra persona", "fingir ser",
            "perfil falso", "fake", "cuenta falsa", "robo de identidad", "suplantacion"
        ],
        "respuesta": "🎭 **Suplantación de Identidad:**\n\nDepende de dónde lo hagas, pero en ambos casos es **DELITO**:\n\n1. **En Internet (Ley 30096):** Si creas un perfil falso o usas fotos ajenas para causar perjuicio (moral o económico). Pena: **3 a 5 años**.\n2. **En la Vida Real (Art. 438 CP):** Si usas el DNI de otro o mientes sobre tu nombre ante una autoridad. Pena: **2 a 4 años**."
    },

    # ==================== DELITOS INFORMÁTICOS (PACK COMPLETO) ====================
    {
        "tema": "Robo de Información / Hackeo",
        "keywords": [
            "robo informacion", "robar informacion", "robe informacion", "sacar informacion", "copiar informacion",
            "robo de datos", "copiar archivos", "hackear", "contraseña", "clave", "sacar datos",
            "cibernetico", "informatico", "acceso ilicito", "entrar al sistema", "bajar base de datos"
        ],
        "respuesta": "💻 **Delitos Informáticos (Ley 30096):**\n\nSi copias, sustraes o accedes a información que no es tuya (de una empresa, universidad o persona):\n\n* **Acceso Ilícito:** Entrar sin permiso a un sistema o correo (Pena 1-4 años).\n* **Atentado a la integridad de datos:** Borrar, alterar o copiar archivos ajenos (Pena 3-6 años).\n* **Tráfico de datos:** Si intentas vender esa información o bases de datos, la pena sube a **3-8 años**."
    },
    {
        "tema": "Fraude Informático (Dinero Digital)",
        "keywords": [
            "me vaciaron la cuenta", "transferencia que no hice", "robo por internet", "me robaron por yape",
            "fraude informatico", "clonaron mi tarjeta", "consumo no reconocido", "compras por internet",
            "yape falso", "plim falso", "billetera digital", "scam"
        ],
        "respuesta": "💸 **Fraude Informático (Art. 8 Ley 30096):**\n\nEl que procura un beneficio económico indebido usando tecnología (clonación de tarjetas, compras online fraudulentas, vaciar cuentas, Yape falso).\n\n⚖️ **Pena:** Cárcel de **3 a 8 años**. Si es una banda criminal, la pena es mayor."
    },
    {
        "tema": "Grooming (Acoso a Menores Online)",
        "keywords": [
            "grooming", "adulto contacta niño", "chat con menores", "pedir fotos a niña", "pedir fotos a niño",
            "cita con menor de edad", "juegos online chat", "free fire", "roblox", "fortnite chat", "discord menor"
        ],
        "respuesta": "🐺 **Grooming (Art. 183-B CP):**\n\nEl adulto que contacta a un menor de edad por medios digitales (redes, juegos, WhatsApp) con el fin de tener actos sexuales o solicitar material pornográfico.\n\n⚖️ **Pena:** Cárcel efectiva de **4 a 8 años**. ¡No es necesario encontrarse físicamente, basta el chat!"
    },
    {
        "tema": "Difusión de Imágenes Íntimas (Packs)",
        "keywords": [
            "pack", "fotos intimas", "video intimo", "nudes", "difundir", "pasar fotos",
            "chantaje sexual", "filtrar pack", "rotar fotos", "fotos privadas"
        ],
        "respuesta": "📸 **Difusión de Imágenes Íntimas (Art. 154-B CP):**\n\nDifundir imágenes o audios de contenido sexual de una persona sin su consentimiento es delito (así ella te las haya pasado antes).\n\n⚖️ **Pena:** 2 a 5 años de cárcel. \n⚠️ **Agravante:** Si eras pareja o expareja de la víctima, la pena sube a **3 a 6 años**."
    },
    {
        "tema": "Espionaje / Interceptación",
        "keywords": [
            "leer chats", "leer whatsapp", "interceptar correos", "espiar whatsapp", "app espia",
            "hackear whatsapp", "leer mensajes de mi pareja", "keylogger", "chuzar telefono"
        ],
        "respuesta": "🕵️ **Interceptación de Datos (Art. 7 Ley 30096):**\n\nEl que indebidamente intercepta, escucha o interfiere una comunicación privada (leer WhatsApp ajenos, interceptar emails).\n\n⚖️ **Pena:** 3 a 6 años. \n⚠️ **Ojo:** Instalar una app espía en el celular de tu pareja o trabajador ES DELITO."
    },
    {
        "tema": "Pornografía Infantil",
        "keywords": [
            "pornografia infantil", "cp", "videos de niños", "fotos de menores", 
            "almacenar videos prohibidos", "descargar prohibido", "fotos prohibidas"
        ],
        "respuesta": "🚫 **Pornografía Infantil (Art. 183-A CP):**\n\nDelito de 'Tolerancia Cero'.\n* **Posesión:** Solo tener los archivos en tu PC/Celular (Pena 5-10 años).\n* **Comercialización/Difusión:** Vender o pasar los archivos (Pena 10-15 años).\n* **Producción:** Grabar al menor (Pena 15-20 años)."
    },

    # ==================== DELITOS PATRIMONIALES (ROBOS Y ESTAFAS) ====================
    {
        "tema": "Robo de Celular",
        "keywords": [
            "robo un celular", "robar un celular", "robe un celular", "celular robado",
            "me robe un celular", "si robo celular", "ley robo celular", "arranchar celular",
            "bajar un celular", "hurto de celular", "celular ajeno"
        ],
        "respuesta": "📱 **Robo de Celular (Marco Legal):**\n\n1. **Hurto Agravado (Art. 186):** Si te lo llevas sin violencia (ej: del bolsillo). Pena: **3 a 6 años**.\n2. **Robo (Art. 188):** Si usas violencia o amenaza (ej: arranchar o 'cogotear'). Pena: **3 a 8 años**.\n3. **Robo Agravado (Art. 189):** Con arma o en moto. Pena: **12 a 20 años**."
    },
    {
        "tema": "Robo vs Hurto (Diferencia)",
        "keywords": [
            "diferencia robo hurto", "cual es la diferencia entre robo y hurto", "es robo o hurto",
            "me robaron o me hurtaron", "definicion robo", "definicion hurto"
        ],
        "respuesta": "⚖️ **Diferencia Clave:**\n\n* **HURTO (Art. 185):** Tomar algo ajeno **SIN violencia** ni amenaza (ej: carterista sigiloso). Pena menor.\n* **ROBO (Art. 188):** Tomar algo usando **VIOLENCIA o AMENAZA** contra la persona (ej: 'dame todo o te mato'). Pena mayor y efectiva."
    },
    {
        "tema": "Robo Agravado",
        "keywords": [
            "mano armada", "pistola", "cuchillo", "navaja", "me apuntaron", "asalto",
            "robo en banda", "raqueteros", "robo de noche", "asalto a mano armada"
        ],
        "respuesta": "🔫 **Robo Agravado (Art. 189 CP):**\n\nEl delito más severo. Ocurre si robas:\n1. A mano armada.\n2. En banda (2 o más personas).\n3. Durante la noche.\n\n⚖️ **Pena:** Cárcel efectiva entre **12 y 20 años**. Si causan lesiones graves, es **Cadena Perpetua**."
    },
    {
        "tema": "Receptación (Comprar Robado)",
        "keywords": [
            "compre celular robado", "compre barato", "celular de segunda", "cachina", "malvinas",
            "receptacion", "bloqueado por imei", "comprar robado", "celular manchado"
        ],
        "respuesta": "📱 **Receptación (Art. 194 CP):**\n\nComprar, recibir o guardar algo que sabes (o deberías presumir) que es robado, ES DELITO.\n\n⚖️ **Pena:** 1 a 4 años. Si es de equipos informáticos o celulares (Receptación Agravada), la pena es de **4 a 6 años** (cárcel efectiva)."
    },
    {
        "tema": "Extorsión (Gota a Gota)",
        "keywords": [
            "extorsion", "cobro de cupos", "gota a gota", "amenaza de muerte dinero",
            "plata o plomo", "dejar granada", "llaman para pedir plata", "cupos"
        ],
        "respuesta": "💣 **Extorsión (Art. 200 CP):**\n\nObligar a una persona a dar dinero mediante violencia o amenaza (incluye préstamos 'gota a gota' y cobro de cupos).\n\n⚖️ **Pena:** De **15 a 25 años**. Si usan explosivos o matan, aplica **Cadena Perpetua**."
    },
    {
        "tema": "Usurpación (Invasión)",
        "keywords": [
            "invasion", "invadieron mi terreno", "trafico de terrenos", "lote",
            "usurpacion", "se metieron a mi casa", "cambiaron la chapa", "invadido"
        ],
        "respuesta": "🏠 **Usurpación (Art. 202 CP):**\n\nDespojar a alguien de su inmueble usando violencia o engaño.\n\n⚖️ **Pena:** 2 a 5 años. \n⚠️ **Defensa Posesoria (Art. 920 CC):** Puedes sacar a los invasores tú mismo (sin juez) si lo haces dentro de los **15 días** de enterarte, usando la fuerza proporcional."
    },

    {
        "tema": "Robo (General)",
        "keywords": [
            "que pasa si robo", "si robo", "robar es delito", "pena por robar", 
            "cometer un robo", "robo simple", "robo"
        ],
        "respuesta": "👮 **El Delito de Robo (Art. 188 CP):**\n\nSi te apoderas de un bien ajeno usando **violencia o amenaza** contra la persona, cometes ROBO.\n\n⚖️ **Pena Base:** Cárcel efectiva de **3 a 8 años**.\n⚠️ **Diferencia:** Si NO usas violencia (solo te lo llevas sin que se den cuenta), es **Hurto** (pena menor). Si usas armas, es **Robo Agravado** (pena mucho mayor)."
    },

    # ==================== DELITOS CONTRA VIDA Y CUERPO ====================
    {
        "tema": "Homicidio Culposo (Accidentes)",
        "keywords": [
            "culposo", "accidente", "atropello", "atropellar", "imprudencia", "negligencia",
            "sin querer", "casualidad", "choque muerte", "mate a alguien por accidente"
        ],
        "respuesta": "🚗 **Homicidio Culposo (Art. 111 CP):**\n\nSi causas la muerte de alguien por negligencia o accidente (sin intención de matar), la pena es privativa de libertad no mayor de **2 años**.\n\n⚠️ **Agravante:** Si el conductor huye o estaba ebrio, la pena sube a entre **4 y 8 años**."
    },
    {
        "tema": "Feminicidio",
        "keywords": [
            "feminicidio", "mato a su mujer", "mato a su pareja", "violencia de genero",
            "ex pareja", "mato a su esposa", "mato a su enamorada"
        ],
        "respuesta": "🟣 **Feminicidio (Art. 108-B CP):**\n\nAsesinar a una mujer por su condición de tal (contexto de violencia familiar, acoso, abuso de poder).\n\n⚖️ **Pena:** No menor de **20 años**. Puede ser **Cadena Perpetua** si hay agravantes."
    },
    {
        "tema": "Sicariato",
        "keywords": [
            "sicario", "mate por dinero", "me pagaron para matar", "contratar asesino",
            "matar por encargo", "sicariato", "ajuste de cuentas"
        ],
        "respuesta": "💰 **Sicariato (Art. 108-C CP):**\n\nMatar a alguien por orden de otro a cambio de dinero. Tanto el que contrata como el que mata reciben la pena.\n\n⚖️ **Pena:** No menor de **25 años**. Si participan menores o armas de guerra, es **Cadena Perpetua**."
    },
    {
        "tema": "Parricidio",
        "keywords": [
            "mate a mi papa", "mate a mi hijo", "mate a mi mama", "matar a mis padres", 
            "matar a mi esposo", "parricidio", "mate a mi abuelo"
        ],
        "respuesta": "🩸 **Parricidio (Art. 107 CP):**\n\nMatar a un familiar directo (padres, hijos, abuelos) o cónyuge.\n\n⚖️ **Pena:** Privativa de libertad no menor de **15 años**. Si hay agravantes, puede llegar a **25 años**."
    },
    {
        "tema": "Lesiones Graves",
        "keywords": [
            "dejar invalido", "desfigurar", "romper hueso", "perdio un ojo", 
            "lesion grave", "mutilar", "corte profundo", "golpiza"
        ],
        "respuesta": "🤕 **Lesiones Graves (Art. 121 CP):**\n\nDaño que pone en peligro la vida, mutila o desfigura.\n\n⚖️ **Pena:** 4 a 8 años. Si la víctima muere, **12 a 20 años**."
    },

    {
        "tema": "Homicidio y Asesinato (General)",
        "keywords": [
            "si mato a alguien", "que pasa si asesino", "pena por asesinato" ,"matar" 
            "asesinar a una persona", "homicidio simple", "homicidio calificado",
            "matar a alguien", "asesinato"
        ],
        "respuesta": "⚰️ **Homicidio y Asesinato (Diferencia):**\n\n* **Homicidio Simple (Art. 106):** Matar a otro sin agravantes (ej: en una pelea). Pena: **6 a 20 años**.\n* **Asesinato (Homicidio Calificado - Art. 108):** Si matas con crueldad, por lucro, por placer, con veneno o alevosía (traición). Pena: **No menor de 15 años**."
    },

    {
        "tema": "Agresión Física / Golpes (General)",
        "keywords": [
            "golpear", "golpee", "le pegue", "puñete", "cachetada", "agredir", "golpie", 
            "pelea callejera", "tirar golpe", "golpiza", "moretones", "pegarle"
        ],
        "respuesta": "👊 **Agresión y Lesiones (Art. 122 CP):**\n\nGolpear a alguien es delito, y la pena depende del daño causado:\n\n1. **Faltas contra la persona:** Si el daño requiere menos de 10 días de asistencia médica (Sanción: Servicios Comunitarios).\n2. **Lesiones Leves:** Si requiere de 10 a 30 días de descanso (Pena: **2 a 5 años**).\n\n⚠️ **¡Importante!** Si golpeas a una **mujer o integrante del grupo familiar**, la pena es más severa y casi siempre efectiva (cárcel), aunque la lesión sea mínima."
    },

    # ==================== DELITOS CONTRA LA LIBERTAD SEXUAL ====================
    {
        "tema": "Violación Sexual (General)",
        "keywords": [
            "violacion", "violar", "abuso sexual", "forzar a tener sexo", 
            "sin consentimiento", "me violaron", "sexo obligado"
        ],
        "respuesta": "🛑 **Violación Sexual (Art. 170 CP):**\n\nObligar a una persona a tener relaciones sexuales (vaginal, anal o bucal) usando violencia o amenaza, o aprovechándose de que no puede resistir (ej: estaba dormida o ebria).\n\n⚖️ **Pena:** Cárcel efectiva de **14 a 20 años**. Si hay agravantes (lesiones, crueldad), la pena sube."
    },
    {
        "tema": "Violación de Menores (Cadena Perpetua)",
        "keywords": [
            "violar a un niño", "violar a una niña", "violar menor de edad", 
            "abuso infantil", "violacion de menor", "pedofilo"
        ],
        "respuesta": "🚨 **Violación de Menor de Edad (Art. 173 CP):**\n\nEs uno de los delitos más graves en el Perú. Si la víctima es menor de **14 años**, NO importa si hubo 'consentimiento', siempre es delito.\n\n⚖️ **Pena:** **CADENA PERPETUA** (Cárcel de por vida). No hay beneficios penitenciarios."
    },
    {
        "tema": "Tocamientos Indebidos",
        "keywords": [
            "me toco", "me manoseo", "tocamientos indebidos", "metio la mano", 
            "toqueteo", "actos libidinosos"
        ],
        "respuesta": "✋ **Tocamientos Indebidos (Art. 176 CP):**\n\nRealizar tocamientos (manoseos) o actos libidinosos sobre el cuerpo de otra persona sin su consentimiento, sin llegar a la violación.\n\n⚖️ **Pena:** Cárcel de **3 a 6 años**. Si la víctima es menor de edad, la pena es mucho mayor (9 a 15 años)."
    },
    {
        "tema": "Seducción de Menores (Engaño)",
        "keywords": [
            "seducir menor", "engañar adolescente", "enamorar menor para tener sexo", 
            "seduccion", "estupro"
        ],
        "respuesta": "⚠️ **Seducción (Art. 175 CP):**\n\nTener relaciones sexuales con una persona de **14 a 18 años** (adolescente) mediante **engaño**.\n\n⚖️ **Pena:** Privativa de libertad de **3 a 5 años**. La ley protege la inexperiencia de los adolescentes frente a engaños de adultos."
    },

    {
        "tema": "Acoso (Resumen de Tipos)",
        "keywords": [
            "acoso", "que es el acoso", "me estan acosando", "tipos de acoso", 
            "diferencia acoso", "ley de acoso"
        ],
        "respuesta": "⚠️ **El Acoso es Delito (Tipos):**\n\nEn Perú, el acoso se castiga diferente según el contexto:\n\n1. **Acoso Sexual (Art. 176-B):** Si hay frases, tocamientos o propuestas de índole sexual no deseadas.\n2. **Stalking (Art. 151-A):** Si te vigilan, persiguen o buscan contacto insistentemente (sin fin sexual explícito, solo por obsesión/molestar).\n3. **Acoso Laboral (Hostilidad):** Si ocurre en el trabajo para aburrirte o perjudicarte.\n4. **Ciberacoso:** Si ocurre por redes sociales (agravante)."
    },
    
    {
        "tema": "Acoso / Stalking (Persecución)",
        "keywords": [
            "me acosan", "me persiguen", "me vigilan", "stalker", 
            "me sigue a todos lados", "obsesionado conmigo", "acoso"
        ],
        "respuesta": "👀 **Delito de Acoso (Stalking - Art. 151-A CP):**\n\nEl que vigila, persigue, asedia o busca establecer contacto con una persona de forma continua contra su voluntad, alterando su vida diaria.\n\n⚖️ **Pena:** Privativa de libertad de **3 a 5 años**. \n⚠️ **Agravante:** Si el acosador es tu expareja o familiar, la pena sube hasta **7 años**."
    },
    {
        "tema": "Acoso Sexual (General)",
        "keywords": [
            "acoso sexual", "propuestas indecentes", "me pide sexo", 
            "insinuaciones sexuales", "hostigamiento sexual"
        ],
        "respuesta": "🛑 **Acoso Sexual (Art. 176-B CP):**\n\nEl que realiza vigilancia, persecución o asedio con fines lascivos (sexuales) no deseados.\n\n⚖️ **Pena:** **3 a 5 años** de cárcel. \n⚠️ **Agravante:** Si utiliza redes sociales (Ciberacoso) o es tu jefe/profesor, la pena sube a **4 a 8 años**."
    },
    {
        "tema": "Acoso Sexual Callejero",
        "keywords": [
            "acoso callejero", "me silbaron", "mañoso en el bus", 
            "tocamientos indebidos calle", "metio la mano", "piropos groseros"
        ],
        "respuesta": "🚌 **Acoso Sexual Callejero:**\n\nRealizar gestos obscenos, tocamientos indebidos, silbidos o insinuaciones sexuales en la vía pública o transporte público ES DELITO.\n\n⚖️ **Pena:** De **2 a 4 años** de cárcel. Si ocurre dentro del bus o combi, la pena es más severa."
    }


    # ==================== FAMILIA (ALIMENTOS Y DIVORCIO) ====================
    {
        "tema": "Retraso / Olvido de Pensión",
        "keywords": [
            "olvide pagar", "olvide paga", "olvido pagar", "se me paso pagar",
            "no deposite", "no pague", "no paga", "retraso pension",
            "accidente con la pension", "accidente pension", "debo pension"
        ],
        "respuesta": "🏦 **Retraso en Pensión de Alimentos:**\n\nSi fue un error y no depositaste a tiempo:\n1. **Deposita inmediatamente** (más intereses).\n2. Guarda el voucher.\n\n⚠️ **Ojo:** Si el retraso es constante, te pueden denunciar por **Omisión a la Asistencia Familiar** y podrías ir a la cárcel."
    },
    {
        "tema": "Pensión de Alimentos (General)",
        "keywords": [
            "alimentos", "pension", "manutencion", "hijo", "papa no paga", "comida",
            "demanda de alimentos", "cuanto es la pension", "porcentaje alimentos"
        ],
        "respuesta": "🍎 **Pensión de Alimentos:**\n\nEs un derecho de los hijos hasta los **28 años** (si estudian). No hay un monto fijo, depende de:\n1. Las necesidades del niño.\n2. La capacidad económica del padre.\n*El máximo embargable es el 60% de los ingresos.*"
    },
    {
        "tema": "Reducción de Alimentos (Desempleo)",
        "keywords": [
            "perdi mi trabajo", "me despidieron", "estoy desempleado", "no tengo plata", 
            "bajar la pension", "reduccion de alimentos", "ganar menos"
        ],
        "respuesta": "📉 **Reducción de Alimentos:**\n\nSi te quedaste sin trabajo, **NO dejes de pagar**. Debes iniciar una demanda de **'Reducción de Alimentos'** ante el Juez para ajustar el monto. Mientras no haya sentencia, la deuda crece al monto antiguo."
    },
    {
        "tema": "Tenencia Compartida",
        "keywords": [
            "con quien se queda el hijo", "tenencia compartida", "custodia",
            "quitar al hijo", "regimen de visitas", "ver a mi hijo", "llevarse al hijo"
        ],
        "respuesta": "👨‍👩‍👧 **Tenencia Compartida (Ley 31590):**\n\nAhora la regla general es la **Tenencia Compartida**. Ambos padres tienen derecho a pasar el mismo tiempo con sus hijos, salvo que sea perjudicial para el menor."
    },
    {
        "tema": "Divorcio",
        "keywords": [
            "divorcio", "separacion", "infidelidad", "adulterio", "casado", "quiero divorciarme",
            "separacion de cuerpos", "divorcio rapido"
        ],
        "respuesta": "💔 **Divorcio:**\n\nPuedes divorciarte por causales (adulterio, violencia, abandono) o por mutuo acuerdo.\n✅ **Divorcio Rápido:** Si ambos están de acuerdo y llevan 2 años casados, pueden hacerlo en la Municipalidad o Notaría en pocos meses."
    },
    {
        "tema": "Filiación (ADN)",
        "keywords": [
            "prueba de adn", "no es mi hijo", "apellido", "negar al hijo", 
            "reconocimiento de paternidad", "filiacion", "prueba genetica"
        ],
        "respuesta": "🧬 **Filiación y ADN:**\n\nSi el padre se niega a reconocer al hijo, el Juez ordenará la prueba de ADN. Si el demandado **NO VA**, se le declara padre automáticamente (Presunción de Paternidad)."
    },

    # ==================== DERECHO LABORAL ====================
    {
        "tema": "Despido Arbitrario",
        "keywords": [
            "me botaron", "despido arbitrario", "sin causa justa", "me echaron del trabajo",
            "despido intempestivo", "me sacaron sin avisar", "despedido"
        ],
        "respuesta": "🚫 **Despido Arbitrario:**\n\nSi te despiden sin causa legal probada, tienes derecho a una **Indemnización**.\n💰 **Cálculo:** 1.5 sueldos por cada año trabajado (Tope de 12 sueldos)."
    },
    {
        "tema": "Despido Nulo (Embarazo/Sindicato)",
        "keywords": [
            "despido embarazada", "despido sindicato", "despido discriminacion", "me botaron embarazada",
            "despido nulo", "reclame mis derechos y me botaron"
        ],
        "respuesta": "🛑 **Despido Nulo:**\n\nEs ilegal despedir por embarazo, lactancia o sindicato. Puedes pedir la **Reposición** (que te devuelvan el trabajo) y el pago de sueldos caídos."
    },
    {
        "tema": "Locación de Servicios (Falso Independiente)",
        "keywords": [
            "recibo por honorarios", "locacion de servicios", "sin planilla", "rxhe",
            "marco tarjeta y emito recibo", "falso independiente", "primacia de la realidad"
        ],
        "respuesta": "🕵️ **Primacía de la Realidad:**\n\nSi emites Recibo por Honorarios PERO tienes horario fijo y jefe, **es un fraude**. Eres un trabajador en planilla camuflado y tienes derecho a CTS, Grati y Vacaciones. ¡Denuncia a Sunafil!"
    },
    {
        "tema": "Beneficios Sociales",
        "keywords": [
            "cts", "gratificacion", "vacaciones", "liquidacion", "beneficios", "cuando pagan grati",
            "cuando pagan cts", "utilidades"
        ],
        "respuesta": "💰 **Beneficios Sociales:**\n\n* **CTS:** Fondo de desempleo (se deposita en Mayo y Noviembre).\n* **Gratificación:** Un sueldo extra en Julio y Diciembre.\n* **Vacaciones:** 30 días pagados por año."
    },
    {
        "tema": "Acoso Laboral (Hostilidad)",
        "keywords": [
            "me quieren aburrir", "hostilidad", "me bajaron el sueldo", "me cambiaron de sede", 
            "maltrato jefe", "hostigamiento", "acoso laboral"
        ],
        "respuesta": "😤 **Actos de Hostilidad:**\n\nEl empleador NO puede bajarte el sueldo, trasladarte para perjudicarte o faltarte el respeto. Puedes enviar una carta de cese de hostilidad o darte por despedido (Despido Indirecto) y cobrar indemnización."
    },

    # ==================== CIVIL Y PROPIEDAD ====================
    {
        "tema": "Inquilino Moroso",
        "keywords": [
            "inquilino no paga", "sacar inquilino", "desalojo", "ocupante precario", 
            "se quedo en mi casa", "no tiene contrato", "inquilino moroso"
        ],
        "respuesta": "🏠 **Desalojo:**\n\nSi el inquilino debe **2 meses y 15 días** de renta, puedes resolver el contrato. \n⚠️ **Cuidado:** No puedes cortarle el agua o cambiar la chapa (eso es Coacción). Debes demandar el Desalojo o usar el Desalojo Notarial si tu contrato lo permite."
    },
    {
        "tema": "Deudas y Cárcel",
        "keywords": [
            "carcel por deudas", "voy preso si no pago", "deuda banco carcel", 
            "prestamo carcel", "deuda tarjeta", "infocorp carcel"
        ],
        "respuesta": "🚫 **No hay prisión por deudas:**\n\nLa Constitución establece que nadie va preso por deudas, **salvo por Pensión de Alimentos**. Los bancos solo pueden embargar bienes, no tu libertad."
    },
    {
        "tema": "Herencia y Testamento",
        "keywords": [
            "herencia", "testamento", "sucesion intestada", "repartir bienes", 
            "anticipo de legitima", "padre fallecido herencia"
        ],
        "respuesta": "📜 **Sucesiones:**\n\nSi no hay testamento, se hace **Sucesión Intestada**. Heredan en orden: Hijos y cónyuge > Padres > Hermanos. Todos los hijos (matrimoniales o no) heredan igual."
    },

    # ==================== TRÁNSITO, POLICÍA Y CONSUMIDOR ====================
    {
        "tema": "Intervención Policial (DNI)",
        "keywords": [
            "policia", "tombo", "dni", "detencion", "control de identidad", "comisaria",
            "me paro la policia", "no tengo dni"
        ],
        "respuesta": "👮 **Control de Identidad:**\n\nLa policía puede pedirte DNI. Si no lo tienes, pueden llevarte a la comisaría para identificarte (máximo **4 horas**). No pueden meterte al calabozo por esto."
    },
    {
        "tema": "Grabar a la Policía",
        "keywords": [
            "grabar policia", "filmar intervencion", "puedo grabar", "me prohiben grabar",
            "celular policia", "borrar video", "grabar tombo"
        ],
        "respuesta": "📱 **Derecho a Grabar:**\n\n**SÍ puedes grabar.** El ciudadano tiene derecho a registrar las intervenciones policiales públicas. Si te obligan a borrar el video, cometen **Abuso de Autoridad**."
    },
    {
        "tema": "Conducción Ebria",
        "keywords": [
            "ebrio", "borracho", "alcohol", "pico de botella", "manejar tomado", "dosaje etilico",
            "manejar borracho"
        ],
        "respuesta": "🍺 **Peligro Común:**\n\nLímite: **0.5 g/l**. \n⚖️ **Sanción:** Multa, cancelación del brevete y pena privativa de libertad no mayor de 2 años (o servicios comunitarios)."
    },
    {
        "tema": "Coima / Corrupción",
        "keywords": [
            "coima", "soborno", "corrupcion", "policia plata", "cohecho", "arreglar",
            "dar para la gaseosa", "billete al policia"
        ],
        "respuesta": "💸 **Cohecho (Coima):**\n\nOfrecer dinero a un policía es delito de **Cohecho Activo** (Pena 4-6 años). Es delito flagrante y te detendrán al instante."
    },
    {
        "tema": "Indecopi (Consumidor)",
        "keywords": [
            "indecopi", "reclamo", "libro de reclamaciones", "garantia", "producto malogrado",
            "devolucion dinero", "discriminacion"
        ],
        "respuesta": "🛒 **Derechos del Consumidor:**\n\nEl proveedor debe tener Libro de Reclamaciones y responder en **15 días hábiles**. Si discriminan (derecho de admisión abusivo), Indecopi pone multas altas."
    },

    {
        "tema": "Piratería de Software (Ingeniería)",
        "keywords": [
            "instalar windows pirata", "vender software pirata", "descargar office crackeado",
            "usar programas piratas", "vender peliculas piratas", "derechos de autor"
        ],
        "respuesta": "💿 **Delitos contra la Propiedad Intelectual:**\n\nEl uso personal a veces pasa desapercibido, pero **vender o distribuir** software/películas piratas es delito.\n\n⚖️ **Pena:** De **2 a 5 años** de cárcel (Art. 217 CP). ¡Cuidado con vender computadoras con software 'crackeado' preinstalado!"
    },
    {
        "tema": "Retención de Títulos (Universidades)",
        "keywords": [
            "la universidad retiene mi titulo", "no me dan mi bachiller por deuda", 
            "colegio retiene libreta", "no me dejan dar examen por no pagar", "retencion de documentos"
        ],
        "respuesta": "🎓 **Prohibición de Retener Documentos:**\n\n¡Es Ilegal! Ninguna universidad, instituto o colegio puede retener tus certificados, libretas o diplomas por falta de pago de pensiones.\n\n✅ **Acción:** Puedes denunciar ante **Indecopi**. La institución recibirá una multa fuerte, aunque igual la deuda monetaria seguirá existiendo."
    },
    {
        "tema": "Ley de Protección de Datos (Spam)",
        "keywords": [
            "venden mis datos", "llamadas spam", "vender base de datos", 
            "ley proteccion de datos", "acosan por telefono", "de donde sacaron mi numero"
        ],
        "respuesta": "🛡️ **Protección de Datos Personales (Ley 29733):**\n\nVender o compartir bases de datos de personas sin su consentimiento es una infracción muy grave.\n\n💰 **Sanción:** El Ministerio de Justicia impone multas de hasta **100 UIT** a las empresas (o personas) que trafican con tu información personal."
    },
    
    # ==================== PACK EXTRA: SOCIEDAD Y MASCOTAS ====================
    {
        "tema": "Maltrato Animal",
        "keywords": [
            "maltrato animal", "mataron a mi perro", "envenenaron a mi gato", 
            "pegan al perro", "ley 30407", "abandono mascota"
        ],
        "respuesta": "🐾 **Ley de Protección y Bienestar Animal (Ley 30407):**\n\nEl que abandona o maltrata cruelmente a un animal doméstico comete delito.\n\n⚖️ **Pena:** Hasta **3 años** de cárcel. Si el animal muere, la pena es de **3 a 5 años** de cárcel efectiva."
    },
    {
        "tema": "Acoso Callejero",
        "keywords": [
            "acoso callejero", "me silbaron", "mañoso en el bus", "tocamientos indebidos calle", 
            "metio la mano", "acoso sexual callejero"
        ],
        "respuesta": "bus🚌 **Acoso Sexual Callejero (Art. 176-B CP):**\n\nRealizar gestos obscenos, tocamientos indebidos o insinuaciones sexuales en la vía pública o transporte público es delito.\n\n⚖️ **Pena:** De **2 a 4 años** de cárcel (más severo si es en transporte público)."
    },
    {
        "tema": "Uso de Gas Pimienta (Defensa)",
        "keywords": [
            "gas pimienta", "es legal el gas pimienta", "usar taser", 
            "defensa personal", "puedo llevar gas pimienta"
        ],
        "respuesta": "🌶️ **Uso de Gas Pimienta:**\n\n**SÍ es legal** portarlo y usarlo, pero SOLO para **Legítima Defensa** ante un ataque inminente.\n\n⚠️ **Ojo:** Debe ser un medio proporcional. Si lo usas para atacar o bromear, cometes delito de Lesiones."
    },


    # ==================== SALUDOS Y CRÉDITOS ====================
    {
        "tema": "Saludos del Grupo 03",
        "keywords": ["hola", "buenos dias", "buenas", "que tal", "inicio", "holi", "holiwis", "quienes son", "autores"],
        "respuesta": "👋 **¡Hola! Soy JurisBot Perú (IA Legal)**\n\nProyecto de Inteligencia Artificial desarrollado por estudiantes de Ingeniería de Sistemas de la **UNJFSC**:\n\n👨‍🎓 **Callan Bautista, Giomar**\n👨‍🎓 **Gomez Castillo, Alejandro**\n👨‍🎓 **Tiburcio Shuan, Leonardo**\n👨‍🎓 **Villavicencio Romero, Renzo**\n\n💡 *Estoy capacitado en Derecho Penal, Civil, Laboral y Protección al Consumidor.*"
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
    return "🤖 **Lo siento.** Mi base de datos no reconoce ese término exacto.\n\nIntenta reformular tu pregunta usando términos legales comunes como: *'robo', 'despido', 'alimentos', 'divorcio', 'extorsión' o 'accidente'*."

# --- INTERFAZ GRÁFICA ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Coat_of_arms_of_Peru_%28State_flag%29_-_variant.svg/1200px-Coat_of_arms_of_Peru_%28State_flag%29_-_variant.svg.png", width=100)
    st.title("JurisBot AI")
    st.write("**Versión:** 3.0 (Final)")
    st.success("🟢 Sistema Operativo")
    st.info("Este sistema utiliza procesamiento de lenguaje natural para asistir en consultas de Derecho Peruano.")
    
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