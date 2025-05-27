from flask import Flask, render_template,request,jsonify
import sqlite3
from datetime import datetime
from openai import OpenAI
import json

app = Flask(__name__)

# Ejemplo para el ejercicio: 
# Se busca constituir una S.A.C. en Perú con tres socios (uno extranjero) y S/ 50,000 de capital, incluyendo redacción de estatutos, inscripción en SUNAT y SUNARP, y asesoría legal para el pacto social.

# conexion de base de datos
def init_db():
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute("create table if not exists cotizaciones (id INTEGER PRIMARY KEY, numero text, email text, cliente text, servicio text, precio real, fecha text, complejidad text, ajuste_precio text, servicio_adicionales text, propuesta text ) ")
  conn.commit()
  conn.close()
  

# Precio de cada servicio
precios_list = {
  "Constitucion_de_empresa": 1500, 
  "Defensa_laboral": 2000,
  "Consultoria_tributaria": 800,
}

# Dirigir a carpeta raiz
@app.route("/")
def index ():
  return render_template("index.html")


# Clave api de OpenRouter
api_key= "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"

# Conexion de la API con l OpenRouter
client=OpenAI(api_key=api_key,base_url="https://openrouter.ai/api/v1")
"https://api.openrouter.ai/api/v1"


# Funcion para 
def analizar_complejidad(descripcion, tipo_servicio):
    # Validación básica de inputs
    if not descripcion or not tipo_servicio:
        return generar_respuesta_error("Descripción y tipo de servicio son requeridos")

    # Construcción del prompt
    prompt = f"""
    ANALISIS JURÍDICO - FORMATO JSON ESTRICTO
    Caso: {descripcion}
    Tipo: {tipo_servicio}
    Devuelve SOLO un JSON con: complejidad (Baja/Media/Alta), ajuste_precio (0/25/50), 
    servicios_adicionales (array) y la propuesta (string) profesional de 2 lineas que incluya los servicios_adicionales, el tiempo estimado y las condiciones básicas.
    """

    try:
        # Llamada a la API
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3 
        )
        
        # Extracción y limpieza de respuesta
        raw_content = response.choices[0].message.content
        clean_content = raw_content.strip().replace('```json', '').replace('```', '')
        
        # Parseo y validación
        return json.loads(clean_content) if clean_content else generar_respuesta_error("Respuesta vacía")
        
    except Exception as e:
        # Manejo de errores simplificado
        return generar_respuesta_error(str(e))

def generar_respuesta_error(mensaje):
    return {
        "complejidad": "Media",
        "ajuste_precio": 25,
        "servicios_adicionales": [],
        "propuesta": f"Error: {mensaje}"
    }
    
    
# generar cotizacion 
@app.route("/generar-cotizacion",methods=["POST"])

def generar_cotizacion():
    data = request.form
    
    # Resultado de la generacion de la IA
    analisis_ia = analizar_complejidad(
        descripcion=data.get("descripcion"),
        tipo_servicio=data.get("servicio")
    )
    
    # 2. Calcular precio
    precio_base = precios_list.get(data.get("servicio"), 0)
    precio_final = precio_base * (1 + analisis_ia["ajuste_precio"]/100)
    
    # 3. Generar número de cotización
    numero_cotizacion = f"COT-{datetime.now().year}-{datetime.now().microsecond}"
    
    # 4. Guardar informacion en la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cotizaciones (numero, email, cliente, servicio, precio, fecha, complejidad, ajuste_precio, servicio_adicionales, propuesta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        numero_cotizacion,
        data.get("email"), 
        data.get("nombre"),
        data.get("servicio"),
        precio_final,
        datetime.now().isoformat(),
        analisis_ia["complejidad"],
        analisis_ia["ajuste_precio"],
        ", ".join(analisis_ia["servicios_adicionales"]),
        analisis_ia["propuesta"]
    ))
    conn.commit()
    conn.close()
    
    # Retornar resultados
    return jsonify({
        "numero": numero_cotizacion,
        "precio": precio_final,
        "complejidad": analisis_ia["complejidad"],
        "ajuste": f"{analisis_ia['ajuste_precio']}%",
        "servicios_adicionales": analisis_ia["servicios_adicionales"],
        "propuesta": analisis_ia["propuesta"],
        "fecha": datetime.now().strftime("%d/%m/%Y")
    })
    
# identificar siempre a app.py
if __name__ == "__main__":
  init_db()
  app.run(debug=True)

