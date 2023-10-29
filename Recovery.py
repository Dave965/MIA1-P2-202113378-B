from Clases import *
from Fhandler import *
import os

def com_recovery(params, lista_particiones):
    identificador = None

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return ""
        
        elif param[0].lower() == "id":
            if param[1][0] == '"':
                identificador = param[1][1:-1]
            else:
                identificador = param[1]

    if identificador == None:
        print("--No se encontro el parametro obligatorio 'id'")
        print()
        return ""

    res = [x for x in lista_particiones if x["identificador"] == identificador]
    if len(res) == 0:
        print("--No existe el id '"+identificador+"' entre las particiones cargadas")
        print()
        return ""

    datos = res[0]["datos"]
    
    s = comandosJ(datos)
    return s
