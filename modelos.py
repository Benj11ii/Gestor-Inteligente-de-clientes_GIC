##Este archivo es para poder contener las instrucciones de clases, getter y setter

from typing import List
from datetime import datetime

## Clase para registrar actividad de clientes, definir esto inicialmente ayuda a usarla luego cuando se crea la clase padre cliente
class RegistroActividad:
    def __init__(self, fecha_hora, accion, detalle, id_cliente):
        self._fecha_hora = fecha_hora
        self._accion = accion
        self._detalle = detalle
        self._id_cliente = id_cliente

    ## Parámetros para mostrar los log, función importante para consultar posteriormente.
    def mostrar_log(self):
        return (f"[{self._fecha_hora}] "
                f"{self._accion}: "
                f"{self._detalle} (Cliente: "
                f"{self._id_cliente})")

    ## Uso de diccionario para el archivo a crear json
    def to_dict(self):
        return {
            "fecha_hora": self._fecha_hora.isoformat() if isinstance(self._fecha_hora, datetime) else self._fecha_hora,
            "accion": self._accion,
            "detalle": self._detalle,
            "id_cliente": self._id_cliente
        }

    ##Usar un classmethod para el diccionario.
    @classmethod
    def from_dict(cls, datos):
        # Convertir string ISO a datetime
        fecha = datetime.fromisoformat(datos["fecha_hora"]) if isinstance(datos["fecha_hora"], str) else datos[
            "fecha_hora"]
        return cls(fecha, datos["accion"], datos["detalle"], datos["id_cliente"])


## Definición de la clase padre, la principal de la cual heredaran las demás, que son tipos de clientes.
class Cliente:
    def __init__(self, id_cliente, nombre, email, telefono, direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self._email = None  ##Definir inicialmente, para luego usar con setter de forma correcta
        self._telefono = None ##Definir privado como email
        self._direccion = None ##Definir privado igual que email y telefono
        self.activo = True
        self.logs: List[RegistroActividad] = []
        self.email = email ## llamar al setter
        self.telefono = telefono ## llamar al setter
        self.direccion = direccion ## llamar al setter

    ##Usé un getter para usar el tipo de cliente
    @property
    def tipo(self):
        nombre_clase = self.__class__.__name__
        # Convertir nombres de clase a algo más amigable
        tipos = {
            'ClienteRegular': 'Regular',
            'ClientePremium': 'Premium',
            'ClienteCorporativo': 'Corporativo'
        }
        return tipos.get(nombre_clase, nombre_clase)

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, nueva_direccion):
        # Validación simple, no vacía, mínimo 10 caracteres
        if nueva_direccion and len(nueva_direccion.strip()) >= 10:
            self._direccion = nueva_direccion.strip()
        else:
            print(f"Dirección muy corta para {self.nombre}. Mínimo 10 caracteres.")
            self._direccion = "Dirección no válida"

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        # Convertir a string por si acaso
        nuevo_telefono = str(nuevo_telefono)

        # Validación simple: solo números y +, entre 9 y 12 caracteres
        import re
        if re.match(r'^\+?\d{9,12}$', nuevo_telefono):
            self._telefono = nuevo_telefono
        else:
            print(
                f"Teléfono '{nuevo_telefono}' no válido para {self.nombre}. Debe tener 9-12 dígitos, puede empezar con +")
            self._telefono = "000000000"  # Valor por defecto

    @property
    def email(self):
        return self._email

    ##Validador en el setter para correo
    @email.setter
    def email(self, nuevo_email):
        # Validación robusta
        import re
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', nuevo_email):
            self._email = nuevo_email
        else:
            print(f"Email '{nuevo_email}' no válido para {self.nombre}. Formato: usuario@dominio.com")
            self._email = "invalido@email.com"

    # Definición de método para mostrar el perfil de clientes.
    def mostrar_perfil(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"Tipo: {self.tipo} | ID: {self.id_cliente} | Nombre: {self.nombre} | Email: {self.email} | Estado: {estado}"

    # Definición de método para agregar el log de forma correcta
    def agregar_log(self, accion, detalle):
        log = RegistroActividad(datetime.now(), accion, detalle, self.id_cliente)
        self.logs.append(log)
        return log

    # Definición de logs
    def mostrar_logs(self):
        if not self.logs:
            return f"El cliente {self.nombre} no tiene actividades registradas."
        resultado = f"Logs de {self.nombre}:\n"
        for log in self.logs:
            resultado += f"  • {log.mostrar_log()}\n"
        return resultado

    # Método para convertir al cliente en diccionario y así trabajarlo con json
    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "email": self._email,  # Guardamos el email real
            "telefono": self.telefono,
            "direccion": self.direccion,
            "activo": self.activo,
            "tipo": self.__class__.__name__,  # Guardamos el tipo de cliente
            "logs": [log.to_dict() for log in self.logs]  # Lista de logs como diccionarios
        }
    # Método de clase para crear al cliente desde el diccionario json, deacuerdo al tipo de cliente y datos que se ingresan.
    @classmethod
    def from_dict(cls, datos):
        tipo = datos.get("tipo", "Cliente")

        if tipo == "ClienteRegular":
            cliente = ClienteRegular(
                datos["id_cliente"],
                datos["nombre"],
                datos["email"],
                datos["telefono"],
                datos["direccion"],
                datos.get("puntos", 0)  # Usamos get con valor por defecto
            )
        elif tipo == "ClientePremium":
            cliente = ClientePremium(
                datos["id_cliente"],
                datos["nombre"],
                datos["email"],
                datos["telefono"],
                datos["direccion"],
                datos["membresia_vence"]
            )
        elif tipo == "ClienteCorporativo":
            cliente = ClienteCorporativo(
                datos["id_cliente"],
                datos["nombre"],
                datos["email"],
                datos["telefono"],
                datos["direccion"],
                datos["rut_empresa"]
            )
        else:
            cliente = ClienteRegular(
                datos["id_cliente"],
                datos["nombre"],
                datos["email"],
                datos["telefono"],
                datos["direccion"],
                datos.get("puntos", 0)
            )

        # Restaurar estado
        cliente.activo = datos.get("activo", True)

        # Restaurar logs si existen
        if "logs" in datos:
            for log_data in datos["logs"]:
                log = RegistroActividad.from_dict(log_data)
                cliente.logs.append(log)

        return cliente

    ##Método especial para imprimir el objeto como texto adornado
    def __str__(self):

        return f"{self.nombre} (ID: {self.id_cliente})"

    ##Método especial para comparar si dos clientes son iguales (==)
    # Dos clientes son iguales si tienen el mismo ID
    def __eq__(self, otro):

        if isinstance(otro, Cliente):
            return self.id_cliente == otro.id_cliente
        return False

