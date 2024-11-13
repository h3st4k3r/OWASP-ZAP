# OWASP ZAP API Scan

Este script utiliza OWASP ZAP para realizar un escaneo completo (Spider, AJAX Spider y Active Scan) sobre una API RESTful definida en un archivo Swagger. El script está diseñado para aprovechar configuraciones existentes en el contexto de OWASP ZAP.

## Requisitos

1. Tener OWASP ZAP ejecutándose en tu máquina o en un servidor accesible.
2. Configurar un contexto en ZAP con los usuarios y parámetros de autenticación requeridos.
3. Python 3 instalado con el paquete `python-owasp-zap-v2.4` en un entorno virtual.

## Configuración

Antes de ejecutar el script, edita los siguientes parámetros:

- **`zap_api_key`**: Tu clave API de OWASP ZAP.
- **`zap_base_url`**: La URL base de OWASP ZAP (normalmente `http://127.0.0.1:8080`).
- **`context_name`**: El nombre del contexto en OWASP ZAP.
- **`swagger_file_path`**: La ruta absoluta al archivo Swagger de tu API.

## Uso

1. **Instalar las dependencias**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install python-owasp-zap-v2.4
   ```

2. **Ejecutar el script**:
   ```bash
   python3 zap_api_scan.py
   ```
