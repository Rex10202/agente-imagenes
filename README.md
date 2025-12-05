# Agente generador de imágenes

Este proyecto implementa un agente que genera imágenes a partir de una descripción en lenguaje natural, evaluando la calidad de las imágenes y seleccionando la mejor según una función de utilidad.

El agente combina:
- Un generador de imágenes (vía API HTTP).
- Una ontología en formato RDF/Turtle.
- Módulos de evaluación cuantitativa de la imagen.
- Validación de restricciones mediante SHACL.

## Estructura del proyecto

- `src/`
  - `run_agent.py`: punto de entrada por línea de comandos.
  - `agent.py`: lógica principal del agente (bucle de generación–evaluación–selección).
  - `generator.py`: funciones para llamar al generador de imágenes (peticiones HTTP).
  - `evaluation.py`: métricas de evaluación de las imágenes.
  - `ontology.py`: carga y manejo de la ontología.
  - `shacl_validate.py`: validación con SHACL.
  - `config.py`: configuración (rutas, parámetros, etc.).
  - `http_client.py`, `utils.py`: utilidades varias.
- `data/`
  - `ontologia_agente_imagenes.ttl`: ontología en formato Turtle usada por el agente.
- `scripts/`
  - `reproduce_results.py`: script para reproducir resultados.
  - `validate_ontology.py`: script para validar la ontología.
- `workflows/`
  - `*.json`: definición de workflows externos (por ejemplo, N8N).
- `outputs/`
  - Se guardan aquí las imágenes generadas y otros resultados (carpeta ignorada en Git).
- `.venv/`
  - Entorno virtual de Python (ignorado en Git).
- `requirements.txt`
  - Dependencias de Python del proyecto.

## Requisitos

- Python 3.10 o 3.11 (recomendado).
- `git` instalado (solo para clonar el repositorio).
- Dependencias Python listadas en `requirements.txt`.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Rex10202/agente-imagenes.git
cd agente-imagenes
```

Crear y activar un entorno virtual (ejemplo en Windows PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Uso

Ejecutar el agente desde la raíz del proyecto:

```bash
python .\src\run_agent.py -d "una descripción de prueba"
```

Parámetros:

- `-d`, `--descripcion` (obligatorio): descripción en lenguaje natural de la imagen que se quiere generar.

Salida esperada (ejemplo):

```text
OK
Best U: 0.923
Imagen: outputs/imagen_mejor.png
Traza:  [...]
```

Las imágenes y resultados intermedios se guardan normalmente en la carpeta `outputs/`.

## Datos

- `data/ontologia_agente_imagenes.ttl`: ontología utilizada por el agente para razonar sobre:
  - Conceptos relacionados con imágenes.
  - Atributos y restricciones.
  - Validaciones mediante SHACL (ver `shacl_validate.py`).

## Scripts auxiliares

Desde la raíz del proyecto (con el entorno virtual activado):

```bash
python .\scripts\validate_ontology.py
python .\scripts\reproduce_results.py
```

Estos scripts son opcionales y se usan para tareas de validación y reproducción de resultados.

## Contribuciones

Las contribuciones y sugerencias son bienvenidas mediante *issues* y *pull requests* en este repositorio.

## Licencia

(Indica aquí la licencia que quieras usar, por ejemplo MIT, Apache 2.0, etc.)
