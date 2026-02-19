# Este es el archivo para el menu inicial
import os
import re
from modelos import ClienteRegular, ClientePremium, ClienteCorporativo
from gestor_archivos import guardar_clientes, cargar_clientes
from conexion_api_externa import validar_formato_id, enviar_email_bienvenida
from conexion_api_externa import validar_email_con_api

## Muestra las opciones del menu
def mostrar_menu():
    print("\n" + "~" * 50)
    print("GESTOR INTELIGENTE DE CLIENTES (GIC)")
    print("~" * 50)
    print("1. Ver clientes registrados")
    print("2. Agregar nuevo cliente")
    print("3. Eliminar cliente")
    print("4. Editar cliente")
    print("5. Guardado automático y Salir del programa")
    print("~" * 50)

##Función para ver clientes
def ver_clientes(clientes):
    if not clientes:
        print("\nNo hay clientes registrados.")
        return

    print(f"\nTotal de clientes: {len(clientes)}")
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente.mostrar_perfil()}") ##Aquí se utiliza desde modelos la gestión mostrar perfil

##Función para agregar clientes de acuerdo al tipo de cliente y sus atributos
def agregar_cliente(clientes):
    print("\n" + "-" * 40)
    print("AGREGAR NUEVO CLIENTE")
    print("-" * 40)

    # 1. Seleccionar tipo de cliente
    print("Tipos de cliente:")
    print("1. Regular (con puntos)")
    print("2. Premium (con membresía)")
    print("3. Corporativo (Rut Empresa)")
    print("4. Volver al menu principal")

    while True:
        tipo_opcion = input("Seleccione tipo de cliente (1-3) o 4 para volver a menu: ")
        if tipo_opcion in ['1', '2', '3', '4']:
            break
        else:
            print("Opción no válida. Debe ser 1, 2, 3 o 4.")
    if tipo_opcion == '4':
        print("Operación cancelada. Volviendo al menú principal...")
        return clientes  # Retorna sin cambios

    # 2. Datos comunes a todos los clientes
    print("\n--- Datos básicos ---")
    while True:
        id_cliente = input("ID del cliente (formato aaa_111): ")

        print("\n--- Validando identidad ---")
        if validar_formato_id(id_cliente, "Cliente"):  # Validamos aquí
            break  # Sale del bucle SOLO si es válido
        else:
            print("Intente nuevamente con el formato correcto (ej: abc_123)\n")

    nombre = input("Nombre: ")
    #Validación con API externa en mail.
    while True:
        email = input("Email: ")
        
        try:
            print("\n--- Validando email con API externa ---")
            es_valido, mensaje = validar_email_con_api(email, nombre)
            
            if es_valido:
                print("✅ Email validado exitosamente por API externa")
                break  # Sale del bucle SOLO si la API dice que es válido
            else:
                print(f"❌ {mensaje}")
                print("Debe ingresar un email válido. Intente nuevamente.\n")
                
        except Exception as e:
            print(f"❌ Error al conectar con API de validación: {e}")
            print("No se puede continuar sin validar el email.")
            print("Intente nuevamente más tarde o con otro email.\n")    
    
    #Validación para teléfono sencilla
    while True:
        telefono = input("Teléfono (ej: 56912345678): ")
        try:
            if re.match(r'^\+?\d{9,15}$', telefono):
                break
            else:
                print("Teléfono no válido. Debe tener 9-15 dígitos (ej: 56912345678)")
        except Exception as e:
            print(f"Error en validación de teléfono: {e}. Intente nuevamente.")
    while True:
        direccion = input("Dirección (mínimo 10 caracteres): ")
        if len(direccion.strip()) >= 10:
            break
        else:
            print("Dirección muy corta. Mínimo 10 caracteres.")

    # Crear según el tipo de cliente
    if tipo_opcion == '1':
        puntos = input("Puntos iniciales (0 por defecto): ")
        try:
            puntos = int(puntos) if puntos else 0
        except ValueError:
            print("Valor no numérico para puntos. Usando 0 por defecto.")
            puntos = 0
        nuevo = ClienteRegular(id_cliente, nombre, email, telefono, direccion, puntos)
        print("Cliente Regular agregado")

    elif tipo_opcion == '2':
        membresia = "31-12-2030"
        nuevo = ClientePremium(id_cliente, nombre, email, telefono, direccion, membresia)
        print("Cliente Premium agregado (membresía válida hasta 31-12-2030)")

    elif tipo_opcion == '3':
        rut_empresa = input("Rut de la empresa: ")
        nuevo = ClienteCorporativo(id_cliente, nombre, email, telefono, direccion, rut_empresa)
        print("Cliente Corporativo agregado")

    ##Enviar correo de bienvenida (simulación de API externa)
    enviar_email_bienvenida(email, nombre)

    #Agregar log automático de creación
    nuevo.agregar_log("CREACIÓN", "Cliente creado desde el menú")
    nuevo.agregar_log("EMAIL", "Email de bienvenida enviado")

    #Añadir el valor a la lista
    clientes.append(nuevo)
    print(f"Cliente agregado correctamente. Total: {len(clientes)}")
    guardar_clientes(clientes)

    return clientes

