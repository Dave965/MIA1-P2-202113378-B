from Clases import *
from Fhandler import *
import os

def com_rename(params, lista_particiones, sesion_activa):
    path = None
    name = None
    respuesta = ""
    
    if not sesion_activa:
        respuesta += ("--Este comando requiere una sesion activa")
        respuesta += "\n\n"
        return respuesta
    
    for x in params:
        param = [w.strip() for w in x.split("=")]

        if param[0].lower() == "r":
            r = True
        elif len(param) != 2:
            respuesta += ("--Error en el parametro '"+param[0]+"', parametro incompleto")
            respuesta += "\n\n"
            return respuesta 

        if param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        if param[0].lower() == "name":
            if param[1][0] == '"':
                name = param[1][1:-1]
            else:
                name = param[1]
                
    if not path:
        respuesta += ("--No se encontro el parametro obligatorio 'path'")
        respuesta += "\n\n"
        return respuesta

    if not name:
        respuesta += ("--No se encontro el parametro obligatorio 'name'")
        respuesta += "\n\n"
        return respuesta

    if len(name) > 12:
        respuesta += ("--El nombre puede tener como maximo 12 caracteres")
        respuesta += "\n\n"
        return respuesta

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        respuesta += ("--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas")
        respuesta += "\n\n"
        return respuesta

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        respuesta += ("--La particion aun no ha sido formateada")
        respuesta += "\n\n"
        return respuesta
    conjunto = path.rsplit("/",1)
    ruta = conjunto[0]
    archivo = conjunto[1]

    estado, permiso, datos = revisar_permisos(ruta+"/"+name,datos,sesion_activa)
    res[0]["datos"] = datos 
    if estado:
        respuesta += ("--Ya existe una ruta con el nuevo nombre")
        respuesta += "\n\n"
        return respuesta

    estado, permiso, datos = revisar_permisos(path,datos,sesion_activa)
    res[0]["datos"] = datos
    
    if permiso[1] != "1":
        respuesta += ("--El usuario no tiene permiso de Escritura en la ruta "+path)
        respuesta += "\n\n"
        return respuesta

    estado, datos = cambiar_nombre(path, datos, name, sesion_activa)
    res[0]["datos"] = datos
    
    res[0]["datos"] = guardar_journaling("rename",params,res[0]["datos"])
    respuesta += ("--Se ha Cambiado el nombre de la ruta '"+path+"' de manera exitosa")
    respuesta += "\n\n"
    return respuesta
