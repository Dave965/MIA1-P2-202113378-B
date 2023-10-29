from Clases import *
from Fhandler import *
import os

def com_mkdir(params, lista_particiones, sesion_activa):
    path = None
    r = False
    respuesta =""


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
                
    if not path:
        respuesta += ("--No se encontro el parametro obligatorio 'path'")
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

    estado, permiso, datos = revisar_permisos(path,datos,sesion_activa)
    if estado:
        respuesta += ("--Ya existe una carpeta con ese nombre")
        respuesta += "\n\n"
        return respuesta 
    
    if r:
        estado, datos = crear_ruta(path,datos,sesion_activa)
        if not estado:
            res[0]["datos"] = datos 
            return respuesta
    else:
        estado, permiso, datos = revisar_permisos(ruta,datos,sesion_activa)
        res[0]["datos"] = datos 
        if not estado:
            respuesta += ("--La ruta no existe")
            respuesta += "\n\n"
            return respuesta
        
        if permiso[1] != "1":
            respuesta += ("--El usuario no tiene permiso de Escritura en la carpeta "+ruta)
            respuesta += "\n\n"
            return respuesta
            
        estado, datos = crear_carpeta(path,datos,sesion_activa)
        res[0]["datos"] = datos
        
        if not estado:
            respuesta += ("--No se pudo crear la carpeta")
            respuesta += "\n\n"
            return respuesta

    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("mkdir",params,res[0]["datos"])
    respuesta += ("Se ha creado la carpeta '"+path+"' de manera exitosa")
    respuesta += "\n\n"
    return respuesta
