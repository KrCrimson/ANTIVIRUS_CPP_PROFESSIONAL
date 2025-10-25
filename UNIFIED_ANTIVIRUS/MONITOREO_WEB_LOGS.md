# Sistema de Monitoreo Web de Logs para Antivirus

Este documento describe los pasos para implementar una solución que recopile los logs generados por el antivirus en cada PC y los envíe a un servidor web centralizado, donde el administrador podrá visualizar métricas y estadísticas desde una vista web.

## 1. Envío de Logs desde cada PC
- Modificar el antivirus para que lea los logs locales (por ejemplo, `logs/antivirus.log`).
- Implementar una función que envíe los datos del log periódicamente a un servidor web mediante una petición HTTP POST (por ejemplo, usando la librería `requests`).
- Ejemplo de código:

```python
import requests
with open('logs/antivirus.log', 'r', encoding='utf-8') as f:
    log_data = f.read()
requests.post('https://TU_SERVIDOR/api/recibir_log', json={'pc_id': 'PC123', 'log': log_data})
```

## 2. Backend Web para Recibir y Almacenar Logs
- Crear un servidor web (Flask, FastAPI, Django, etc.) que exponga una API para recibir los logs.
- Almacenar los logs recibidos en una base de datos o archivos.
- Ejemplo básico con Flask:

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/api/recibir_log', methods=['POST'])
def recibir_log():
    data = request.get_json()
    pc_id = data['pc_id']
    log = data['log']
    # Guardar log en base de datos o archivo
    return {'status': 'ok'}

app.run(host='0.0.0.0', port=5000)
```

## 3. Dashboard Web para Visualizar Métricas
- Desarrollar una vista web (puede ser con Flask, Django, FastAPI + frontend JS) que lea los logs almacenados y muestre métricas, gráficos y estadísticas.
- Usar librerías como Chart.js, Plotly, o simplemente HTML+CSS para mostrar los datos.
- Ejemplo de endpoint para métricas:

```python
@app.route('/admin/dashboard')
def dashboard():
    # Leer logs y calcular métricas
    return render_template('dashboard.html', metrics=metrics)
```

## 4. Seguridad y Autenticación
- Proteger el acceso al dashboard con autenticación (login de administrador).
- Validar los datos recibidos y limitar el tamaño/frecuencia de los envíos.

## 5. Despliegue
- Hospedar el backend web en un servidor accesible por todas las PCs.
- Configurar el antivirus para enviar los logs al servidor.
- Acceder al dashboard web como administrador para visualizar las métricas.

---

**Notas:**
- Puedes adaptar los ejemplos a tus necesidades y tecnologías preferidas.
- Es recomendable usar HTTPS para proteger la transmisión de datos.
- Puedes agregar más endpoints para reportes, descargas de logs, etc.
