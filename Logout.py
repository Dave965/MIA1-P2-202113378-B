from Clases import *
from Fhandler import *
import os

def com_logout(lista_particiones, sesion_activa):
    respuesta = ""
    if not sesion_activa:
        respuesta += "--No hay sesion activa"
        respuesta += "\n\n"
        return respuesta, sesion_activa

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        respuesta += "--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas"
        respuesta += "\n\n"

    sesion_activa = None
    respuesta += "Se ha cerrado sesion"
    respuesta += "\n\n"

    res[0]["datos"] = guardar_journaling("logout",[],res[0]["datos"])
    return respuesta, sesion_activa
