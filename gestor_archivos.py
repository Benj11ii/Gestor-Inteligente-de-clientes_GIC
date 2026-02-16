##Este archivo es para poder contener los procesos que implican manipulación de archivo en formato json

import json
import os
from modelos import ClienteRegular, ClientePremium, ClienteCorporativo, Cliente

ARCHIVO_CLIENTES = "clientes.json"

def guardar_clientes(lista_clientes):
    try:
        # Convertir cada cliente a diccionario
        datos = [cliente.to_dict() for cliente in lista_clientes]

        with open(ARCHIVO_CLIENTES, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        print(f"{len(lista_clientes)} cliente(s) guardado(s) en {ARCHIVO_CLIENTES}")
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False


def cargar_clientes():
    if not os.path.exists(ARCHIVO_CLIENTES):
        print("Archivo no encontrado, se creará uno nuevo al guardar")
        return []

    try:
        with open(ARCHIVO_CLIENTES, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        # Convertir cada diccionario a objeto Cliente
        clientes = []
        for item in datos:
            # Usar el método de clase para reconstruir
            cliente = Cliente.from_dict(item)
            clientes.append(cliente)
        print("Mensaje informativo inicial.")
        print(f"{len(clientes)} cliente(s) cargado(s) desde {ARCHIVO_CLIENTES}")
        return clientes
    except Exception as e:
        print(f"Error al cargar: {e}")
        return []

##Función auxiliar para mostrar clientes
def mostrar_clientes_cargados(clientes):
    if not clientes:
        print("No hay clientes para mostrar")
        return

    print("\n" + "=" * 50)
    print("CLIENTES EN MEMORIA")
    print("=" * 50)
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente.mostrar_perfil()}")
        # Mostrar también los logs si existen
        if cliente.logs:
            print(cliente.mostrar_logs())
    print("=" * 50)

