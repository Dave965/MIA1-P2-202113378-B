from Clases import *
from Fhandler import *
import os

def com_rmgrp(params, lista_particiones, sesion_activa):
    name = None
    respuesta=""

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

        if param[0].lower() == "name":
            if param[1][0] == '"':
                name = param[1][1:-1]
            else:
                name = param[1]

    if not name:
        respuesta += "--No se encontro el parametro obligatorio 'name'"
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
    grupo = None

    try:
        grupo = [x for x in grupos if x[2] == name][0]
    except:
        respuesta += "--No existe el grupo con nombre '"+name+"' entre los grupos creados"
        respuesta += "\n\n"
        return respuesta

    usuarios_grupo = [x for x in usuarios if x[2] == name and x[0] != "0"]

    if len(usuarios_grupo) > 0:
        respuesta += "--No se puede eliminar el grupo con nombre '"+name+"' porque tiene usuarios activos"
        respuesta += "\n\n"
        return respuesta

    texto = ""
    
    for linea in usuarios:
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    for linea in grupos:
        if linea == grupo:
            continue
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    texto+= "0,"+grupo[1]+","+grupo[2]+"\n"
    
    res[0]["datos"] = escribir_archivo("/users.txt", res[0]["datos"], texto)
    res[0]["datos"] = guardar_journaling("rmgrp",params,res[0]["datos"])
    respuesta += "Grupo '"+name+"' eliminado exitosamente"
    respuesta += "\n\n"
    return respuesta
    
    
        
    
    
    
    
