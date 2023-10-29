from Clases import *
from Fhandler import *
import os

def com_mkusr(params, lista_particiones, sesion_activa):
    respuesta = ""
    user = None
    password = None
    grp = None

    if not sesion_activa:
        respuesta += "--Este comando requiere una sesion activa"
        respuesta += "\n\n"
        return respuesta

    if sesion_activa["user"] != "root":
        respuesta += "--Solo el usuario root puede ejecutar este comando"
        respuesta += "\n\n"
        return respuesta

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            respuesta += "--Error en el parametro '"+param[0]+"', parametro incompleto"
            respuesta += "\n\n"
            return respuesta 

        if param[0].lower() == "user":
            if param[1][0] == '"':
                user = param[1][1:-1]
            else:
                user = param[1]

        if param[0].lower() == "pass":
            if param[1][0] == '"':
                password = param[1][1:-1]
            else:
                password = param[1]

        if param[0].lower() == "grp":
            if param[1][0] == '"':
                grp = param[1][1:-1]
            else:
                grp = param[1]


    if not user:
        respuesta += "--No se encontro el parametro obligatorio 'user'"
        respuesta += "\n\n"
        return respuesta

    if not password:
        respuesta += "--No se encontro el parametro obligatorio 'pass'"
        respuesta += "\n\n"
        return respuesta

    if not grp:
        respuesta += "--No se encontro el parametro obligatorio 'grp'"
        respuesta += "\n\n"
        return respuesta

    if len(user) > 10:
        respuesta += "--El nombre de usuario debe tener como maximo 10 caracteres"
        respuesta += "\n\n"
        return respuesta

    if len(password) > 10:
        respuesta += "--El password del usuario debe tener como maximo 10 caracteres"
        respuesta += "\n\n"
        return respuesta
    
    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        respuesta += "--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas"
        respuesta += "\n\n"
        return respuesta

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        respuesta += "--La particion aun no ha sido formateada"
        respuesta += "\n\n"
        return respuesta
    users_creados, datos = traer_archivo("/users.txt", datos)
    lineas = users_creados.split("\n")
    usuarios = [x.split(",") for x in lineas if len(x.split(",")) == 5]
    grupos = [x.split(",") for x in lineas if len(x.split(",")) == 3]
    us = [x for x in usuarios if x[3] == user]
    grupo = [x for x in grupos if x[2] == grp]

    if len(us) > 0:
        respuesta += "--Ya existe un usuario con nombre '"+user+"' entre los usuarios creados"
        respuesta += "\n\n"
        return respuesta

    if len(grupo) < 1:
        respuesta += "--No existe un grupo con nombre '"+grp+"' entre los grupos creados"
        respuesta += "\n\n"
        return respuesta

    if grupo[0] == "0":
        respuesta += "--El grupo '"+grp+"' fue eliminado."
        respuesta += "\n\n"
        return respuesta

    texto = ""
    
    for linea in usuarios:
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    texto+= str(len(usuarios)+1)+",U,"+grp+","+user+","+password+"\n"

    for linea in grupos:
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    
    
    datos = escribir_archivo("/users.txt", datos, texto)
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("mkusr",params,res[0]["datos"])
    
    respuesta += "Usuario '"+user+"' creado exitosamente"
    respuesta += "\n\n"
    return respuesta
