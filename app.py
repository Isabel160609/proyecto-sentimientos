import streamlit as st 
import joblib 
import numpy as np 
import spacy
import string

# Cargar el modelo en español de spaCy en Streamlit
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    # Por si no está instalado en local
    import os
    os.system("python -m spacy download es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

def limpiar_texto(texto):
    doc = nlp(texto)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and token.text.strip() not in string.punctuation
    ]
    return ' '.join(tokens)

# 1. Configuración de la página
st.set_page_config(
    page_title="Detector de Estado de Ánimo",
    page_icon="🧠",
    layout="centered"
)

# 2. Cargar el modelo y el vectorizador
# Asegúrate de haber guardado tu modelo y vectorizador previamente en tu script de entrenamiento
@st.cache_resource  # Esto evita que Streamlit recargue el modelo en cada clic
def cargar_recursos():
    try:
        modelo = joblib.load("LogisticRegression_Balanced.pkl")
        vectorizador = joblib.load("vectorizador.pkl")
        return modelo, vectorizador
    except FileNotFoundError:
        return None, None

modelo, vectorizador = cargar_recursos()

# 3. Interfaz de Usuario (UI)
st.title("🧠 ¿Cómo te encuentras hoy?")
st.write(
    "Escribe unas líneas sobre cómo ha sido tu día o cómo te sientes "
    "y nuestro modelo predictivo intentará interpretar tu estado de ánimo."
)

# Si no se encuentran los archivos del modelo, mostramos un aviso amigable
if modelo is None or vectorizador is None:
    st.warning(
        "⚠️ No se encontraron los archivos 'LogisticRegression_Balanced.pkl' o 'vectorizador.pkl'. "
        "Por favor, asegúrate de exportarlos en tu script de entrenamiento e incluirlos en la misma carpeta."
    )
else:
    # 4. Entrada de texto del usuario
    texto_usuario = st.text_area(
        "Cuéntame cómo estás:",
        placeholder="Hoy me siento bastante motivado pero un poco cansado...",
        height=150
    )
    
    # Botón para analizar
    if st.button("Analizar mi estado de ánimo", use_container_width=True):
        if texto_usuario.strip() == "":
            st.info("Por favor, escribe algo antes de analizar.")
        else:
            # 5. Preprocesamiento y Predicción
            # Transformamos el texto usando el vectorizador cargado
            texto_limpio = limpiar_texto(texto_usuario)
            texto_vectorizado = vectorizador.transform([texto_limpio])
            
            # Predecimos la clase y obtenemos las probabilidades
            prediccion = modelo.predict(texto_vectorizado)[0]
            probabilidades = modelo.predict_proba(texto_vectorizado)[0]
            clases = modelo.classes_
            
            # Mostramos el resultado de forma visual
            st.subheader("Resultado del análisis:")
            
            # Personaliza este bloque según las etiquetas reales de tu dataset (ej: "Feliz", "Triste", "Estresado")
            st.success(f"El modelo cree que tu estado es: **{prediccion.upper()}**")
            
            # Mostrar la confianza del modelo
            prob_max = max(probabilidades) * 100
            st.write(f"Confianza de la predicción: **{prob_max:.2f}%**")
            
            # Opcional: Mostrar el desglose de probabilidades con barras visuales
            with st.expander("Ver desglose de probabilidades"):
                for clase, prob in zip(clases, probabilidades):
                    st.write(f"**{clase}**")
                    st.progress(float(prob))