import os
import platform
import requests
import json
from requests.auth import HTTPBasicAuth

# --- 1. DATOS DEL ALUMNO (MODIFICAR AQUÍ) ---
JIRA_DOMAIN = "tu-dominio"
EMAIL = "tu_correo@ejemplo.com"
API_TOKEN = "tu_token"
PROJECT_KEY = "tu_clave"

# --- 2. EXTRACCIÓN DE HARDWARE ---
hostname = platform.node()
os_info = f"{platform.system()} {platform.release()}"
ip_address = os.popen('hostname -I').read().strip().split()[0]
ram_gb = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.**3), 2)

descripcion = f"""
*Reporte de CMDB Automatizado:*
* Hostname: {hostname}
* IP Privada: {ip_address}
* OS: {os_info}
* RAM: {ram_gb} GB
"""

# --- 3. ENVÍO A JIRA ---
url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/2/issue"
payload = json.dumps({
  "fields": {
    "project": {"key": PROJECT_KEY},
    "summary": f"[CMDB] Auto-Inventario: {hostname}",
    "description": descripcion,
    "issuetype": {"name": "Task"}
  }
})
headers = {"Accept": "application/json", "Content-Type": "application/json"}

print("Conectando con Jira API...")
response = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth(EMAIL, API_TOKEN))

if response.status_code == 201:
    print("✅ ¡Éxito! Activo registrado en Jira.")
else:
    print(f"❌ Error {response.status_code}: Revisa tus credenciales.")
