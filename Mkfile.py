from Clases import *
from Fhandler import *
import os

def com_mkfile(params, lista_particiones, sesion_activa):
    path = None
    r = False
    size = 0
    cont = None
    respuesta=""

    cadena = "0123456789"
    texto_archivo = ""

    if not sesion_activa:
        respuesta += "--Este comando requiere una sesion activa"
        respuesta += "\n\n"
        return respuesta
    
    for x in params:
        param = [w.strip() for w in x.split("=")]

        if param[0].lower() == "r":
            r = True
        elif len(param) != 2:
            respuesta += "--Error en el parametro '"+param[0]+"', parametro incompleto"
            respuesta += "\n\n"
            return respuesta

        if param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        if param[0].lower() == "size":
            try:
                size = int(param[1])
            except:
                respuesta += "--Size debe ser un numero positivo"
                respuesta += "\n\n"
                return respuesta

        if param[0].lower() == "cont":
            if param[1][0] == '"':
                cont = param[1][1:-1]
            else:
                cont = param[1]
                
    if not path:
        respuesta += "--No se encontro el parametro obligatorio 'path'"
        respuesta += "\n\n"
        return respuesta

    texto_archivo = cadena*int(size/10)+cadena[:(size%10)]
        
    if cont:
        if not os.path.exists(cont):
            respuesta += "--No existe un archivo en la ruta '"+cont+"'"
            respuesta += "\n\n"
            return respuesta

        with open(cont,"r") as f:
            texto_archivo = f.read()
            f.close()    

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
    conjunto = path.rsplit("/",1)
    ruta = conjunto[0]
    archivo = conjunto[1]

    estado, permiso, datos = revisar_permisos(path,datos,sesion_activa)
    if estado:
        respuesta += "--Ya existe un archivo con ese nombre"
        respuesta += "\n\n"
        return respuesta 
    
    if r:
        estado, datos = crear_ruta(ruta,datos,sesion_activa)
        if not estado:
            res[0]["datos"] = datos 
            return respuesta

        estado, datos = crear_archivo(path,datos,sesion_activa)
        if not estado:
            res[0]["datos"] = datos 
            respuesta += "--No se pudo crear el archivo"
            respuesta += "\n\n"
            return respuesta
        
    else:
        estado, permiso, datos = revisar_permisos(ruta,datos,sesion_activa)
        res[0]["datos"] = datos 
        if not estado:
            respuesta += "--La ruta no existe"
            respuesta += "\n\n"
            return respuesta
        
        if permiso[1] != "1":
            respuesta += "--El usuario no tiene permiso de Escritura en la carpeta "+ruta
            respuesta += "\n\n"
            return respuesta
            
        estado, datos = crear_archivo(path,datos,sesion_activa)
        res[0]["datos"] = datos 
        if not estado:
            respuesta += "--No se pudo crear el archivo"
            respuesta += "\n\n"
            return respuesta

    datos = escribir_archivo(path, datos, texto_archivo)
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("mkfile",params,res[0]["datos"])
    respuesta += "Se ha creado el archivo '"+path+"' de manera exitosa"
    respuesta += "\n\n"
    return respuesta
