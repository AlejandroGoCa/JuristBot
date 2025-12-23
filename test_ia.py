import google.generativeai as genai

# TU CLAVE
API_KEY = "AIzaSyAdKwvOTdeTW77zd2_QFlyYrPpvlwIyWwQ"
genai.configure(api_key=API_KEY)

print("🔍 Buscando modelos disponibles para tu clave...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ MODELO ENCONTRADO: {m.name}")
except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")