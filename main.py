from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Mkdisk import *
from Rep import *
from Fdisk import *
from Rmdisk import *
from Mount import *
from Unmount import *
from Mkfs import *
from Login import *
from Logout import *
from Rmgrp import *
from Mkgrp import *
from Mkusr import *
from Rmusr import *
from Mkfile import *
from Cat import *
from Remove import *
from Edit import *
from Rename import *
from Mkdir import *
from Copy import *
from Move import *
from Find import *
from Chown import *
from Chgrp import *
from Chmod import *
from Recovery import *
from Loss import *

particiones_montadas = []
sesion_activa = None
ultimo_disco = ''
last_response = None

def interpretacion_de_comando(comando):
    comando = comando.split("#",1)[0].strip()
    if len(comando) == 0:
        return "", ""

    global ultimo_disco, sesion_activa, particiones_montadas
    respuesta = ""
    reporte = None
    params = [param.strip() for param in comando.split("-")]

    if params[0].lower() == 'mkdisk':
        respuesta = com_mkdisk(params[1:])
    elif params[0].lower() == 'rmdisk':
        respuesta = com_rmdisk(params[1:])
    elif params[0].lower() == 'fdisk':
        respuesta = com_fdisk(params[1:])
    elif params[0].lower() == 'mount':
        respuesta = com_mount(params[1:], particiones_montadas)
    elif params[0].lower() == 'lpm':
        respuesta = "Lista de particiones montadas\n"
        for p in particiones_montadas:
            respuesta += "--"+p["identificador"]
        respuesta += "\n\n"
    elif params[0].lower() == 'unmount':
        respuesta = com_unmount(params[1:], particiones_montadas)
    elif params[0].lower() == 'mkfs':
        respuesta = com_mkfs(params[1:], particiones_montadas)
    elif params[0].lower() == 'login':
        respuesta, sesion_activa = com_login(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'logout':
        respuesta, sesion_activa = com_logout(particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkgrp':
        respuesta = com_mkgrp(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'rmgrp':
        respuesta = com_rmgrp(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkusr':
        respuesta = com_mkusr(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'rmusr':
        respuesta = com_rmusr(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkfile':
        respuesta = com_mkfile(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'cat':
        respuesta = com_cat(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'remove':
        respuesta = com_remove(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'edit':
        respuesta = com_edit(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'rename':
        respuesta = com_rename(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkdir':
        respuesta = com_mkdir(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'copy':
        respuesta = com_copy(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'move':
        respuesta = com_move(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'find':
        respuesta = com_find(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'chown':
        respuesta = com_chown(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'chgrp':
        respuesta = com_chgrp(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'chmod':
        respuesta = com_chmod(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'pause':
        respuesta = "--Pausa\n\n"
    elif params[0].lower() == 'rep':
        respuesta, reporte = com_rep(params[1:], particiones_montadas)
    elif params[0].lower() == 'cl':
        particiones_montadas = []
        respuesta = "--se han limpiado las particiones cargadas\n\n"
    else:
        respuesta = "--Comando '"+params[0]+"' no reconocido"
        respuesta += "\n\n"

    return respuesta, reporte

def ejecutar_comandos(s):
    lineas = s.split("\n")
    for l in lineas:
        print("----------------------------------")
        interpretacion_de_comando(l)

def ejecutar(comandos):
    res = ""
    listaReportes = []
    lineas = comandos.split("\n")
    for l in lineas:
        res += "----------------------------------\n"
        res += l+"\n"
        res1, rep = interpretacion_de_comando(l)
        if rep:
            listaReportes.append(rep)
        res += res1
    return {"consola": res, "reportes": listaReportes}

app=Flask(__name__)
CORS(app)

@app.route("/ejecutar", methods=['POST'])
def procesar():
    global last_response
    comandos = request.data.decode().replace("\\n","\n").replace("\"","").replace("\\","")
    response = jsonify(ejecutar(comandos))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/logs", methods=['POST'])
def procesar1():
    global last_response
    c = request.data.decode().replace("\\n","\n").replace("\"","").replace("\\","")
    t, r = interpretacion_de_comando(c)
    response = jsonify({"mensaje":t.strip("\n")})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()
