import warnings
# Oculta las advertencias de versiones diferentes de scikit-learn en la terminal
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

import streamlit as st
import joblib
import spacy
import string
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Detector de Estado de Ánimo", page_icon="🌿", layout="centered")

# --- INICIALIZAR HISTORIAL EN LA SESIÓN ---
if "historial_animo" not in st.session_state:
    st.session_state.historial_animo = []

# --- SPACY (Optimizado y sin spinner de bloqueo) ---
@st.cache_resource(show_spinner=False)
def cargar_spacy():
    try:
        return spacy.load("es_core_news_sm")
    except OSError:
        import os
        os.system("python -m spacy download es_core_news_sm")
        return spacy.load("es_core_news_sm")

nlp = cargar_spacy()

def limpiar_texto(texto):
    doc = nlp(texto)
    tokens = [t.lemma_.lower() for t in doc
              if not t.is_stop and not t.is_punct and t.text.strip() not in string.punctuation]
    return ' '.join(tokens)

# ==========================================
# --- CSS (Fondo Crema Terroso, Mármol y Contraste Blindado) ---
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght=700;900&family=Inter:wght=400;500;600&display=swap');

/* Fondo general de la app (Crema Terroso Cálido #e3e6da) */
.stApp {
    background-color: #e3e6da !important; 
    background-image:
      /* Esquina superior izquierda (Hojas grandes) */
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='0 0 220 220'><g fill='%237aa874' opacity='0.45'><path d='M20 20 C 60 40, 90 90, 80 160 C 60 120, 30 80, 20 20 Z'/><path d='M60 10 C 100 30, 130 80, 120 150 C 100 110, 70 70, 60 10 Z' opacity='0.6'/></g></svg>"),
      /* Esquina superior derecha (Helecho sutil) */
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='0 0 220 220'><g fill='%235d8258' opacity='0.35'><path d='M200 20 C 160 40, 130 90, 140 160 C 160 120, 190 80, 200 20 Z'/><path d='M170 15 C 140 40, 120 80, 130 130 C 150 100, 160 60, 170 15 Z' opacity='0.5'/></g></svg>"),
      /* Lateral izquierdo medio (Hojas flotantes) */
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='150' height='150' viewBox='0 0 150 150'><g fill='%237aa874' opacity='0.25'><path d='M10 75 C 40 75, 70 95, 60 130 C 45 105, 25 90, 10 75 Z'/></g></svg>"),
      /* Lateral derecho medio (Rama fina) */
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'><g fill='%235d8258' opacity='0.3'><path d='M170 90 C 130 95, 110 120, 120 160 C 135 130, 155 110, 170 90 Z'/></g></svg>"),
      /* Esquina inferior izquierda (Plantas densas) */
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='0 0 220 220'><g fill='%237aa874' opacity='0.45'><path d='M20 200 C 60 180, 90 130, 80 60 C 60 100, 30 140, 20 200 Z'/><path d='M50 210 C 80 180, 110 140, 100 80 C 80 120, 60 160, 50 210 Z' opacity='0.5'/></g></svg>"),
      /* Esquina inferior derecha (Hojas tropicales) */
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='0 0 220 220'><g fill='%232f5233' opacity='0.3'><path d='M200 200 C 160 180, 130 130, 140 60 C 160 100, 190 140, 200 200 Z'/></g></svg>");
    
    background-repeat: no-repeat, no-repeat, no-repeat, no-repeat, no-repeat, no-repeat;
    background-position: top left, top right, left 45%, right 55%, bottom left, bottom right;
    background-size: 240px, 240px, 150px, 180px, 240px, 240px;
}

/* TÍTULO PRINCIPAL */
h1.titulo-principal, .titulo-principal {
    font-family: 'Playfair Display', serif !important;
    font-weight: 900 !important;
    font-size: 2.8rem !important;
    color: #1b331e !important;
    text-align: center !important;
    margin: 0.5rem 0 0.3rem 0 !important;
    -webkit-text-fill-color: #1b331e !important;
}
.subtitulo {
    font-family: 'Inter', sans-serif !important;
    text-align: center !important;
    color: #3b4d3b !important;
    font-size: 1.05rem !important;
    margin-bottom: 0.3rem !important;
}
.separador {
    text-align: center;
    color: #5d8258;
    font-size: 1.3rem;
    margin: 0.8rem 0;
    letter-spacing: 6px;
}

/* Tarjetas (Mármol Claro #f4f6f0) */
.tarjeta {
    background: #f4f6f0 !important; 
    border: 1.5px solid #b3baa6 !important;
    border-radius: 18px;
    padding: 1.3rem 1.6rem;
    box-shadow: 0 6px 16px rgba(40, 60, 35, 0.1);
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
}

