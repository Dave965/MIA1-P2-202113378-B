from Clases import *
from Fhandler import *
import os

def com_copy(params, lista_particiones, sesion_activa):
    path = None
    destino = None
    respuesta = ""


    if not sesion_activa:
        respuesta +=("--Este comando requiere una sesion activa")
        respuesta += "\n\n"
        return respuesta
    
    for x in params:
        param = [w.strip() for w in x.split("=")]

        if param[0].lower() == "r":
            r = True
        elif len(param) != 2:
            respuesta +=("--Error en el parametro '"+param[0]+"', parametro incompleto")
            respuesta += "\n\n"
            return respuesta 

        if param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        if param[0].lower() == "destino":
            if param[1][0] == '"':
                destino = param[1][1:-1]
            else:
                destino = param[1]
                
    if not path:
        respuesta +=("--No se encontro el parametro obligatorio 'path'")
        respuesta += "\n\n"
        return respuesta

    if not destino:
        respuesta +=("--No se encontro el parametro obligatorio 'destino'")
        respuesta += "\n\n"
        return respuesta

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        respuesta +=("--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas")
        respuesta += "\n\n"
        return respuesta

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        respuesta +=("--La particion aun no ha sido formateada")
        respuesta += "\n\n"
        return respuesta
    estado, permiso, datos = revisar_permisos(destino,datos,sesion_activa)
    res[0]["datos"] = datos 

    if not estado:
        respuesta +=("--La ruta no existe")
        respuesta += "\n\n"
        return respuesta
    
    if permiso[1] != "1":
        respuesta +=("--El usuario no tiene permiso de Escritura en el directorio "+destino)
        respuesta += "\n\n"
        return respuesta

    datos = copiar(path,destino,datos,sesion_activa)
    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("copy",params,res[0]["datos"])
    return respuesta
