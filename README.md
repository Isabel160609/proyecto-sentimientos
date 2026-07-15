# proyecto-sentimientos

🌿 Analizador de Ánimo Inteligente (Equipo Sentimientos)
El Analizador de Ánimo Inteligente es una herramienta interactiva de autoconciencia y salud mental desarrollada en Python. Mediante técnicas de Procesamiento del Lenguaje Natural (NLP) y Machine Learning, analiza el tono emocional de las palabras del usuario en tiempo real.

El sistema está diseñado para detectar desórdenes emocionales y estados de estrés, guiando al usuario con empatía a través de una interfaz botánica adaptativa con tonos "Crema y Salvia Terroso".

🚀 Características Clave y Novedades (v2.0)
Traducción Dinámica (Blindaje en Español): Mapeo interno robusto que traduce automáticamente las predicciones nativas del modelo en inglés (Anxiety, Depression, Suicidal, Normal, etc.) a sus correspondientes términos localizados y amigables en español ("Ansiedad", "Depresión", "Suicida", "Normal").

Registro por Calendario Interactivo: Implementación de un componente de fecha st.date_input integrado que reemplaza el selector de meses estático, permitiendo al usuario registrar análisis en cualquier fecha histórica o actual.

Gráfica de Tendencia Spline (Línea Redondeada): Visualización interactiva y orgánica mediante la librería Altair que aplica una interpolación monotone para trazar curvas suaves y puntos circulares exactos sobre cada registro.

Escala de Bienestar Penalizada: Un sistema estructurado que mapea de manera lógica y visual la severidad de los estados de ánimo:

+1: Normal 😊

0: Estrés 😰

-1: Depresión 😢

-2: Ansiedad, Bipolaridad o Trastornos de Personalidad ⚠️

-3: Ideación Suicida 🚨

🛠️ Stack Tecnológico y Modelado
Interfaz de Usuario (Frontend): Streamlit (con CSS inyectado para una experiencia visual relajante con paleta botánica).

Procesamiento de Lenguaje Natural (NLP): SpaCy (es_core_news_sm) para la tokenización, lematización inteligente y filtrado de palabras vacías (stopwords) y signos de puntuación en español.

Modelado de Machine Learning (Backend):

Modelo Logistic Regression Balanced preentrenado, optimizado para manejar eficientemente conjuntos de datos desbalanceados en temas de salud mental.

TF-IDF / Vectorizador para la conversión del texto en variables numéricas interpretables por el modelo.

Visualizaciones: Gráficas dinámicas de dispersión y líneas continuas con Altair.

📦 Estructura del Repositorio

├── app.py                         # Archivo principal de la aplicación Streamlit
├── LogisticRegression_Balanced.pkl # Modelo de Machine Learning entrenado
├── vectorizador.pkl               # Pipeline del vectorizador para preprocesamiento de texto
├── requirements.txt               # Lista de dependencias y librerías del proyecto
└── README.md                      # Documentación del proyecto (este archivo)

💻 Instalación y Ejecución Local
Sigue estos pasos para clonar el repositorio, configurar el entorno virtual e iniciar la aplicación en tu máquina:

1. Clonar el repositorio

 ***git clone https://github.com/Isabel160609/proyecto-sentimientos.git
   cd proyecto-sentimientos***

2. Configurar el Entorno Virtual (Opcional pero recomendado)

 # En Windows:
 ***python -m venv venv
   venv\Scripts\activate***

# En macOS/Linux:
 ***python3 -m venv venv
   source venv/bin/activate***

3. Instalar Dependencias
Instala los paquetes necesarios definidos en requirements.txt:

  ***pip install -r requirements.txt***

4. Descargar el Modelo en Español de SpaCy
Dado que el preprocesamiento de NLP se realiza en español, es indispensable descargar el pipeline de SpaCy ejecutando:

  ***python -m spacy download es_core_news_sm***

5. Lanzar la Aplicación
Inicia el servidor local de Streamlit:

  ***streamlit run app.py***

La herramienta se abrirá automáticamente en tu navegador web predeterminado en la dirección http://localhost:8501.

👥 Miembros del Equipo
Este proyecto ha sido desarrollado con dedicación y enfoque en el impacto social por:

Isabel Domenech (Desarrolladora Full-Stack & Python Dev)

Claudia Grossi (Gestión de Proyectos & Organización)

Waleska Jimenez (Trust & Safety Specialist & Data Analyst)

Desarrollado con ❤️ por el Equipo Sentimientos para promover la autoconciencia y el bienestar mental.
