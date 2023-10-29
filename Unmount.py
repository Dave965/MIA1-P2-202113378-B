from Clases import *
from Fhandler import *
import os

def com_unmount(params, lista_particiones):
    respuesta = ""
    identificador = None
    contenido = None
    for x in params:
        param = [w.strip() for w in x.split("=")]

        if len(param) != 2:
            respuesta +="--Error en el parametro '"+param[0]+"', parametro incompleto"
            respuesta += "\n\n"
            return respuesta

        if param[0].lower() == "id":
            identificador = param[1]

    if identificador == None:
        respuesta +="--No se encontro el parametro obligatorio 'id'"
        respuesta += "\n\n"
        return respuesta


    res = [x for x in lista_particiones if x["identificador"] == identificador]
    if len(res) == 0:
        respuesta +="--No existe el id '"+identificador+"' entre las particiones cargadas"
        respuesta += "\n\n"
        return respuesta

    res[0]["datos"] = umSb(res[0]["datos"])
    path = res[0]["path"]
    name = res[0]["nombre"]
    
    mbr = MBR()
    with open(path,"rb") as f:
        mbr.deserializar(f.read())
        f.close()

    part = None
    ext = False
    cont = None
    extendida = None
    
    for x in mbr.mbr_partition:
        if x.part_name.decode().strip('\x00') == name:
            part = x
            break

    if part == None:
        extendida = [x for x in mbr.mbr_partition if x.part_type.decode().lower() == "e"]
        if len(extendida) != 0:
            extendida = extendida[0]
            with open(path,"rb") as f:
                f.seek(extendida.part_start)
                contenido = f.read(extendida.part_s)
                f.close()
            ebr = EBR()
            porcion = contenido 
            aceptados = ["1","0"]
            while True:
                ebr.deserializar(porcion)
                if ebr.part_name.decode().strip('\x00') == name:
                    part = ebr
                    ext = True
                    cont = contenido
                    break
                if ebr.part_status.decode() not in aceptados or ebr.part_next == -1:
                    break
                porcion = contenido[ebr.part_next:]

    part.setStatus("0")

    if ext:
        data_serializada = part.serializar()+res[0]["datos"]
        pre = cont[:part.part_start-sizeEBR]
        post = cont[part.part_start-sizeEBR+len(data_serializada):]
        cont = pre+data_serializada+post

        with open(path,'r+b') as d:
            pre = d.read()[:extendida.part_start]
            d.seek(0)
            post = d.read()[extendida.part_start+extendida.part_s:]
            d.seek(0)
            d.write(pre+cont+post)
            d.close()
        
        data_serializada = mbr.serializar()

        with open(path,'r+b') as d:
            post = d.read()[len(data_serializada):]
            d.seek(0)
            d.write(data_serializada)
            d.write(post)
            d.close()
            
    else:
        with open(path,"rb") as f:
            f.seek(part.part_start)
            contenido = f.read()[part.part_s:]
            f.close()

        data_serializada = mbr.serializar()

        with open(path,'r+b') as d:
            post = d.read()[len(data_serializada):]
            d.seek(0)
            d.write(data_serializada)
            d.write(post)
            d.seek(part.part_start)
            d.write(res[0]["datos"])
            d.write(contenido)
            d.close()

    lista_particiones.remove(res[0])
    respuesta +="Particion '"+name+"' desmontada con exito"
    respuesta += "\n\n"
    return respuesta
