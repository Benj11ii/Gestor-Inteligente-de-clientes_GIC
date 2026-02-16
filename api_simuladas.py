##Este archivo es para poder contener las validaciones y para simular el uso de API externa
import time
import re

def validar_formato_id(id_cliente, nombre):
    try:
        print(f"Validando ID: {id_cliente}...")
        time.sleep(1)  # Simula tiempo de procesamiento como si fuera una API externa real

        # Validar formato: 3 letras, guión bajo, 3 números
        patron = r'^[A-Za-z]{3}_\d{3}$'

        if re.match(patron, id_cliente):
            print(f"Identidad validada para {nombre}")
            return True
        else:
            print(f"Formato incorrecto. Debe ser: 3 letras + _ + 3 números (ej: aaa_111)")
            return False
    except Exception as e:
        print(f"Error en validación: {e}")
        return False


def enviar_email_bienvenida(email, nombre):
     try:
        print(f"\nEnviando email de bienvenida a {email}...")
        # Simulación
        if "@" in email:
            print(f"Email enviado a {nombre}")
            time.sleep(1) # Simula tiempo de procesamiento como si fuera una API externa real
            return True
        else:
            print(f"Email inválido, no se pudo enviar")
            return False
     except Exception as e:
        print(f"Error al enviar email: {e}")
        return False