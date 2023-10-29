from Clases import *
from Fhandler import *
import os

def com_chmod(params, lista_particiones, sesion_activa):
    path = None
    ugo = None
    r = False
    respuesta = ""

    if not sesion_activa:
        respuesta +=("--Este comando requiere una sesion activa")
        respuesta += "\n\n"
        return respuesta
    
    if sesion_activa["user"] != "root":
        respuesta +=("--Solo el usuario root puede ejecutar este comando")
        respuesta += "\n\n"
        return respuesta

    for x in params:
        param = [w.strip() for w in x.split("=")]

        if param[0].lower() == "r":
            r = True
            continue
        
        if len(param) != 2:
            respuesta +=("--Error en el parametro '"+param[0]+"', parametro incompleto")
            respuesta += "\n\n"
            return respuesta 

        if param[0].lower() == "ugo":
            if param[1][0] == '"':
                ugo = param[1][1:-1]
            else:
                ugo = param[1]

        elif param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

    if ugo == None:
        respuesta +=("--No se encontro el parametro obligatorio 'ugo'")
        respuesta += "\n\n"
        return respuesta

    if path == None:
        respuesta +=("--No se encontro el parametro obligatorio 'path'")
        respuesta += "\n\n"
        return respuesta 

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        respuesta +=("--No existe el id '"+identificador+"' entre las particiones cargadas")
        respuesta += "\n\n"
        return respuesta 

    perms = []
    try:
        for i in ugo:
            perms.append(int(i))
    except:
        respuesta +=("--El parametro ugo debe ser numerico")
        respuesta += "\n\n"
        return respuesta

    for i in perms:
        if i<0 or i>7:
            respuesta +=("--Los permisos deben ser un numero del 0 al 7")
            respuesta += "\n\n"
            return respuesta

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        respuesta +=("--La particion aun no ha sido formateada")
        respuesta += "\n\n"
        return respuesta
    
    if r:
        datos = cambiar_permiso_r(path, datos, sesion_activa, perms[0], perms[1], perms[2])
    else:
        datos = cambiar_permiso(path, datos, sesion_activa, perms[0], perms[1], perms[2])
    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("chmod",params,res[0]["datos"])
    respuesta +=("Se han actualizado los permisos de la ruta")
    respuesta += "\n\n"
    return respuesta 
