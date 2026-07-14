# proyecto-sentimientos

🧠 Detector de Estado de Ánimo (Analizador de Sentimientos en Salud Mental)
Este proyecto consiste en una aplicación web interactiva desarrollada con Streamlit que utiliza técnicas de Procesamiento de Lenguaje Natural (PLN) y modelos de Machine Learning de Scikit-learn para interpretar y clasificar estados de ánimo o posibles trastornos reflejados en textos en español.

El modelo ha sido entrenado para identificar múltiples clases como: Normal, Depression, Anxiety, Bipolar, Stress, Personality disorder y Suicidal.

🚀 Características Clave
Preprocesamiento Avanzado con spaCy: Limpieza lingüística en español que incluye tokenización, eliminación de stop words (palabras vacías) y lematización (reducción a la raíz de las palabras) utilizando el modelo es_core_news_sm.

Vectorización de Texto: Uso de TfidfVectorizer controlado con selección de características para convertir el lenguaje humano en vectores numéricos legibles por el algoritmo.

Modelo de Clasificación Balanceado: Entrenamiento con un algoritmo de Regresión Logística configurado con pesos balanceados (class_weight='balanced') para corregir el impacto del desbalance crítico de clases en los datos de salud mental.

Interfaz Interactiva: Una SPA (Single Page Application) limpia y moderna construida en Streamlit con desgloses interactivos de la probabilidad y métricas de confianza en tiempo real.

📁 Estructura del Proyecto
Plaintext
├── app.py                     # Script principal de la aplicación de Streamlit
├── vectorizador.pkl           # Vectorizador TF-IDF serializado (entrenado en Colab)
├── LogisticRegression_Balanced.pkl # Modelo predictivo entrenado con Scikit-learn
├── requirements.txt           # Dependencias de Python necesarias para correr el proyecto
└── README.md                  # Documentación del proyecto (este archivo)
🛠️ Requisitos e Instalación
Para ejecutar este proyecto de manera local en tu computadora, sigue los siguientes pasos:

1. Clonar el repositorio y acceder a él
Bash
git clone https://github.com/tu-usuario/proyecto_final_sentimientos.git
cd proyecto_final_sentimientos
2. Instalar las dependencias
Asegúrate de tener instalado Python 3.10, 3.11 o 3.12 (versión estable recomendada). Instala las librerías necesarias con el siguiente comando:

Bash
pip install -r requirements.txt
3. Descargar el modelo de lenguaje de spaCy para español
Bash
python -m spacy download es_core_news_sm
💻 Cómo Ejecutar la Aplicación
Una vez que tengas los archivos de tu modelo (LogisticRegression_Balanced.pkl y vectorizador.pkl) dentro de la carpeta raíz, inicia el servidor local de Streamlit con:

Bash
streamlit run app.py
Streamlit se abrirá automáticamente en tu navegador web predeterminado en la dirección local: http://localhost:8501.

📊 Flujo de Machine Learning (Backend en Colab)
El desarrollo del modelo siguió el ciclo clásico de vida de un proyecto de ciencia de datos:

EDA (Análisis Exploratorio de Datos): Estudio del desbalance de clases del dataset (donde la gran mayoría de datos se concentraban en clases como Normal y Depression).

Preprocesamiento Estricto: Ejecución de procesamiento en paralelo a través de los pipes nativos de spaCy para limpiar textos en español eficientemente.

Manejo de Desbalance: Corrección del sesgo del modelo aplicando estratificación en el particionado de datos (stratify=y) y entrenando modelos con penalización proporcional por clase.

Serialización: Exportación de artefactos mediante joblib para su consumo ágil en la aplicación de producción.

📝 Ejemplo de requirements.txt
Para garantizar la compatibilidad del software, tu archivo requirements.txt debería verse de la siguiente manera:

Plaintext
streamlit
spacy
joblib
scikit-learn
numpy
pandas
⚠️ Descargo de responsabilidad: Esta aplicación se creó únicamente con fines educativos e informativos. Las predicciones del modelo se basan en patrones lingüísticos estadísticos y bajo ninguna circunstancia deben considerarse como un diagnóstico o reemplazo de una consulta médica o psicológica profesional.
