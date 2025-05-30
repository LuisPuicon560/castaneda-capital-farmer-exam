# Sistema de Cotizaciones Legales - Capital & Farmer  
Aplicación web para generar cotizaciones legales automáticas con integración de IA. 

## Instalación
1. Clonar el repositorio con gitbash```git clone https://github.com/LuisPuicon560/castaneda-capital-farmer-exam.git```
3. virtualenv -p python3 env
4. .\env\Scripts\actívate
5. pip install -r requirements.txt
6. Dirigir a app.py y agregar clave api en openrouter.ai
7. python app.py

## Uso
- Acceder a http://localhost:5000
- Completar formulario de cotización
- Dar click al boton "Generar Cotización"

## APIs utilizadas
- Api DeepSeek -r1:free

## NPM utilizadas
- Flask
- OpenAi

## Estructura del proyecto
.
├── app.py                # Backend (Flask/FastAPI)
├── templates/            # HTML (Frontend)
│   └── index.html        # Formulario de cotización
├── static/               # Carpeta de estilos y lógica del frontend
    └── css
        └── style.css     # Estilos del lado Frontend
    └── js
        └── script.js     # Lógica del lado Frontend
├── database.db           # Base de datos SQLite
├── requirements.txt      # Dependencias
└── README.md             # Documentación
