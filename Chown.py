from Clases import *
from Fhandler import *
import os

def com_chown(params, lista_particiones, sesion_activa):
    path = None
    user = None
    r = False
    respuesta = ""

    if not sesion_activa:
        respuesta +=("--Este comando requiere una sesion activa")
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

        if param[0].lower() == "user":
            if param[1][0] == '"':
                user = param[1][1:-1]
            else:
                user = param[1]

        elif param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

    if user == None:
        respuesta +=("--No se encontro el parametro obligatorio 'user'")
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

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        respuesta +=("--La particion aun no ha sido formateada")
        respuesta += "\n\n"
        return respuesta
    users_creados, datos = traer_archivo("/users.txt", datos)
    lineas = users_creados.split("\n")
    usuarios = [x.split(",") for x in lineas if len(x.split(",")) == 5]
    grupos = [x.split(",") for x in lineas if len(x.split(",")) == 3]

    try:
        usuarios = [x for x in usuarios if x[3] == user][0]
    except:
        respuesta +=("--No existe el usuario con el nombre '"+user+"' en la particion")
        respuesta += "\n\n"
        return respuesta 

    if usuarios[0] == "0":
        respuesta +=("--El usuario con el nombre '"+user+"' ha sido borrado")
        respuesta += "\n\n"
        return respuesta

    grupo = [x for x in grupos if x[2] == usuarios[2]][0]

    uid = int(usuarios[0])
    gid = int(grupo[0])

    if r:
        datos = cambiar_propietario_r(path, datos, sesion_activa, uid, gid)
    else:
        datos = cambiar_propietario(path, datos, sesion_activa, uid, gid)
    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("chown",params,res[0]["datos"])
    respuesta +=("Se ha actualizado el propietario de la ruta")
    respuesta += "\n\n"
    return respuesta 
