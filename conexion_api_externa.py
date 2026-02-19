## Este archivo contiene las validaciones con API externa REAL
## Usando Rapid Email Verifier (gratuito)

import requests
import time
import re

API_URL = "https://rapid-email-verifier.fly.dev/api/validate"

def validar_email_con_api(email, nombre):
    try:
        print(f"Conectando con servicio de validación...")
        time.sleep(0.5)

        # Llamada a la API
        response = requests.get(
            f"{API_URL}?email={email}",
            timeout=10
        )

        if response.status_code != 200:
            return False, f"Error en API (código {response.status_code})"

        data = response.json()
        
        # Analizar resultado
        status = data.get("status", "")
        
        if status == "VALID":
            return True, "Email válido"
        elif status == "DISPOSABLE":
            return False, "Email desechable (temporal) no permitido"
        elif status == "INVALID_FORMAT":
            return False, "Formato de email inválido"
        elif status == "INVALID_DOMAIN":
            return False, "El dominio del email no existe"
        else:
            return False, f"Email no válido (estado: {status})"

    except requests.exceptions.ConnectionError:
        return False, "Error de conexión con la API"
    except requests.exceptions.Timeout:
        return False, "Tiempo de espera agotado"
    except Exception as e:
        return False, f"Error: {str(e)}"


def enviar_email_bienvenida(email, nombre):
    print(f"\nSimulando envío de email de bienvenida a {nombre}...")
    time.sleep(0.5)
    print(f"Email de bienvenida registrado en logs (simulado)")
    return True

def validar_formato_id(id_cliente, nombre):
    """
    Valida que el ID tenga formato: 3 letras + _ + 3 números
    Ejemplo: abc_123
    """
    try:
        print(f"🔍 Validando formato de ID: {id_cliente}...")
        time.sleep(0.5)  # Simula tiempo de procesamiento

        # Patrón: 3 letras (mayúsculas o minúsculas) + guión bajo + 3 números
        patron = r'^[A-Za-z]{3}_\d{3}$'

        if re.match(patron, id_cliente):
            print(f"Formato de ID válido para {nombre}")
            return True
        else:
            print(f"Formato incorrecto. Debe ser: 3 letras + _ + 3 números")
            print(f"   Ejemplos válidos: abc_123, XYZ_789, pqr_456")
            return False
    except Exception as e:
        print(f"⚠️ Error en validación de formato: {e}")
        return False