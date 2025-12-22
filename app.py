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
        "tema": "Robo de Celular (Ley Específica)",
        "keywords": [
            "robo un celular", "robar un celular", "robe un celular", 
            "me robe un celular", "si robo celular", "ley robo celular",
            "hurto de celular", "arranchar celular"
        ],
        "respuesta": "📱 **Robo de Celular (Marco Legal):**\n\nSi te apoderas de un celular ajeno, incumples estas leyes dependiendo del modo:\n\n1. **Hurto Agravado (Art. 186 CP):** Si te lo llevas sin violencia (ej: te lo encuentras o lo sacas del bolsillo sin que se den cuenta). Pena: **3 a 6 años**.\n2. **Robo (Art. 188 CP):** Si usas violencia o amenaza (ej: arranchar o amenazar). Pena: **3 a 8 años**.\n3. **Robo Agravado (Art. 189 CP):** Si usas arma o moto. Pena: **12 a 20 años**."
    },
    {
        "tema": "Diferencia General Robo/Hurto",
        "keywords": [
            "diferencia robo y hurto", "es robo o hurto", "cual es la diferencia",
            "ley robo", "ley hurto"
        ],
        "respuesta": "⚖️ **Diferencia Legal (Art. 185 vs 188 CP):**\n\n* **HURTO:** Te apoderas del bien con destreza, **SIN violencia** (ej: carteristas, tenderos). La pena es menor.\n* **ROBO:** Te apoderas del bien usando **VIOLENCIA o AMENAZA** contra la persona. La pena es mucho mayor y siempre es cárcel efectiva."
    },
    {
        "tema": "Hallazgo de Arma (Qué hacer)",
        "keywords": [
            "encontre un arma", "encontre arma", "halle un arma", "arma tirada", 
            "arma de fuego", "vi una pistola", "recogi un arma", "encontrar un arma"
        ],
        "respuesta": "🔫 **Hallazgo de Arma de Fuego:**\n\nSi encuentras un arma por error:\n1. **¡NO LA TOQUES!** (Podrías dejar tus huellas o dispararla accidentalmente).\n2. Aléjate y llama al **105 (Policía)** inmediatamente.\n\n⚖️ **Cuidado:** Si te la guardas o te la llevas a casa, cometes el delito de **Tenencia Ilegal de Armas** (Art. 279 CP), que tiene pena de **6 a 15 años de cárcel**, sin importar que la hayas encontrado."
    },

    {
        "tema": "Hallazgo de Cadáver",
        "keywords": [
            "encontre un cuerpo", "encontre un cadaver", "encontre un muerto", 
            "vi un cuerpo", "vi un muerto", "cuerpo tirado", "hallazgo de cadaver"
        ],
        "respuesta": "💀 **Hallazgo de Cadáver (Procedimiento):**\n\n1. **¡NO TOQUES NADA!** Podrías contaminar la escena del crimen y volverte sospechoso.\n2. **Llama al 105** para que cerquen la zona.\n3. **El Fiscal:** Solo el Fiscal de turno puede ordenar el 'Levantamiento del Cadáver'.\n\n⚠️ **Advertencia:** Si mueves el cuerpo o te llevas cosas, puedes ser denunciado por **Encubrimiento** o alterar la prueba (Obstrucción a la Justicia)."
    },

    {
        "tema": "Ocultamiento de Cadáver (Encubrimiento)",
        "keywords": [
            "esconder cuerpo", "ocultar cuerpo", "enterrar cuerpo", "desaparecer cuerpo", 
            "botar cuerpo", "quemar cuerpo", "tirar al rio", "esconder muerto"
        ],
        "respuesta": "⛏️ **Encubrimiento Real (Art. 405 CP):**\n\nSi ayudas a desaparecer, ocultar o alterar los rastros de un delito (como esconder un cuerpo) para dificultar la justicia:\n\n⚖️ **Pena:** Cárcel de **2 a 4 años**. \n⚠️ **Nota:** Si lo haces para proteger a un familiar muy cercano (hijo, cónyuge, padres), el juez podría eximirte de pena (Excusa Absolutoria), pero igual serás investigado."
    },
    {
        "tema": "Profanación de Tumbas / Exhumación Ilegal",
        "keywords": [
            "sacar cuerpo", "desenterrar", "abrir tumba", "profanar", "robar cadaver", 
            "cementerio", "exhumar", "sacar muerto"
        ],
        "respuesta": "⚰️ **Ofensas a la Memoria de los Muertos (Art. 318 CP):**\n\nEstá prohibido sacar un cadáver de su tumba sin autorización judicial o sanitaria.\n\n⚖️ **Pena:** El que sustrae un cadáver o profana una tumba será reprimido con **pena privativa de libertad**.\n*Si es para fines de lucro (vender el cuerpo o dientes de oro), la pena es mayor.*"
    },
    {
        "tema": "Necrofilia / Falta de Respeto",
        "keywords": [
            "sexo con cadaver", "necrofilia", "abusar cuerpo", "violar muerto", 
            "relaciones con muerto"
        ],
        "respuesta": "🛑 **Vilipendio de Cadáver (Art. 318 CP):**\n\nQuien practica actos sexuales con un cadáver (necrofilia) o lo trata de manera irrespetuosa/ultrajante comete delito contra los muertos.\n\n⚖️ **Pena:** Cárcel efectiva. La ley protege la dignidad de la persona incluso después de fallecida."
    },
  
  # ==================== PACK HOMICIDIOS Y VIDA (COMPLETO) ====================
    {
        "tema": "Parricidio (Matar familiar)",
        "keywords": [
            "mate a mi papa", "mate a mi hijo", "mate a mi mama", "matar a mis padres", 
            "matar a mi esposo", "parricidio", "mate a mi abuelo"
        ],
        "respuesta": "🩸 **Parricidio (Art. 107 CP):**\n\nMatar a un familiar directo (padres, hijos, abuelos) o al cónyuge/conviviente a sabiendas de la relación.\n\n⚖️ **Pena:** Privativa de libertad no menor de **15 años**. Si hay agravantes, puede llegar a **25 años o más**."
    },
    {
        "tema": "Homicidio por Emoción Violenta",
        "keywords": [
            "encontre a mi mujer con otro", "infidelidad flagrante", "perdi la cabeza", 
            "ataque de celos", "emocion violenta", "mate por celos", "cegado por la ira"
        ],
        "respuesta": "😡 **Homicidio por Emoción Violenta (Art. 109 CP):**\n\nCuando matas a alguien bajo un estado emocional incontrolable que rompe tus frenos inhibitorios (ej: descubrir una infidelidad en el acto).\n\n⚖️ **Pena Reducida:** Como no fue planificado, la pena es menor: de **3 a 5 años** de cárcel."
    },
    {
        "tema": "Sicariato (Matar por dinero)",
        "keywords": [
            "sicario", "mate por dinero", "me pagaron para matar", "contratar asesino", 
            "matar por encargo", "sicariato"
        ],
        "respuesta": "💰 **Sicariato (Art. 108-C CP):**\n\nMatar a alguien por orden de otro a cambio de dinero u otro beneficio. Tanto el que contrata como el que mata reciben la pena.\n\n⚖️ **Pena:** No menor de **25 años**. Si participan menores o armas de guerra, es **Cadena Perpetua**."
    },
    {
        "tema": "Instigación al Suicidio / Eutanasia",
        "keywords": [
            "ayudar a morir", "suicidio asistido", "eutanasia", "quiere suicidarse", 
            "ayudar a suicidarse", "muerte digna"
        ],
        "respuesta": "💊 **Ayuda al Suicidio (Art. 113 CP):**\n\nEn Perú, ayudar o convencer a otro para que se suicide es delito (Pena 1-4 años).\n\n⚠️ **Eutanasia:** A excepción del caso histórico de Ana Estrada (judicializado), la 'muerte piadosa' sigue siendo penalizada como **Homicidio Piadoso** (Art. 112), salvo orden judicial expresa."
    },
    {
        "tema": "Aborto (General)",
        "keywords": [
            "aborto", "abortar", "interrumpir embarazo", "pastilla abortiva", 
            "sacar al bebe", "no quiero tener al bebe"
        ],
        "respuesta": "👶 **El Aborto en el Perú:**\n\nEs ilegal y punible, salvo una excepción:\n\n✅ **Aborto Terapéutico:** Es el ÚNICO legal. Se permite solo cuando es el único medio para salvar la vida de la gestante o evitar un mal grave en su salud.\n❌ **Aborto Consentido/Sentimental:** (Incluso por violación) sigue estando tipificado como delito, aunque con penas bajas o servicio comunitario."
    },
    
    # ==================== LESIONES (GOLPES Y DAÑOS) ====================
    {
        "tema": "Lesiones Graves",
        "keywords": [
            "dejar invalido", "desfigurar", "romper hueso", "perdio un ojo", 
            "lesion grave", "mutilar", "corte profundo"
        ],
        "respuesta": "🤕 **Lesiones Graves (Art. 121 CP):**\n\nSi causas daño que pone en peligro la vida, mutila un miembro, desfigura el rostro o causa invalidez.\n\n⚖️ **Pena:** 4 a 8 años. Si la víctima muere a causa de la lesión, la pena sube a **12 a 20 años**."
    },
    {
        "tema": "Lesiones Leves / Agresión",
        "keywords": [
            "golpes", "moretones", "puñete", "cachetada", "arañones", 
            "pelea callejera", "agresion fisica"
        ],
        "respuesta": "🩹 **Lesiones Leves (Art. 122 CP):**\n\nDaños que requieren más de 10 y menos de 30 días de asistencia médica.\n\n⚖️ **Pena:** 2 a 5 años. \n⚠️ **Nota:** Si la agresión es contra una mujer (violencia de género) o un familiar, la pena siempre es efectiva y no baja de 3 años."
    },
    {
        "tema": "Exposición al Peligro / Abandono",
        "keywords": [
            "abandonar bebe", "dejar al abuelo en la calle", "exposicion al peligro", 
            "abandonar persona incapaz"
        ],
        "respuesta": "🚼 **Abandono de Personas en Peligro (Art. 125 CP):**\n\nEl que expone a peligro de muerte o abandona a un menor de edad o a una persona incapaz de valerse por sí misma (anciano enfermo).\n\n⚖️ **Pena:** 1 a 4 años. Si la persona muere por el abandono, la pena sube a **4 a 8 años**."
    },

     #TEMA DE PENSIONES
    {
        "tema": "Retraso / Olvido de Pensión",
        "keywords": [
            "olvide pagar", "olvide paga", "olvido pagar", "se me paso pagar", 
            "no deposite", "no pague", "no paga", 
            "retraso pension", "accidente con la pension", "accidente pension"
        ],
        "respuesta": "🏦 **Retraso en Pensión de Alimentos:**\n\nSi fue un error o 'accidente' y no depositaste a tiempo:\n1. **Deposita inmediatamente** (incluyendo los intereses legales).\n2. Guarda el voucher.\n\n⚠️ **Ojo:** Si esto se vuelve constante, te pueden denunciar por **Omisión a la Asistencia Familiar** y podrías ir a la cárcel, sin importar que haya sido un 'olvido'."
    },

    {
        "tema": "Me quedé sin trabajo (Reducción de Pensión)",
        "keywords": [
            "perdi mi trabajo", "me despidieron", "estoy desempleado", "no tengo plata", 
            "bajar la pension", "reduccion de alimentos", "ganar menos"
        ],
        "respuesta": "📉 **Reducción de Alimentos:**\n\nSi te quedaste sin trabajo o ganas menos, **NO dejes de pagar** (la deuda se acumula). \n\n✅ **Solución:** Debes iniciar una demanda de **'Reducción de Alimentos'** ante el Juez inmediatamente para que ajusten el monto a tu nueva realidad. Mientras no haya sentencia, la deuda sigue creciendo al monto antiguo."
    },
    {
        "tema": "Tengo más hijos (Prorrateo)",
        "keywords": [
            "tengo otro hijo", "nueva familia", "otra mujer", "mas hijos", 
            "no me alcanza para todos", "prorrateo"
        ],
        "respuesta": "⚖️ **Prorrateo de Alimentos:**\n\nSi tienes hijos con diferentes parejas y el sueldo no te alcanza, puedes pedir el **'Prorrateo'**.\n\nEl Juez dividirá tu porcentaje embargable (máximo 60% de tus ingresos) equitativamente entre todos tus hijos. Ningún hijo tiene preferencia sobre otro."
    },
    {
        "tema": "Hijo Mayor de Edad (¿Hasta cuándo?)",
        "keywords": [
            "hasta cuando se paga", "cumplio 18", "mayor de edad", "ya trabaja", 
            "hijo de 28", "exoneracion"
        ],
        "respuesta": "🎓 **¿Hasta cuándo se paga?:**\n\nLa pensión NO se corta automáticamente a los 18 años.\n\n1. **Hasta los 18:** Es obligatorio.\n2. **Hasta los 28:** Solo si el hijo sigue **estudios superiores con éxito** (notas aprobatorias).\n3. **Indefinido:** Si el hijo tiene una incapacidad física o mental permanente.\n\n⚠️ Para dejar de pagar, debes hacer un juicio de **'Exoneración de Alimentos'**."
    },
    {
        "tema": "Registro de Deudores (REDAM)",
        "keywords": [
            "redam", "infocorp alimentos", "lista de deudores", "no puedo viajar", 
            "impedimento de salida", "banco prestamo"
        ],
        "respuesta": "🚫 **REDAM (Registro de Deudores Alimentarios Morosos):**\n\nSi debes **3 cuotas** (consecutivas o alternadas), te inscriben en el REDAM.\n\n**Consecuencias:**\n- ✈️ No puedes salir del país.\n- 💳 Los bancos no te dan préstamos (te reportan a Infocorp).\n- 📄 Dificultades para contratar con el Estado."
    },
    {
        "tema": "Gastos de Embarazo",
        "keywords": [
            "estoy embarazada", "pension embarazada", "prenatal", "gastos parto", 
            "el papa no ayuda embarazo"
        ],
        "respuesta": "🤰 **Alimentos a la Madre Gestante:**\n\nNo tienes que esperar a que nazca el bebé. La madre puede demandar **'Alimentos' desde el embarazo**.\n\nEl juez ordenará que el padre pague los gastos del embarazo, parto y postparto (los primeros 60 días)."
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
# ==================== DELITOS CONTRA EL PATRIMONIO (ROBOS Y ESTAFAS) ====================
    {
        "tema": "Diferencia Hurto vs Robo",
        "keywords": [
            "diferencia robo hurto", "cual es la diferencia entre robo y hurto", 
            "es robo o hurto", "me robaron o me hurtaron"
        ],
        "respuesta": "⚖️ **Diferencia Clave (Hurto vs. Robo):**\n\n1. **Hurto (Art. 185):** Se apoderan de tus cosas **SIN violencia** ni amenaza (ej: te sacan el celular del bolsillo en el bus y no te das cuenta).\n2. **Robo (Art. 188):** Usan **violencia o amenaza** contra ti (ej: te empujan, te apuntan con arma o te dicen 'dame todo o te mato').\n\n*El Robo siempre tiene pena más alta que el Hurto.*"
    },
    {
        "tema": "Hurto Simple / Agravado",
        "keywords": [
            "me sacaron la billetera", "me sacaron el celular", "sin darme cuenta", 
            "hurto", "carterista", "tendero", "robaron mi casa vacia"
        ],
        "respuesta": "🕵️ **Hurto (Art. 185 y 186 CP):**\n\nApoderarse de un bien ajeno sin violencia.\n\n* **Hurto Simple:** Pena de 1 a 3 años.\n* **Agravado:** Si entran a tu casa cuando no estás, usan llaves falsas, rompen ventanas o lo hacen en la noche. La pena sube a **3 a 6 años**."
    },
    {
        "tema": "Robo Agravado (Mano Armada)",
        "keywords": [
            "mano armada", "pistola", "cuchillo", "navaja", "me apuntaron", 
            "robo en banda", "raqueteros", "robo de noche"
        ],
        "respuesta": "🔫 **Robo Agravado (Art. 189 CP):**\n\nEl delito patrimonial más severo. Ocurre cuando:\n1. Es a mano armada.\n2. Son 2 o más personas (banda).\n3. Ocurre durante la noche.\n\n⚖️ **Pena:** Cárcel efectiva entre **12 y 20 años**. Si causan lesiones graves a la víctima, es **Cadena Perpetua**."
    },
    {
        "tema": "Extorsión (Gota a Gota / Cupos)",
        "keywords": [
            "extorsion", "cobro de cupos", "gota a gota", "amenaza de muerte dinero", 
            "plata o plomo", "dejar granada", "llaman para pedir plata"
        ],
        "respuesta": "💣 **Extorsión (Art. 200 CP):**\n\nObligar a una persona a dar dinero mediante violencia o amenaza (incluye los préstamos 'gota a gota' y cobro de cupos en obras).\n\n⚖️ **Pena:** De **15 a 25 años**. Si usan explosivos o matan a alguien, aplica la **Cadena Perpetua**."
    },
    {
        "tema": "Usurpación (Invasión de Terrenos)",
        "keywords": [
            "invasion", "invadieron mi terreno", "trafico de terrenos", "lote", 
            "usurpacion", "se metieron a mi casa", "cambiaron la chapa"
        ],
        "respuesta": "🏠 **Usurpación (Art. 202 CP):**\n\nDespojar a alguien de su inmueble, alterar linderos o turbar la posesión usando violencia o engaño.\n\n⚖️ **Pena:** 2 a 5 años. \n⚠️ **Defensa Posesoria Extrajudicial (Art. 920 CC):** Puedes sacar a los invasores tú mismo (sin juez) si lo haces dentro de los **15 días** de enterarte, usando la fuerza proporcional y con ayuda de la Policía."
    },
    {
        "tema": "Estafa y Cuentos",
        "keywords": [
            "estafa", "me engañaron dinero", "cuento de la maleta", "pepita de oro", 
            "falso yape", "piramide", "inversion falsa"
        ],
        "respuesta": "🤥 **Estafa (Art. 196 CP):**\n\nObtener un provecho económico induciendo a error a la víctima (engaño, astucia, ardid).\n\n⚖️ **Pena:** 1 a 6 años.\n*Dato:* Si es una estafa agravada (contra muchas personas o usando documentos falsos), la pena sube hasta 8 años."
    },
    {
        "tema": "Receptación (Comprar Robado)",
        "keywords": [
            "compre celular robado", "compre barato", "celular de segunda", 
            "cachina", "malvinas", "receptacion", "bloqueado por imei"
        ],
        "respuesta": "📱 **Receptación (Art. 194 CP):**\n\n¡Cuidado! Comprar, recibir o guardar algo que sabes (o deberías saber) que es robado, ES DELITO.\n\n⚖️ **Pena:** 1 a 4 años. Si es de equipos informáticos o celulares (Receptación Agravada), la pena es de **4 a 6 años** (cárcel efectiva)."
    },
    {
        "tema": "Daños (Vandalismo)",
        "keywords": [
            "rompieron mi ventana", "rayaron mi carro", "destruyeron mi puerta", 
            "vandalismo", "romper cosas ajenas"
        ],
        "respuesta": "🔨 **Daños (Art. 205 CP):**\n\nEl que daña, destruye o inutiliza un bien ajeno.\n\n⚖️ **Pena:** Prestación de servicios comunitarios. Si el daño supera las 4 UIT o afecta bienes públicos, puede haber pena de cárcel (1 a 3 años)."
    },

    # ==================== FAMILIA Y CIVIL ====================
    # ==================== BLOQUE FAMILIA: PADRES E HIJOS ====================
    {
        "tema": "Tenencia Compartida (Nueva Ley)",
        "keywords": [
            "con quien se queda el hijo", "tenencia compartida", "custodia", 
            "quitar al hijo", "regimen de visitas", "ver a mi hijo", "llevarse al hijo"
        ],
        "respuesta": "👨‍👩‍👧 **Tenencia Compartida (Ley 31590):**\n\nEn Perú, ahora la regla general es la **Tenencia Compartida**. Ambos padres tienen derecho a pasar el mismo tiempo con sus hijos, salvo que sea perjudicial para el menor.\n\n⚠️ **Importante:** Ningún padre puede prohibir al otro ver a sus hijos (salvo orden judicial). Si la madre/padre impide las visitas, puede ser denunciado por **Sustracción de Menor** o Desobediencia a la Autoridad."
    },
    {
        "tema": "Filiación / ADN (Reconocimiento)",
        "keywords": [
            "prueba de adn", "no es mi hijo", "apellido", "negar al hijo", 
            "reconocimiento de paternidad", "filiacion", "prueba genetica"
        ],
        "respuesta": "🧬 **Filiación y ADN:**\n\nSi el padre se niega a reconocer al hijo, la madre puede demandar **Filiación Judicial**.\n\n⚖️ **La Regla de Oro:** El Juez ordenará la prueba de ADN. Si el demandado **NO VA** o se niega a hacerse la prueba, el Juez lo declarará padre automáticamente (Presunción de Paternidad) y ordenará el pago de alimentos."
    },
    {
        "tema": "Patria Potestad (Perder derechos)",
        "keywords": [
            "quitar patria potestad", "perder derechos hijo", "padre ausente", 
            "suspension patria potestad", "mal padre"
        ],
        "respuesta": "🚫 **Pérdida de Patria Potestad:**\n\nEs la sanción más grave. Un padre pierde sus derechos sobre el hijo si:\n1. Abandona al menor.\n2. Dedica al menor a la mendicidad o trabajo infantil.\n3. Es condenado por delitos graves contra el hijo.\n*Nota:* Perder la patria potestad NO te libra de pagar alimentos."
    },
    {
        "tema": "Permiso de Viaje (Menores)",
        "keywords": [
            "viaje menor", "sacar al hijo del pais", "permiso de viaje", 
            "viajar con mi hijo", "papa no firma permiso"
        ],
        "respuesta": "✈️ **Permiso de Viaje para Menores:**\n\n* **Dentro del Perú:** Si viaja con uno de los padres, basta la autorización de ese padre (salvo disposición judicial en contrario).\n* **Al Extranjero:** OBLIGATORIAMENTE se necesita la firma notarial de **ambos padres**. Si uno no quiere firmar, puedes pedir una **Autorización de Viaje Judicial** demostrando que el viaje es beneficioso para el niño."
    },

    # ==================== BLOQUE FAMILIA: PAREJA Y MATRIMONIO ====================
    {
        "tema": "Unión de Hecho (Convivencia)",
        "keywords": [
            "convivencia", "conviviente", "union de hecho", "concubina", 
            "pareja sin casarse", "derechos de conviviente", "bienes convivientes"
        ],
        "respuesta": "🏠 **Unión de Hecho (Art. 326 CC):**\n\nLa convivencia genera derechos parecidos al matrimonio si:\n1. Son hombre y mujer libres de impedimento matrimonial (solteros/divorciados).\n2. Conviven por **más de 2 años** continuos.\n\n✅ **Efecto:** Se genera una **Sociedad de Gananciales** (los bienes comprados en ese tiempo son de los dos). Para formalizarlo, deben ir al Notario o hacerlo vía judicial."
    },
    {
        "tema": "Separación de Patrimonios (Bienes Separados)",
        "keywords": [
            "bienes separados", "separacion de patrimonios", "mis cosas son mias", 
            "casarse por bienes separados", "deudas de mi esposo"
        ],
        "respuesta": "💰 **Régimen Patrimonial:**\n\nAntes de casarse (o durante el matrimonio), pueden elegir el régimen de **Separación de Patrimonios**.\n\n* **Ventaja:** Lo que tú compras es tuyo y lo que él/ella compra es suyo. Las deudas de tu pareja NO afectan tus bienes. Se debe inscribir en Registros Públicos (SUNARP)."
    },
    {
        "tema": "Divorcio por Adulterio/Infidelidad",
        "keywords": [
            "me fue infiel", "adulterio", "amante", "pruebas infidelidad", 
            "divorcio por conducta deshonrosa", "divorcio sancion"
        ],
        "respuesta": "💔 **Divorcio por Adulterio:**\n\nEs una causal válida para divorciarse, pero tiene reglas:\n1. Debes probarlo (fotos, chats, videos, hijo extramatrimonial).\n2. Tienes un plazo: Caduca a los 6 meses de enterarte o 5 años de sucedido el hecho.\n3. El cónyuge culpable pierde el derecho a heredar y podría pagar una **indemnización** por daño moral."
    },
    {
        "tema": "Violencia Familiar (Medidas de Protección)",
        "keywords": [
            "me pega", "grita", "violencia psicologica", "violencia fisica", 
            "pelea pareja", "medidas de proteccion", "denuncia mujer"
        ],
        "respuesta": "🛡️ **Violencia Familiar (Ley 30364):**\n\nCualquier agresión (física o psicológica) debe denunciarse en la Comisaría o Juzgado de Familia.\n\n✅ **Medidas de Protección:** El juez debe dictarlas en máximo **24 horas** (ej: retiro del agresor de la casa, prohibición de acercamiento). No necesitas abogado para denunciar y es gratuito."
    },

    # ==================== BLOQUE CIVIL: HERENCIAS Y SUCESIONES ====================
    {
        "tema": "Anticipo de Legítima (Herencia en Vida)",
        "keywords": [
            "herencia en vida", "adelanto de herencia", "anticipo de legitima", 
            "dar casa a hijo", "traspaso propiedad"
        ],
        "respuesta": "🎁 **Anticipo de Legítima:**\n\nEs cuando los padres donan sus bienes a los hijos en vida. \n\n⚠️ **Regla:** Nadie puede dar por vía de donación más de lo que puede disponer por testamento. Si tienes hijos/cónyuge, solo puedes regalar libremente el **un tercio** de tus bienes a extraños; el resto está reservado para tus herederos forzosos."
    },
    {
        "tema": "Testamento vs Sucesión Intestada",
        "keywords": [
            "testamento", "no dejo testamento", "sucesion intestada", 
            "declaratoria de herederos", "repartir bienes"
        ],
        "respuesta": "📜 **Sucesión Intestada:**\n\nEs el trámite más común en Perú (cuando alguien muere sin testamento). Se hace ante Notario o Juez.\n\n**Orden de herederos:**\n1. Hijos y descendientes.\n2. Padres y ascendientes.\n3. Cónyuge (Hereda junto con los hijos).\n4. Hermanos (solo si no hay los anteriores)."
    },
    {
        "tema": "Hijo no reconocido en Herencia",
        "keywords": [
            "hijo fuera del matrimonio herencia", "hijo ilegitimo", 
            "todos los hijos heredan igual", "herencia hermanos"
        ],
        "respuesta": "⚖️ **Igualdad de Hijos:**\n\nEn el Perú, **TODOS los hijos tienen los mismos derechos**, sean matrimoniales, extramatrimoniales o adoptivos. Todos heredan en partes iguales. No existe distinción legal entre ellos."
    },

    # ==================== BLOQUE CIVIL: PROPIEDAD Y VIVIENDA ====================
    {
        "tema": "Desalojo de Inquilino Precario",
        "keywords": [
            "inquilino no paga", "sacar inquilino", "desalojo", "ocupante precario", 
            "se quedo en mi casa", "no tiene contrato"
        ],
        "respuesta": "🏠 **Desalojo (Ocupante Precario):**\n\nSi alguien vive en tu propiedad sin contrato y sin pagar (o se le venció el contrato), es un 'Precario'.\n\n✅ **Pasos:**\n1. Enviar Carta Notarial invitando a conciliar.\n2. Ir a Centro de Conciliación.\n3. Si no se va, interponer demanda judicial de Desalojo.\n*Tip:* Si alquilas, usa siempre la 'Cláusula de Allanamiento Futuro' para desalojar rápido."
    },
    {
        "tema": "Prescripción Adquisitiva (Dueño por tiempo)",
        "keywords": [
            "vivio muchos años", "dueño por tiempo", "prescripcion adquisitiva", 
            "titulo de propiedad posesion", "10 años viviendo"
        ],
        "respuesta": "⏳ **Prescripción Adquisitiva de Dominio:**\n\nPuedes volverte dueño de un inmueble si lo posees de manera:\n1. Continua (sin interrupciones).\n2. Pacífica (sin violencia).\n3. Pública (todos te ven como dueño).\n\n**Plazos:**\n* **10 años:** Si no tienes justo título (mala fe).\n* **5 años:** Si tienes justo título y buena fe."
    },
    {
        "tema": "Compraventa sin Escritura",
        "keywords": [
            "minuta", "contrato privado", "solo tengo papel simple", 
            "compra venta sin notario", "escritura publica"
        ],
        "respuesta": "📝 **Seguridad Jurídica (Art. 1549 CC):**\n\nEl contrato privado es válido entre las partes, pero **NO te protege frente a terceros**. \n\n⚠️ **Riesgo:** El vendedor podría vender la misma casa a otra persona. Si esa segunda persona lo inscribe en Registros Públicos (SUNARP) primero, ella será la dueña legal aunque tú hayas comprado antes. ¡Siempre exige Escritura Pública y Registro!"
    },

    # ==================== BLOQUE CIVIL: DEUDAS Y DINERO ====================
    {
        "tema": "Prisión por Deudas",
        "keywords": [
            "carcel por deudas", "voy preso si no pago", "deuda banco carcel", 
            "prestamo carcel", "deuda tarjeta"
        ],
        "respuesta": "🚫 **No hay prisión por deudas:**\n\nLa Constitución Política del Perú (Art. 2, inc. 24.c) establece que **no hay prisión por deudas**. \n\n⚠️ **Única Excepción:** La deuda por **Pensión de Alimentos**. Esa es la única deuda que te puede llevar a la cárcel."
    },
    {
        "tema": "Prescripción de Deudas",
        "keywords": [
            "cuando prescribe una deuda", "borrar infocorp", "deuda antigua", 
            "cuantos años caduca deuda", "prescripcion deuda"
        ],
        "respuesta": "📆 **Prescripción de Deudas:**\n\nLas deudas no son eternas. La acción para cobrar prescribe a los **10 años** (acción personal) en la mayoría de contratos civiles.\n\n*Infocorp:* La central de riesgo te mantiene en el registro negativo por un máximo de **5 años** desde el vencimiento de la deuda, pero la deuda con el banco sigue existiendo hasta que prescriba o pagues."
    },
    {
        "tema": "Cambio de Nombre",
        "keywords": [
            "cambiar mi nombre", "cambiar mi apellido", "rectificacion partida", 
            "nombre ridiculo", "error en partida"
        ],
        "respuesta": "✍️ **Cambio de Nombre:**\n\nEn Perú, el nombre es inmutable, salvo motivos justificados.\n1. **Por error:** Se hace vía notarial o judicial (Rectificación de Partida).\n2. **Por motivos graves:** Si el nombre es ofensivo, ridículo o atenta contra la dignidad (ej: llamarse 'Hitler' o nombres humillantes), se puede solicitar el cambio ante un Juez Civil."
    },
    # ==================== BLOQUE LABORAL: DESPIDOS Y RENUNCIAS ====================
    {
        "tema": "Despido Arbitrario (Sin Causa)",
        "keywords": [
            "me botaron", "despido arbitrario", "sin causa justa", "me echaron del trabajo", 
            "despido intempestivo", "me sacaron sin avisar"
        ],
        "respuesta": "🚫 **Despido Arbitrario (D.L. 728):**\n\nSi te despiden sin una causa legal comprobada o sin seguir el procedimiento (carta de preaviso), tienes derecho a una **Indemnización**.\n\n💰 **Cálculo:** 1.5 sueldos por cada año completo de servicios (con un tope máximo de 12 sueldos). Las fracciones de año se pagan por dozavos y treintavos."
    },
    {
        "tema": "Despido Nulo (Prohibido)",
        "keywords": [
            "despido embarazada", "despido sindicato", "despido discriminacion", 
            "despido nulo", "me botaron por estar embarazada", "reclame mis derechos y me botaron"
        ],
        "respuesta": "🛑 **Despido Nulo:**\n\nEs ilegal despedir a alguien por:\n1. Embarazo o lactancia.\n2. Afiliarse a un sindicato o ser dirigente.\n3. Discriminación (raza, sexo, religión, VIH).\n4. Presentar una queja contra la empresa.\n\n✅ **Consecuencia:** No solo pagan indemnización, sino que puedes pedir la **Reposición** (que te devuelvan tu puesto) y el pago de todos los sueldos dejados de percibir (devengados)."
    },
    {
        "tema": "Liquidación de Beneficios",
        "keywords": [
            "liquidacion", "cuanto me toca", "pago final", "calcule mi liquidacion", 
            "demora liquidacion", "no me pagan mi liquidacion"
        ],
        "respuesta": "🧮 **Liquidación de Beneficios Sociales:**\n\nAl terminar el vínculo laboral (por renuncia o despido), la empresa tiene **48 horas** para pagarte:\n1. CTS Trunca.\n2. Vacaciones Truncas y no gozadas.\n3. Gratificaciones Truncas.\n\n⚠️ **Si no pagan:** Puedes denunciar ante SUNAFIL y exigir intereses legales laborales."
    },
    {
        "tema": "Renuncia y Preaviso",
        "keywords": [
            "renuncia", "renunciar", "carta de renuncia", "30 dias", 
            "exoneracion de plazo", "irme del trabajo"
        ],
        "respuesta": "👋 **Renuncia Voluntaria:**\n\nLa ley exige avisar con **30 días de anticipación**. \n\n✅ **El Truco:** Puedes pedir la **'Exoneración del Plazo de Preaviso'** en tu carta. Si el empleador no te contesta negándotelo en 3 días, se asume aceptado y puedes irte antes."
    },

    # ==================== BLOQUE LABORAL: BENEFICIOS (PLATA) ====================
    {
        "tema": "CTS (Compensación Tiempo Servicios)",
        "keywords": [
            "cts", "compensacion tiempo de servicios", "cuando depositan cts", 
            "seguro desempleo", "retiro cts"
        ],
        "respuesta": "💰 **CTS (Compensación por Tiempo de Servicios):**\n\nEs un beneficio social para protegerte cuando te quedes sin empleo.\n* **Depósitos:** La empresa deposita medio sueldo aprox. en **Mayo** y **Noviembre** en el banco que tú elijas.\n* **Retiro:** Actualmente (según leyes vigentes temporales) se puede disponer del 100%, pero la norma general es que es intangible hasta que ceses o acumules 4 sueldos."
    },
    {
        "tema": "Gratificaciones (Julio y Diciembre)",
        "keywords": [
            "grati", "gratificacion", "aguinaldo", "pago julio", "pago diciembre", 
            "bono 9 por ciento"
        ],
        "respuesta": "🎁 **Gratificaciones (Ley 27735):**\n\nSi estás en planilla (Régimen Privado), recibes un sueldo completo extra en **Julio** (Fiestas Patrias) y **Diciembre** (Navidad).\n\n➕ **Bono Extra:** Además, te pagan el 9% adicional que la empresa pagaría a EsSalud (Bonificación Extraordinaria)."
    },
    {
        "tema": "Utilidades (Ganancias)",
        "keywords": [
            "utilidades", "reparto de utilidades", "ganancias empresa", 
            "cuando pagan utilidades"
        ],
        "respuesta": "📈 **Utilidades:**\n\nEs un derecho si trabajas en una empresa que:\n1. Tiene más de **20 trabajadores**.\n2. Generó rentas (ganancias) el año anterior.\n*Se pagan usualmente entre Marzo y Abril. El monto depende de tus días trabajados y tu sueldo.*"
    },
    {
        "tema": "Asignación Familiar",
        "keywords": [
            "asignacion familiar", "bono hijos", "tengo hijos trabajo", 
            "10 por ciento", "pago por hijos"
        ],
        "respuesta": "👶 **Asignación Familiar:**\n\nSi tienes hijos menores de 18 años (o hasta 24 si estudian), tienes derecho a un pago extra mensual.\n\n💰 **Monto:** Es el **10% del Sueldo Mínimo Vital** (actualmente S/ 102.50). Es un monto fijo, no importa si tienes 1 o 5 hijos."
    },

    # ==================== BLOQUE LABORAL: CONTRATOS TRAMPOSOS ====================
    {
        "tema": "Locación de Servicios (Recibo por Honorarios)",
        "keywords": [
            "recibo por honorarios", "locacion de servicios", "sin planilla", 
            "marco tarjeta y emito recibo", "falso independiente", "primacia de la realidad"
        ],
        "respuesta": "🕵️ **Principio de Primacía de la Realidad:**\n\nSi emites Recibo por Honorarios (Locación) PERO:\n1. Tienes un horario fijo.\n2. Tienes un jefe que te da órdenes (subordinación).\n3. Trabajas en la oficina de la empresa.\n\n🚨 **¡Es un fraude!** Eres un trabajador en planilla camuflado. Tienes derecho a TODOS los beneficios (CTS, Grati, Vacaciones) desde el primer día. Puedes denunciar a SUNAFIL para que te reconozcan."
    },
    {
        "tema": "Contrato CAS (Sector Público)",
        "keywords": [
            "cas", "contrato administrativo de servicios", "trabajo estado", 
            "municipalidad cas", "derechos cas"
        ],
        "respuesta": "🏛️ **Régimen CAS (D.L. 1057):**\n\nEs un contrato especial para el Sector Público. Aunque antes tenía pocos derechos, ahora tienen:\n* Aguinaldos (S/ 300 en Julio/Dic).\n* Vacaciones de 30 días.\n* Licencias (maternidad, paternidad).\n* Seguridad Social.\n⚠️ *Ojo:* El CAS es temporal, pero ya existen leyes para pasar a régimen indeterminado en ciertos casos."
    },
    {
        "tema": "Periodo de Prueba",
        "keywords": [
            "periodo de prueba", "3 meses", "me botaron a los dos meses", 
            "prueba laboral"
        ],
        "respuesta": "⏳ **Periodo de Prueba:**\n\nEs de **3 meses** para trabajadores normales. Durante este tiempo, pueden despedirte sin causa y SIN indemnización (solo te pagan tus días trabajados).\n\n* **6 meses:** Para puestos de confianza.\n* **1 año:** Para personal de dirección."
    },

    # ==================== BLOQUE LABORAL: PROTECCIÓN Y ACOSO ====================
    {
        "tema": "Hostilidad Laboral (Acoso)",
        "keywords": [
            "me quieren aburrir", "hostilidad", "me bajaron el sueldo", 
            "me cambiaron de sede", "maltrato jefe", "hostigamiento"
        ],
        "respuesta": "😤 **Actos de Hostilidad:**\n\nEl empleador NO puede:\n1. Bajarte el sueldo sin autorización.\n2. Trasladarte a un lugar lejano para perjudicarte.\n3. Faltarte el respeto.\n\n✅ **Acción:** Debes enviar una carta de 'Cese de Hostilidad'. Si no paran, puedes darte por despedido (Despido Indirecto) y cobrar indemnización."
    },
    {
        "tema": "Acoso Sexual Laboral",
        "keywords": [
            "acoso sexual", "tocamientos", "propuestas indecentes", 
            "jefe acosador", "comite hostigamiento"
        ],
        "respuesta": "🛑 **Hostigamiento Sexual Laboral:**\n\nSi recibes insinuaciones, tocamientos o comentarios sexuales no deseados.\n\n1. **Denuncia:** Ante Recursos Humanos (Comité de Intervención).\n2. **Protección:** La empresa debe rotar al agresor o darte medidas de protección inmediatamente.\n3. **Despido:** Es causa justa para despedir al acosador."
    },
    {
        "tema": "Licencia por Maternidad/Paternidad",
        "keywords": [
            "licencia maternidad", "licencia paternidad", "cuantos dias paternidad", 
            "dias por hijo"
        ],
        "respuesta": "👶 **Licencias por Nacimiento:**\n\n* **Madres:** 98 días (49 prenatal y 49 postnatal). Pueden acumularse.\n* **Padres:** 10 días calendario consecutivos (15 días si son gemelos o parto prematuro). La empresa debe pagarlos obligatoriamente."
    },

 # ==================== DELITOS INFORMÁTICOS Y CIBERCRIMEN (LEY 30096) ====================
    {
        "tema": "Fraude Informático (Robo de dinero digital)",
        "keywords": [
            "me vaciaron la cuenta", "transferencia que no hice", "robo por internet", 
            "fraude informatico", "clonaron mi tarjeta", "consumo no reconocido", 
            "yape falso", "plim falso"
        ],
        "respuesta": "💸 **Fraude Informático (Art. 8 Ley 30096):**\n\nEl que deliberadamente procura un beneficio económico ajeno mediante el uso indebido de tecnologías (clonación de tarjetas, compras online fraudulentas, vaciar cuentas).\n\n⚖️ **Pena:** Cárcel de **3 a 8 años**. Si es cometido por una organización criminal o abusando de una posición en el banco, la pena sube."
    },
    {
        "tema": "Suplantación de Identidad Digital",
        "keywords": [
            "perfil falso", "cuenta falsa", "se hace pasar por mi", "crearon un facebook con mis fotos", 
            "fake", "suplantacion identidad", "robo de identidad"
        ],
        "respuesta": "🎭 **Suplantación de Identidad (Art. 9 Ley 30096):**\n\nCrear perfiles falsos o hacerse pasar por otra persona en redes sociales/internet para causar perjuicio (moral o económico).\n\n⚖️ **Pena:** Privativa de libertad de **3 a 5 años**. \n*Ejemplo:* Crear un Instagram falso de tu ex para insultar a gente o pedir dinero a su nombre."
    },
    {
        "tema": "Grooming (Acoso a Menores)",
        "keywords": [
            "grooming", "adulto contacta niño", "chat con menores", "pedir fotos a niña", 
            "cita con menor de edad", "juegos online chat", "free fire", "roblox"
        ],
        "respuesta": "🐺 **Grooming (Art. 183-B CP):**\n\nEl adulto que contacta a un menor de edad por medios digitales (redes, juegos como Roblox/FreeFire, WhatsApp) con el fin de tener actos sexuales o solicitar material pornográfico.\n\n⚖️ **Pena:** Cárcel efectiva de **4 a 8 años**. ¡No es necesario que se encuentren físicamente, basta con la propuesta por chat!"
    },
    {
        "tema": "Phishing (Páginas Falsas)",
        "keywords": [
            "phishing", "link falso", "mensaje del banco", "correo falso", 
            "te ganaste un premio", "actualiza tus datos", "pagina clonada"
        ],
        "respuesta": "🎣 **Phishing y Abuso de Dispositivos (Art. 10 Ley 30096):**\n\nCrear, vender o usar programas/enlaces para robar datos bancarios o contraseñas (ej: clonar la página del BCP o mandar SMS falsos).\n\n⚖️ **Pena:** 1 a 4 años de cárcel. Se castiga solo con tener la herramienta diseñada para delinquir."
    },
    {
        "tema": "Interceptación de Datos (Espionaje)",
        "keywords": [
            "leer chats ajenos", "interceptar correos", "espiar whatsapp", 
            "hackear whatsapp", "leer mensajes de mi pareja", "keylogger"
        ],
        "respuesta": "🕵️ **Interceptación de Datos (Art. 7 Ley 30096):**\n\nEl que indebidamente intercepta, escucha o interfiere una comunicación privada (leer WhatsApp ajenos, interceptar emails).\n\n⚖️ **Pena:** 3 a 6 años. \n⚠️ **Dato:** Instalar una aplicación espía en el celular de tu pareja ES DELITO."
    },
    {
        "tema": "Difusión de Imágenes Íntimas (Packs)",
        "keywords": [
            "pack", "fotos intimas", "video intimo", "nudes", "difundir", 
            "chantaje sexual", "pasar fotos", "filtrar pack"
        ],
        "respuesta": "📸 **Difusión de Imágenes Íntimas (Art. 154-B CP):**\n\nDifundir imágenes o audios de contenido sexual de una persona sin su consentimiento es delito, aunque ella te las haya enviado voluntariamente.\n\n⚖️ **Pena:** 2 a 5 años de cárcel. \n⚠️ **Agravante:** Si eras pareja o expareja de la víctima, la pena sube a **3 a 6 años**."
    },
    {
        "tema": "Chantaje Sexual (Sextorsión)",
        "keywords": [
            "me pide plata por fotos", "si no le pago publica", "chantaje sexual", 
            "sextorsion", "amenaza con publicar fotos"
        ],
        "respuesta": "🔞 **Chantaje Sexual (Art. 176-C CP):**\n\nAmenazar a alguien con difundir sus fotos íntimas si no accede a tener relaciones sexuales o realizar actos de connotación sexual.\n\n⚖️ **Pena:** Cárcel entre **4 y 8 años**. Si lo que pide es dinero, se convierte en **Extorsión**."
    },
    {
        "tema": "Pornografía Infantil",
        "keywords": [
            "pornografia infantil", "cp", "videos de niños", "fotos de menores", 
            "almacenar videos prohibidos", "descargar prohibido"
        ],
        "respuesta": "🚫 **Pornografía Infantil (Art. 183-A CP):**\n\nDelito de 'Tolerancia Cero'.\n* **Posesión:** Solo tener los archivos en tu PC/Celular (Pena 5-10 años).\n* **Comercialización/Difusión:** Vender o pasar los archivos (Pena 10-15 años).\n* **Producción:** Grabar al menor (Pena 15-20 años)."
    },
    {
        "tema": "Acceso Ilícito (Hacking)",
        "keywords": [
            "hackear facebook", "entrar a cuenta ajena", "adivinar contraseña", 
            "entrar al sistema", "acceso ilicito"
        ],
        "respuesta": "💻 **Acceso Ilícito (Art. 2 Ley 30096):**\n\nEntrar a un sistema informático (correo, red social, base de datos) vulnerando las medidas de seguridad.\n\n⚖️ **Pena:** 1 a 4 años. Si accedes a sistemas del Estado o bancos, la pena es mayor."
    },

  # ==================== TRÁNSITO, POLICÍA Y DERECHOS CIUDADANOS ====================
    {
        "tema": "Intervención Policial (DNI)",
        "keywords": ["policia", "tombo", "dni", "detencion", "control de identidad", "comisaria", "me paro la policia"],
        "respuesta": "👮 **Control de Identidad (Art. 205 CPP):**\n\nLa policía puede pedirte DNI en la vía pública para identificarte.\n\n* **Si tienes DNI:** Te identificas y te vas (salvo que tengas Requisitoria).\n* **Si NO tienes DNI:** Pueden llevarte a la comisaría para identificarte (biométrico/Reniec). \n⚠️ **Límite:** La retención NO puede durar más de **4 horas**. No pueden meterte al calabozo por esto."
    },
    {
        "tema": "Grabar a la Policía",
        "keywords": [
            "grabar policia", "filmar intervencion", "puedo grabar", "me prohiben grabar", 
            "celular policia", "borrar video"
        ],
        "respuesta": "📱 **Derecho a Grabar:**\n\n**SÍ puedes grabar.** El Tribunal Constitucional y el Mininter han confirmado que el ciudadano tiene derecho a registrar las intervenciones policiales en la vía pública.\n\n🚫 **Abuso:** Si un policía te quita el celular o te obliga a borrar el video, comete **Abuso de Autoridad**. Solo pueden incautar tu celular con orden judicial o si es prueba de un delito flagrante."
    },
    {
        "tema": "Allanamiento de Domicilio (Policía)",
        "keywords": [
            "policia entra a mi casa", "orden judicial", "romper puerta", 
            "allanamiento", "entrar sin orden"
        ],
        "respuesta": "🚪 **Inviolabilidad de Domicilio (Art. 2 Constitución):**\n\nLa policía NO puede entrar a tu casa sin tu permiso, SALVO en 3 casos:\n1. **Orden Judicial** de allanamiento.\n2. **Delito Flagrante** (persiguiendo al ladrón que acaba de robar o venta de drogas en ese instante).\n3. **Peligro Inminente** (incendio, alguien pidiendo auxilio)."
    },
    {
        "tema": "Conducción Ebria",
        "keywords": ["ebrio", "borracho", "alcohol", "pico de botella", "manejar tomado", "dosaje etilico"],
        "respuesta": "🍺 **Peligro Común (Conducción en ebriedad):**\n\nLímite legal: **0.5 g/litro** (particular) o **0.25** (transporte público/moto).\n\n⚖️ **Consecuencias:**\n1. Multa (M02: 50% de una UIT).\n2. Cancelación del Brevete (Inhabilitación).\n3. Pena privativa de libertad no mayor de 2 años (o servicios comunitarios).\n*Si causas muerte o lesiones ebrio, la pena es cárcel efectiva.*"
    },
    {
        "tema": "Accidente de Tránsito (SOAT)",
        "keywords": [
            "choque", "atropello", "soat", "accidente", "seguro", "herido accidente"
        ],
        "respuesta": "🚑 **Accidente y SOAT:**\n\nSi hay heridos, el **SOAT** cubre automáticamente los gastos médicos (hasta 5 UIT), sin importar quién tuvo la culpa.\n\n⚠️ **Fuga:** Si chocas y te fugas sin auxiliar a la víctima, cometes delito de **Fuga del Lugar del Accidente de Tránsito** (Art. 408 CP), con pena de cárcel, además de las lesiones."
    },
    {
        "tema": "Lunas Polarizadas",
        "keywords": [
            "lunas oscuras", "polarizado", "permiso lunas", "multa polarizado"
        ],
        "respuesta": "😎 **Lunas Polarizadas:**\n\nPara usar vidrios oscurecidos necesitas un permiso del Ministerio del Interior. \n\n👮 **Multa:** Si no tienes el permiso vigente, te corresponde la papeleta **G17** (Multa + Retención del vehículo hasta que regules la situación)."
    },
    {
        "tema": "Coima / Corrupción",
        "keywords": ["coima", "soborno", "corrupcion", "policia plata", "cohecho", "arreglar"],
        "respuesta": "💸 **Cohecho (Coima):**\n\n* **El que recibe (Policía):** Cohecho Pasivo (Pena 5-8 años).\n* **El que da (Tú):** Cohecho Activo (Pena 4-6 años).\n\n🚨 **Flagrancia:** Ofrecer 'arreglar' con dinero a un policía es delito instantáneo. Te pondrán las esposas en ese momento y serás procesado penalmente."
    },

    # ==================== CONSUMIDOR (INDECOPI) Y VIVIENDA ====================
    {
        "tema": "Defensa del Consumidor (Garantía)",
        "keywords": [
            "indecopi", "reclamo", "libro de reclamaciones", "garantia", 
            "producto malogrado", "devolucion dinero"
        ],
        "respuesta": "🛒 **Derechos del Consumidor:**\n\n1. **Idoneidad:** El producto debe servir para lo que lo compraste.\n2. **Libro de Reclamaciones:** Todos los negocios deben tenerlo (físico o virtual). Si reclamas, deben responderte en máximo **15 días hábiles**.\n3. **Garantía:** Si falla, tienes derecho a reparación, cambio o devolución del dinero."
    },
    {
        "tema": "Discriminación (Derecho de Admisión)",
        "keywords": [
            "discriminacion", "no me dejaron entrar", "derecho de admision", 
            "reservado el derecho de admision", "racismo discoteca"
        ],
        "respuesta": "🚫 **Discriminación:**\n\nEl cartel 'Nos reservamos el derecho de admisión' NO permite discriminar. Nadie puede impedirte la entrada por tu ropa, color de piel, orientación sexual o discapacidad.\n\n⚖️ **Sanción:** Indecopi impone multas altísimas (hasta 450 UIT) a los locales que discriminan."
    },
    {
        "tema": "Bullying Escolar (Indecopi)",
        "keywords": [
            "bullying", "acoso escolar", "colegio no hace nada", 
            "mi hijo le pegan", "indecopi colegios"
        ],
        "respuesta": "🏫 **Bullying en Colegios Privados:**\n\nEl colegio tiene la obligación de actuar. Debe tener un psicólogo y un Libro de Registro de Incidencias.\n\n⚠️ **Sanción:** Si el colegio sabe del bullying y no hace nada, Indecopi puede multarlo. Los padres pueden denunciar ante Indecopi por 'falta de idoneidad del servicio educativo'."
    },
    {
        "tema": "Inquilinos y Alquiler (Desalojo)",
        "keywords": [
            "inquilino moroso", "no paga renta", "desalojo", "sacar inquilino", "contrato alquiler"
        ],
        "respuesta": "🏠 **Arrendamiento y Desalojo:**\n\nSi el inquilino debe **2 meses y 15 días** de renta, puedes resolver el contrato.\n\n✅ **Desalojo Express:** Si tu contrato tiene 'Cláusula de Allanamiento' y está legalizado notarialmente, puedes desalojarlo rápidamente con ayuda del Notario y el Juez de Paz."
    },
    {
        "tema": "Corte de Servicios (Inquilinos)",
        "keywords": [
            "cortar agua inquilino", "cortar luz", "sacar cosas inquilino", 
            "cambiar chapa", "coaccion"
        ],
        "respuesta": "🚰 **¡Cuidado Dueño! (Coacción):**\n\nAunque el inquilino no pague, el dueño **NO PUEDE** cortar el agua/luz, quitar la puerta o cambiar la chapa por la fuerza. \n\n⚖️ **Delito:** Eso es **Usurpación** o **Coacción**. El inquilino (aunque moroso) podría denunciarte penalmente. Debes usar la vía legal del Desalojo."
    },
    {
        "tema": "Garantía de Alquiler",
        "keywords": [
            "devolucion garantia", "garantia alquiler", "pintar departamento", 
            "dueño no devuelve garantia"
        ],
        "respuesta": "💰 **Devolución de Garantía:**\n\nLa garantía sirve para cubrir daños o deudas al final del contrato. Si el inmueble está en buen estado (salvo el desgaste normal) y no hay deudas, el dueño **DEBE devolverla**.\n*Si no lo hace, se puede invitar a conciliar o demandar obligación de dar suma de dinero.*"
    },

    # ==================== GENERALES Y CONSTITUCIÓN ====================
    {
        "tema": "Legítima Defensa",
        "keywords": ["defensa propia", "legitima defensa", "me defendi", "mate al ladron"],
        "respuesta": "🛡️ **Legítima Defensa (Art. 20 CP):**\n\nNo tienes responsabilidad penal si te defiendes de una agresión ilegítima, real y actual.\n\n✅ **Requisitos:**\n1. Agresión ilegítima.\n2. Necesidad racional del medio empleado (no significa igualdad de armas, sino usar lo que tengas a mano razonablemente).\n3. Falta de provocación suficiente."
    },
    {
        "tema": "Habeas Corpus (Libertad)",
        "keywords": [
            "habeas corpus", "detenido ilegalmente", "preso sin motivo", 
            "libertad personal"
        ],
        "respuesta": "⚖️ **Habeas Corpus:**\n\nEs una garantía constitucional que se presenta ante el Juez cuando la libertad de una persona es vulnerada (ej: detención arbitraria por la policía sin motivo, o desaparición forzada). Se resuelve en tiempo récord (24-48 horas)."
    },
    {
        "tema": "Saludos del Grupo 03",
        "keywords": ["hola", "buenos dias", "buenas", "que tal", "inicio", "holi", "Holiwis", "quienes son", "autores", "creadores"],
        "respuesta": "👋 **¡Hola! Soy JurisBot Perú (IA Legal)**\n\nProyecto de Inteligencia Artificial desarrollado por estudiantes de Ingeniería de Sistemas de la **UNJFSC**:\n\n👨‍🎓 **Callan Bautista, Giomar**\n👨‍🎓 **Gomez Castillo, Alejandro**\n👨‍🎓 **Tiburcio Shuan, Leonardo**\n👨‍🎓 **Villavicencio Romero, Renzo**\n\n💡 *Estoy capacitado en Derecho Penal, Civil, Laboral y Protección al Consumidor. ¡Hazme una pregunta!*"
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