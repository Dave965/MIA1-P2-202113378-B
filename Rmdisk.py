import os
def com_rmdisk(params):
    respuesta = ""
    path = None

    for x in params:
        param = [w.strip() for w in x.split("=")]
        if param[0].lower() != "path":
            respuesta +="--Parametro '"+param[0]+"' no reconocido para el comando 'rmdisk'"
            respuesta += "\n\n" 
            return respuesta
        
        if len(param)<2:
            respuesta +="--El parametro 'path' necesita una direccion"
            respuesta += "\n\n" 
            return respuesta

        if param[1][0] == '"':
            path = param[1][1:-1]
        else:
            path = param[1]

    if path == None:
        respuesta +="--No se encontro el parametro obligatorio 'path'"
        respuesta += "\n\n" 
        return respuesta

    if not os.path.isfile(path):
        respuesta +="--No existe un disco en '"+path+"'"
        respuesta += "\n\n" 
        return respuesta

    os.remove(path)
    respuesta +="--Disco removido con exito"
    respuesta += "\n\n" 
    return respuesta