## Clases hijas, heredan de Cliente
class ClienteRegular(Cliente):
    def __init__(self, id_cliente, nombre, email, telefono, direccion, puntos=0):
        super().__init__(id_cliente, nombre, email, telefono, direccion)
        # Aquí se pueden agregar atributos específicos de Regular más adelante
        self.puntos = puntos

    def to_dict(self):
        datos = super().to_dict()
        datos["puntos"] = self.puntos
        return datos

        # Sobrescribimos el método para mostrar los puntos
    def mostrar_perfil(self):
        perfil_base = super().mostrar_perfil()
        return f"{perfil_base} | Puntos: {self.puntos}"


class ClientePremium(Cliente):
    def __init__(self, id_cliente, nombre, email, telefono, direccion, membresia_vence):
        super().__init__(id_cliente, nombre, email, telefono, direccion)
        # Aquí se pueden agregar atributos específicos de Premium
        self.membresia_vence = membresia_vence
        self.descuento = 0.20  # 20% de descuento

    def to_dict(self):
        datos = super().to_dict()  # Trae id, nombre, email, etc.
        datos["membresia_vence"] = self.membresia_vence
        return datos

    def aplicar_descuento(self, monto):
        return monto * (1 - self.descuento)

    def mostrar_perfil(self):
        perfil_base = super().mostrar_perfil()
        return f"{perfil_base} | Membresía vence: {self.membresia_vence}"


class ClienteCorporativo(Cliente):
    def __init__(self, id_cliente, nombre, email, telefono, direccion, rut_empresa):
        super().__init__(id_cliente, nombre, email, telefono, direccion)
        # Aquí se pueden agregar atributos específicos de Corporativo
        self.rut_empresa = rut_empresa  # Identificación para procesar factura

    def to_dict(self):
        datos = super().to_dict()
        datos["rut_empresa"] = self.rut_empresa  # ← IMPORTANTE: agregar este campo
        return datos

    def generar_factura_empresa(self):
        return f"Facturando a nombre de: {self.nombre} (rut_empresa: {self.rut_empresa})"

    def mostrar_perfil(self):
        perfil_base = super().mostrar_perfil()
        # Aquí se demuestra el proceso de clienteCorporativo que genera factura
        info_factura = self.generar_factura_empresa()
        return f"{perfil_base} | {info_factura}"