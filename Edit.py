from Clases import *
from Fhandler import *
import os

def com_edit(params, lista_particiones, sesion_activa):
    path = None
    cont = None
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

        if param[0].lower() == "cont":
            if param[1][0] == '"':
                cont = param[1][1:-1]
            else:
                cont = param[1]
                
    if not path:
        respuesta += ("--No se encontro el parametro obligatorio 'path'")
        respuesta += "\n\n"
        return respuesta

    if not cont:
        respuesta += ("--No se encontro el parametro obligatorio 'cont'")
        respuesta += "\n\n"
        return respuesta

    if not os.path.exists(cont):
        respuesta += ("--No existe un archivo en la ruta '"+cont+"'")
        respuesta += "\n\n"
        return respuesta

    with open(cont,"r") as f:
        texto_archivo = f.read()
        f.close()    

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
    estado, permiso, datos = revisar_permisos(path,datos,sesion_activa)
    res[0]["datos"] = datos 

    if not estado:
        respuesta += ("--La ruta no existe")
        respuesta += "\n\n"
        return respuesta
    
    if permiso[1] != "1":
        respuesta += ("--El usuario no tiene permiso de Escritura en el archivo "+path)
        respuesta += "\n\n"
        return respuesta

    if permiso[0] != "1":
        respuesta += ("--El usuario no tiene permiso de Lectura en el archivo "+path)
        respuesta += "\n\n"
        return respuesta

    datos = escribir_archivo(path, datos, texto_archivo)
    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("edit",params,res[0]["datos"])
    respuesta += ("--Se ha editado el archivo '"+path+"' de manera exitosa")
    respuesta += "\n\n"
    return respuesta
    