/* Detalle superior de las tarjetas */
.tarjeta::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #5d8258 0%, #1b331e 100%);
}

.tarjeta-titulo {
    font-family: 'Playfair Display', serif !important;
    color: #1b331e !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.8rem 0 !important;
}

/* --- DETALLES DE CONTRASTE PARA LAS MÉTRICAS (st.metric) --- */
[data-testid="stMetricLabel"], 
[data-testid="stMetricLabel"] > div, 
[data-testid="stMetricLabel"] p,
.st-emotion-cache-16293g2,
.st-emotion-cache-1wugsn5,
.st-emotion-cache-6vsc96 {
    color: #2b442e !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

[data-testid="stMetricValue"], 
[data-testid="stMetricValue"] > div,
[data-testid="stMetricValue"] div,
.st-emotion-cache-10r0gix,
.st-emotion-cache-12w0qpk,
.st-emotion-cache-1xarl3b {
    color: #1b331e !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 900 !important;
}

/* Cajas de st.metric nativos (Verde Salvia suave #e9ece3) */
div[data-testid="stMetric"] {
    background-color: #e9ece3 !important; 
    border: 1px solid #b3baa6 !important;
    border-radius: 12px;
    padding: 10px 15px !important;
}

/* Selector de opción e input de fecha (Verde Salvia suave #e9ece3) */
.stSelectbox div[data-baseweb="select"],
.stDateInput div[data-baseweb="input"] {
    background-color: #e9ece3 !important;
    border: 1.5px solid #b3baa6 !important;
    border-radius: 12px !important;
}
.stSelectbox div[data-baseweb="select"] *,
.stDateInput div[data-baseweb="input"] * {
    color: #1b331e !important;
}

/* Área de texto (Verde Salvia suave #e9ece3) */
.stTextArea textarea {
    background-color: #e9ece3 !important;
    border: 1.5px solid #b3baa6 !important;
    border-radius: 12px !important;
    color: #1b331e !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: #1b331e !important;
    box-shadow: 0 0 0 1px #1b331e !important;
}

/* Placeholders y descripciones */
.stTextArea textarea::placeholder {
    color: #4a5c4a !important;
    opacity: 0.9 !important;
}
.stTextArea div[data-testid="InputInstruction"] {
    color: #4a5c4a !important;
}

/* Botón de Enviar */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(180deg, #3d6b3f 0%, #1b331e 100%) !important;
    color: #e2d9c2 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 12px rgba(27, 51, 30, 0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(27, 51, 30, 0.35) !important;
}

/* Cajas de resultado */
.resultado-box {
    background: linear-gradient(180deg, #3d6b3f 0%, #1b331e 100%);
    color: #e2d9c2 !important;
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    text-align: center;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    margin-bottom: 0.7rem;
}
.confianza-box {
    background: linear-gradient(180deg, #4a7a4d 0%, #3d6b3f 100%);
    color: #e2d9c2 !important;
    border-radius: 14px;
    padding: 0.8rem 1.2rem;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

/* Barras de probabilidad */
.prob-row { display:flex; align-items:center; gap:12px; margin-bottom:10px; font-family:'Inter',sans-serif; }
.prob-label { width:110px; color:#1b331e; font-weight:600; font-size:0.95rem; text-align: left; }
.prob-bar-bg { flex:1; background:#c8bfa6; border-radius:20px; height:14px; overflow:hidden; }
.prob-bar-fill { height:100%; background:linear-gradient(90deg,#7aa874 0%,#1b331e 100%); border-radius:20px; }

/* Aviso temático informativo */
.aviso-botanico {
    background-color: #d1d9be !important; 
    border: 1.5px solid #a4b093 !important; 
    border-radius: 12px;
    padding: 12px 16px;
    color: #1b331e !important; 
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    margin-top: 15px;
    margin-bottom: 15px;
}

header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# --- INTERFAZ ---
# ==========================================
st.markdown('<h1 class="titulo-principal">🌿 Detector de Estado de Ánimo</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">🍃 Analiza el tono emocional de tus palabras con Inteligencia Artificial 🍃</p>', unsafe_allow_html=True)
st.markdown('<div class="separador">∼ 🌿 ∼</div>', unsafe_allow_html=True)

# --- CARGAR RECURSOS (Optimizado sin bloqueos) ---
@st.cache_resource(show_spinner=False)
def cargar_recursos():
    try:
        modelo_cargado = joblib.load("LogisticRegression_Balanced.pkl")
        vectorizador_cargado = joblib.load("vectorizador.pkl")
        return modelo_cargado, vectorizador_cargado
    except FileNotFoundError:
        return None, None

modelo, vectorizador = cargar_recursos()
if modelo is None or vectorizador is None:
    st.warning("⚠️ Faltan 'LogisticRegression_Balanced.pkl' o 'vectorizador.pkl' en la carpeta.")
    st.stop()

# Tarjeta de entrada de texto
st.markdown(
    '<div class="tarjeta"><div class="tarjeta-titulo">¿Cómo te encuentras hoy? 🍃🧠</div>',
    unsafe_allow_html=True
)
texto_usuario = st.text_area(
    "input",
    placeholder="Escribe aquí... Ej: Hoy ha sido un gran día y me siento con mucha motivación.",
    height=130,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# --- NUEVO: CALENDARIO DE SELECCIÓN DE FECHA ---
st.markdown('<div style="margin-top:-5px; margin-bottom:15px; font-family:\'Inter\',sans-serif; font-weight:600; color:#1b331e;">📅 Selecciona la fecha de registro:</div>', unsafe_allow_html=True)
fecha_registro = st.date_input(
    "Selecciona la fecha para este registro",
    value=datetime.now().date(),
    label_visibility="collapsed"
)

st.write("") 
analizar = st.button("🌱   Analizar mi estado de ánimo")

if analizar:
    if texto_usuario.strip() == "":
        st.info("⚠️ Por favor, escribe algo antes de analizar.")
    else:
        texto_limpio = limpiar_texto(texto_usuario)
        texto_vec = vectorizador.transform([texto_limpio])
        prediccion = modelo.predict(texto_vec)[0]
        probabilidades = modelo.predict_proba(texto_vec)[0]
        clases = modelo.classes_

        pred_cruda = str(prediccion).lower().strip().replace("_", " ")

        if "suicidal" in pred_cruda or "suicida" in pred_cruda:
            valor_animo = -3
            prediccion_es = "Suicida"
            emoji_estado = "🚨"
        elif "bipolar" in pred_cruda:
            valor_animo = -2
            prediccion_es = "Bipolaridad"
            emoji_estado = "⚠️"
        elif "personality" in pred_cruda or "personalidad" in pred_cruda:
            valor_animo = -2
            prediccion_es = "Desorden de Personalidad"
            emoji_estado = "⚠️"
        elif "anxiety" in pred_cruda or "ansiedad" in pred_cruda:
            valor_animo = -2
            prediccion_es = "Ansiedad"
            emoji_estado = "⚠️"
        elif "depression" in pred_cruda or "depresión" in pred_cruda or "depresion" in pred_cruda:
            valor_animo = -1
            prediccion_es = "Depresión"
            emoji_estado = "😢"
        elif "stress" in pred_cruda or "estrés" in pred_cruda or "estres" in pred_cruda:
            valor_animo = 0
            prediccion_es = "Estrés"
            emoji_estado = "😰"
        elif "normal" in pred_cruda:
            valor_animo = 1
            prediccion_es = "Normal"
            emoji_estado = "😊"
        else:
            valor_animo = 0
            prediccion_es = str(prediccion).title()
            emoji_estado = "🌿"

        prob_max = max(probabilidades) * 100

        # Combinamos la fecha elegida del calendario con la hora actual para que el historial guarde un timestamp real
        hora_actual = datetime.now().time()
        fecha_completa = datetime.combine(fecha_registro, hora_actual)

        # Guardamos en el historial
        st.session_state.historial_animo.append({
            "Estado": prediccion_es.upper(),
            "Valor": valor_animo,
            "Fecha": fecha_completa
        })

        # --- CONSTRUCCIÓN DE LAS BARRAS EN HTML ---
        traducciones_barras = {
            "anxiety": "Ansiedad",
            "bipolar": "Bipolaridad",
            "depression": "Depresión",
            "personality disorder": "Desorden de Personalidad",
            "stress": "Estrés",
            "suicidal": "Suicida",
            "normal": "Normal"
        }
        
        barras_html = ""
        for clase, prob in zip(clases, probabilidades):
            clase_key = str(clase).lower().strip().replace("_", " ")
            clase_es = traducciones_barras.get(clase_key, str(clase).title())
            pct = float(prob) * 100
            barras_html += f'<div class="prob-row"><div class="prob-label">{clase_es}</div><div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{pct:.1f}%"></div></div></div>'

        bloque_resultado = f"""
        <div class="separador">∼ 🍀 ∼</div>
        <div class="tarjeta">
            <div class="tarjeta-titulo" style="color: #1b331e !important;">Resultados del Análisis 🍃📋</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; margin-top: 10px;">
                <div>
                    <div class="resultado-box">{emoji_estado} ESTADO DETECTADO: {prediccion_es.upper()}</div>
                    <div class="confianza-box">Confianza: {prob_max:.2f}%</div>
                </div>
                <div>
                    {barras_html}
                </div>
            </div>
        </div>
        """
        st.markdown(bloque_resultado, unsafe_allow_html=True)

# ==========================================
# --- SECCIÓN DE HISTORIAL Y GRÁFICO ---
# ==========================================
if len(st.session_state.historial_animo) > 0:
    st.markdown('<div class="separador">∼ 🌿 ∼</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tarjeta"><div class="tarjeta-titulo">Tu Evolución Emocional en el Tiempo 📈🌱</div>',
        unsafe_allow_html=True
    )
    
    df_historial = pd.DataFrame(st.session_state.historial_animo)
    df_grafico = df_historial.copy()
    
    # Formateamos el eje X con el día del mes, nombre corto del mes y hora para una lectura compacta
    df_grafico['Fecha_Registro'] = df_grafico['Fecha'].dt.strftime('%d %b (%H:%M)')
    
    # Ordenamos el DataFrame por la fecha real para pintar correctamente la evolución
    df_grafico = df_grafico.sort_values(by="Fecha")
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.metric("Total de Análisis", len(df_historial))
    with col_der:
        ultimo_estado = df_historial.iloc[-1]['Estado']
        st.metric("Último Estado", ultimo_estado)

    st.markdown("<p style='margin-top:15px; color:#1b331e; font-family:Inter, sans-serif; font-weight:600;'>Evolución de bienestar en la línea de tiempo:</p>", unsafe_allow_html=True)
    
    import altair as alt

    if len(df_historial) < 2:
        st.markdown("""
        <div class="aviso-botanico">
            💡 Haz un segundo análisis (seleccionando otra fecha en el calendario) para conectar los puntos y generar la gráfica de tendencias.
        </div>
        """, unsafe_allow_html=True)
        
        chart_single = alt.Chart(df_grafico).mark_point(
            color='#1b331e', 
            size=120, 
            filled=True
        ).encode(
            x=alt.X('Fecha_Registro:N', title='Fecha de Registro', sort=None),
            y=alt.Y('Valor:Q', title='Nivel de Bienestar', scale=alt.Scale(domain=[-3.5, 1.5]))
        ).properties(
            height=300,
            background='transparent'
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            gridColor='#b3baa6',
            domainColor='#1b331e',
            tickColor='#1b331e',
            labelColor='#3b4d3b',
            titleColor='#1b331e'
        )
        st.altair_chart(chart_single, width="stretch", theme=None)
    else:
        line = alt.Chart(df_grafico).mark_line(
            interpolate='monotone', 
            color='#1b331e', 
            strokeWidth=4
        ).encode(
            x=alt.X('Fecha_Registro:N', title='Fecha de Registro', sort=None),
            y=alt.Y('Valor:Q', title='Nivel de Bienestar', scale=alt.Scale(domain=[-3.5, 1.5]))
        )
        
        points = alt.Chart(df_grafico).mark_point(
            color='#1b331e', 
            size=120,
            filled=True
        ).encode(
            x=alt.X('Fecha_Registro:N', sort=None),
            y=alt.Y('Valor:Q')
        )
        
        final_chart = (line + points).properties(
            height=300,
            background='transparent'
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            gridColor='#b3baa6',
            domainColor='#1b331e',
            tickColor='#1b331e',
            labelColor='#3b4d3b',
            titleColor='#1b331e'
        )
        
        st.altair_chart(final_chart, width="stretch", theme=None)
    
    st.markdown("""
    <div style='font-size: 0.85rem; color: #3b4d3b; margin-top: 15px; margin-bottom: 20px; background-color: #e9ece3; padding: 10px; border-radius: 8px;'>
        <strong>Referencia de Escala:</strong><br>
        🟢 <strong>+1:</strong> Normal 😊 | 
        🟡 <strong>0:</strong> Estrés 😰 | 
        🟠 <strong>-1:</strong> Depresión 😢 | 
        🔴 <strong>-2:</strong> Ansiedad / Bipolaridad / Trastorno de Personalidad ⚠️ | 
        🚨 <strong>-3:</strong> Ideación Suicida
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Borrar historial de la sesión"):
        st.session_state.historial_animo = []
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)