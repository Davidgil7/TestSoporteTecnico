#Realizado en la version 3.11.4 de python
#Si hay problemas con el modulo cors intalarlo como esta a continuacion
#pip install -U flask-cors

"""1.	Conocimientos de SQL

a) Construya una sentencia SQL para la creación de una vista que involucre los datos de las tres tablas
mencionadas anteriormente

CREATE VIEW VistaLlamadas AS
SELECT e.numeroextension, e.nombreusuario, l.fechahorallamada, l.duracionllamada, l.costollamada, s.tiposervicio
FROM Extensiones e
JOIN Llamadas l ON e.numeroextension = l.numeroextension
JOIN Servicios s ON l.tiposervicio = s.tiposervicio

b) Basándose en la vista anterior, cree una consulta que muestre la siguiente información:

• Número de llamadas realizadas por cada usuario, su duración total y el costo total
"""

b1 ="""SELECT nombreusuario, COUNT(*) AS numerollamadas, SUM(duracionllamada) AS duraciontotal, SUM(costollamada) AS costototal
    FROM VistaLlamadas
    GROUP BY nombreusuario;"""

"""•	Consultar las 10 llamadas con mayor duración"""

b2 = """SELECT * FROM VistaLlamadas
ORDER BY duracionllamada DESC
LIMIT 10;"""

"""•	Consultar las 10 llamadas con mayor costo"""

b3 = """SELECT * FROM VistaLlamadas
ORDER BY costollamada DESC
LIMIT 10;"""

"""•	Consultar el número de llamadas y el costo por tipo de servicio"""

b4 = """SELECT TipoServicio, COUNT(*) AS NumeroLlamadas, SUM(costollamada) AS CostoTotalLlamadas
FROM VistaLlamadas
GROUP BY TipoServicio;"""

import sqlite3
import json
import warnings
from pathlib import Path
from flask import Flask, abort, jsonify
from flask_cors import CORS

warnings.filterwarnings("ignore")

"""2. Conocimientos de programación

Utilizando un lenguaje de programación de su preferencia cree una API Rest que devuelva:

a)	Cree un endpoint que devuelva la vista creada anteriormente.
"""

def EjecucionesBd(sql):

    bd = sqlite3.connect(Path("LlamadasTelefonicas.db"))
    cursor = bd.execute(sql)
    bdData = cursor.fetchall()
    datos = []

    columname = []
    for name in cursor.description:
        columname.append(name[0])

    for fila in bdData:
        dato = {}

        for colun in range(0,len(columname)):
            dato[columname[colun]] = fila[colun]
        datos.append(dato)

    json_data = json.dumps(datos)
    bd.close()

    return json_data

def Encabezados(ejecionSql):
    encaMal = {"FechaHoraLlamada" : "Fecha y Hora Llamada" , 
               "NumeroExtension" : "Número Extensión", 
               "NumeroMarcado" : "Número Marcado", 
               "DuracionLlamada" : "Duración Llamada", 
               "CostoLlamada": "Costo Llamada", 
               "TipoServicio": "Tipo de Servicio",
               "NombreUsuario": "Nombre usuario",
               "numerollamadas":"Llamadas realizadas",
               "duraciontotal": "Duracion de las llamadas",
               "costototal":"Costos total llamadas",
               "NumeroLlamada":"Numero de llamadas",
               "CostoTotalLlamadas": "Costo total llamadas",
               "numeroLlamadas": "Total llamadas realizadas",
                "costoTotal": "Costo total llamadas",
                "duracionTotal": "Duración total llamadas"}

    for enca in encaMal:
        ejecionSql = ejecionSql.replace(enca,encaMal[enca])

    return ejecionSql


app = Flask(__name__)

#whitelist = ['/ResultadosApi.html',]
resources = {
    r"/*": {"origins": "*"}
    #r"/*": {"origins": whitelist, "methods": ["GET"]}
   }

cors = CORS(app, resources=resources)

@app.route("/")
def hello():
    return "Probando"

@app.route('/vistallamadas')
def vistallamadas():

   resultados = EjecucionesBd("SELECT * FROM VistaLlamadas;")
   return Encabezados(resultados),200

"""b)	los registros del resultado de la vista anterior, dependiendo del tipo de consulta que son los siguientes:
        1. Número de llamadas realizadas por cada usuario y su duración y el costo total.
        2. Las 10 llamadas con mayor duración.
        3. Las 10 llamadas con mayor costo.
        4. Número de llamadas y el costo por tipo de servicio."""

@app.route('/numero-llamadas-usuario/<solicitud>')
def llamadasUsuario(solicitud):
  resultados = {"LlamadasXUsuari": EjecucionesBd(b1),
                "10MayorDuracion": EjecucionesBd(b2),
                "10MayorCosto": EjecucionesBd(b3),
                "NllamadasCosto": EjecucionesBd(b4)}
  #resultados = EjecucionesBd(b1)
  match solicitud:
      case "1":
          return Encabezados(resultados["LlamadasXUsuari"]), 200
      case "2":
          return Encabezados(resultados["10MayorDuracion"]), 200
      case "3":
          return Encabezados(resultados["10MayorCosto"]), 200
      case "4":
          return Encabezados(resultados["NllamadasCosto"]), 200
      case _:
          abort(401,"error en la peticion")

"""c)	Cree un endpoint que tome como entrada el número de extensión del usuario y retorne en la estructura que usted decida, el resumen de llamadas que ha realizado el usuario, este resumen debe contener.
            •	Número de llamadas.
            •	Costo total de las llamadas.
            •	Duración total de las llamadas en minutos.
           NOTA: El dato DuracionLLamada viene dado en segundos.
"""
@app.route("/resumen-llamadas/<extension>")
def resumenLlamadas(extension):

    try:
        extension = int(extension)
    except ValueError:
        return jsonify({"error": "El número de extensión debe ser un valor numérico"}), 400


    resultados = EjecucionesBd(f"""SELECT COUNT(*) AS numeroLlamadas, SUM(costollamada) AS costoTotal, SUM(duracionllamada) / 60 AS duracionTotal
        FROM VistaLlamadas
        WHERE numeroextension = {extension}""")
    # La sentencia sql retorna las columnas #LlamadasRealizadas | CostoLLamdas | DuracionLlamadas(minutos)
    return Encabezados(resultados), 200


if __name__ == '__main__':
    app.run(port=5000)

app.run(debug=True)