from Clases import *
from Fhandler import *
import os

def com_rep(params,lista_particiones):
    name = None
    path = None
    identificador = None
    ruta = None
    respuesta = ""
    reporte = None

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            respuesta +=("--Error en el parametro '"+param[0]+"', parametro incompleto")
            respuesta += "\n\n"
            return respuesta, reporte
        if param[0].lower() == "name":
            if param[1][0] == '"':
                name = param[1][1:-1]
            else:
                name = param[1]

        if param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        if param[0].lower() == "id":
            if param[1][0] == '"':
                identificador = param[1][1:-1]
            else:
                identificador = param[1]

        if param[0].lower() == "ruta":
            if param[1][0] == '"':
                ruta = param[1][1:-1]
            else:
                ruta = param[1]

    if not name:
        respuesta +=("--No se encontro el parametro obligatorio 'name'")
        respuesta += "\n\n"
        return respuesta, reporte

    if not path:
        respuesta +=("--No se encontro el parametro obligatorio 'path'")
        respuesta += "\n\n"
        return respuesta, reporte

    if not identificador:
        respuesta +=("--No se encontro el parametro obligatorio 'id'")
        respuesta += "\n\n"
        return respuesta, reporte

    res = [x for x in lista_particiones if x["identificador"] == identificador]
    if len(res) == 0:
        respuesta +=("--No existe el id '"+identificador+"' entre las particiones cargadas")
        respuesta += "\n\n"
        return respuesta, reporte

    datos = res[0]["datos"]


    if name == "tree":
        estado = integridadSB(datos)
        if not estado:
            respuesta +=("--La particion aun no ha sido formateada")
            respuesta += "\n\n"
            return respuesta, reporte
        s = repTree(datos)
        reporte = {"tipo": "g", "name":path,"rep":s}

    elif name == "bm_block":
        estado = integridadSB(datos)
        if not estado:
            respuesta +=("--La particion aun no ha sido formateada")
            respuesta += "\n\n"
            return respuesta, reporte
        reporte = {"tipo": "t", "name":path,"rep":repBitmap(datos,"b")}

    elif name == "bm_inode":
        estado = integridadSB(datos)
        if not estado:
            respuesta +=("--La particion aun no ha sido formateada")
            respuesta += "\n\n"
            return respuesta, reporte
        reporte = {"tipo": "t", "name":path,"rep":repBitmap(datos,"i")}

    elif name == "sb":
        estado, s = repSB(datos)
        if not estado:
            respuesta +=("--La particion aun no ha sido formateada")
            respuesta += "\n\n"
            return respuesta, reporte
        reporte = {"tipo": "g", "name":path,"rep":s}

    elif name == "file":
        estado = integridadSB(datos)
        if not estado:
            respuesta +=("--La particion aun no ha sido formateada")
            respuesta += "\n\n"
            return respuesta, reporte
        if ruta == None:
            respuesta +=("--No se encontro el parametro obligatorio 'ruta'")
            respuesta += "\n\n"
            return respuesta, reporte
        s, datos = traer_archivo(ruta,datos)
        reporte = {"tipo": "t", "name":path,"rep":s}
        
    elif name == "disk":
        p = res[0]["path"]
        mbr = MBR()
        with open(p,"rb") as f:
            mbr.deserializar(f.read())
            f.close()
        reporte = {"tipo": "g", "name":path,"rep":mbr.showdisk(p)}

    elif name == "mbr":
        p = res[0]["path"]
        mbr = MBR()
        with open(p,"rb") as f:
            mbr.deserializar(f.read())
            f.close()
        reporte = {"tipo": "g", "name":path,"rep":mbr.imprimir(p)}
        
    else:
        respuesta +=("--No se reconoce el nombre del reporte")

    datos = res[0]["datos"]
    respuesta +=("Reporte creado con exito")
    respuesta += "\n\n"
    return respuesta, reporte
