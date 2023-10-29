from Clases import *
from Fhandler import *
import os

def com_cat(params, lista_particiones, sesion_activa):
    file = []
    respuesta = ""

    if not sesion_activa:
        respuesta +="--Este comando requiere una sesion activa"
        respuesta += "\n\n"
        return respuesta

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            respuesta +="--Error en el parametro '"+param[0]+"', parametro incompleto"
            respuesta += "\n\n"
            return respuesta 

        if param[0].lower().startswith("file"):
            if param[1][0] == '"':
                file.append(param[1][1:-1])
            else:
                file.append(param[1])

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        respuesta +="--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas"
        respuesta += "\n\n"
        return respuesta

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        respuesta +="--La particion aun no ha sido formateada"
        respuesta += "\n\n"
        return respuesta
    s = ""
    for f in file:
        s+=f+"\n"
        existe, permiso, datos = revisar_permisos(f, datos,sesion_activa)
        if not existe:
            s+="--No existe el archivo\n"
            s+="\n"
            continue
        if permiso[0] == "0":
            s+="--El usuario no tiene permiso de lectura\n"
            s+="\n"
            continue
        
        x, datos = traer_archivo(f,datos)
        s+=x
        s+="\n"

    res[0]["datos"] = datos
    respuesta += s
    return respuesta 
