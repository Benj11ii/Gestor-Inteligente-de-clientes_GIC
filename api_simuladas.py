## Este archivo contiene las validaciones con API externa REAL
## Usando Rapid Email Verifier (gratuito)

import requests
import time

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