##Función para eliminar clientes
def eliminar_cliente(clientes):
    if not clientes:
        print("\nNo hay clientes para eliminar.")
        return clientes

    print("\n" + "-" * 40)
    print("ELIMINAR CLIENTE")
    print("-" * 40)

    # Mostrar lista resumida para que el usuario elija, y así saber cuál cliente se puede eliminar
    print("Clientes disponibles:")
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente.nombre} (ID: {cliente.id_cliente})")

    print("\nOpciones de eliminación:")
    print("1. Eliminar por número de lista")
    print("2. Eliminar por ID")
    print("3. Cancelar")

    opcion = input("Seleccione una opción (1-3): ")

    if opcion == '1':
        try:
            num = int(input(f"Número de cliente a eliminar (1-{len(clientes)}): "))
            if 1 <= num <= len(clientes):
                cliente_eliminado = clientes.pop(num - 1)
                print(f"Cliente '{cliente_eliminado.nombre}' eliminado correctamente.")
                guardar_clientes(clientes)
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Debe ingresar un número válido.")
        except IndexError:
            print("Error inesperado al eliminar.")

    elif opcion == '2':
        id_buscar = input("Ingrese el ID del cliente a eliminar: ")
        encontrados = [c for c in clientes if c.id_cliente == id_buscar]

        if not encontrados:
            print(f"No se encontró cliente con ID '{id_buscar}'.")
        elif len(encontrados) == 1:
            cliente = encontrados[0]
            confirmacion = input(f"¿Eliminar a '{cliente.nombre}'? (s/n): ")
            if confirmacion.lower() == 's':
                clientes.remove(cliente)
                print(f"Cliente '{cliente.nombre}' eliminado correctamente.")
            else:
                print("Eliminación cancelada.")
        else:
            # Caso raro de IDs duplicados (no debería pasar) // sólo lo agregué como precaución
            print(f"Se encontraron {len(encontrados)} clientes con ese ID.")
            for c in encontrados:
                print(f"  - {c.nombre}")
            confirmacion = input("¿Eliminar TODOS? (s/n): ")
            if confirmacion.lower() == 's':
                for c in encontrados:
                    clientes.remove(c)
                print(f"{len(encontrados)} clientes eliminados.")

    else:
        print("Operación cancelada.")

    return clientes

##Función para editar datos de clientes ya creados
def editar_cliente(clientes):
    print("\n" + "-" * 40)
    print("EDITAR CLIENTE")
    print("-" * 40)

    if not clientes:
        print("\nNo hay clientes para editar.")
        return clientes

    # Mostrar lista resumida para que el usuario elija, y así saber cuál cliente se puede editar
    print("Clientes disponibles:")
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente.nombre} (ID: {cliente.id_cliente})")

    #Pedir id o indice del cliente para editar
    cliente_elegido = input("\nIngrese el número de lista o el ID del cliente a editar: ")
    cliente_a_editar = None
    if cliente_elegido.isdigit():
        indice = int(cliente_elegido) - 1
        if 0 <= indice < len(clientes):
            cliente_a_editar = clientes[indice]

        #Si no se encontró por número (o no era número), buscamos por ID textual
    if not cliente_a_editar:
        for c in clientes:
            if c.id_cliente == cliente_elegido:
                cliente_a_editar = c
                break
    if not cliente_a_editar:
        print(f"No se encontró ningún cliente con el ID '{cliente_elegido}'.")
        return clientes

    print(f"\nEditando a: {cliente_a_editar.nombre}")
    print("Deje en blanco si no desea cambiar el dato.")

    # Editar Nombre
    nuevo_nombre = input(f"Nuevo nombre ({cliente_a_editar.nombre}): ")
    if nuevo_nombre:
        cliente_a_editar.nombre = nuevo_nombre

    # Editar Teléfono (aprovechando el setter con validación)
    nuevo_telefono = input(f"Nuevo teléfono ({cliente_a_editar.telefono}): ")
    if nuevo_telefono:
        cliente_a_editar.telefono = nuevo_telefono  # Esto activa tu validación automática del setter

    # Editar Email
    nuevo_email = input(f"Nuevo email ({cliente_a_editar.email}): ")
    if nuevo_email:
        cliente_a_editar.email = nuevo_email  # Esto activa tu validación automática del setter

    print("Datos actualizados correctamente.")
    cliente_a_editar.agregar_log("EDICIÓN", "Se actualizaron datos del perfil")
    guardar_clientes(clientes) ## Se agrega línea para guardar cambios igual que se hizo con eliminar y agregar clientes
    return clientes


##Función principal del menu
def ejecutar(clientes):
    try:
        if os.path.exists("clientes.json"):
            clientes = cargar_clientes()
            print("Archivo revisado en formato JSON")
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        print("Comenzando con lista vacía")
        clientes = []

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")
        if opcion == '1':
            ver_clientes(clientes)
        elif opcion == '2':
            clientes = agregar_cliente(clientes)
        elif opcion == '3':
            clientes = eliminar_cliente(clientes)
        elif opcion == '4':
            clientes = editar_cliente(clientes)
        elif opcion == '5':
            guardar_clientes(clientes)
            print("\n¡Gracias por usar el GIC!. Hasta pronto.")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
