# Simulador de chatbot de prestamo bancario

## Descripción del Proyecto

Simulador de chatbot de prestamo bancario desarrollado en Python que simula el proceso de pedir un prestamo. El programa permite:

- Identificarse en el programa usando usuarios del archivo `usuarios.csv`
- Solicitar un préstamo bancario en base a un margen pre-establecido.
- Confirmar transacción y actualizar margen en archivo `usuarios.csv`

La arquitectura del proyecto está consolidada en un único archivo `main.py`, diseñado de forma modular, con funciones de responsabilidad única y usando constantes globales.

## Datos de la Universidad y la Cátedra

- **Universidad:** Universidad Tecnológica Nacional (UTN) — Modalidad a Distancia
- **Cátedra:** Organización Empresarial
- **Coordinador:** Gabriela Martinez
- **Año:** 2026

## Profesores

- Andrea Ramos
- Mario Lopez
- Carolina Bruno

## Tutores

- Martina Zabala
- Esteban Varberde

## Integrantes

- Nehuel Mendoza - Comisión M26 C1-27
- Matías Burgos - Comisión M26 C1-20


## Estructura del Proyecto

```
Simulador-de-chatbot-de-prestamo-bancario/
├── main.py        # Lógica principal del sistema: menú, CRUD, filtros, orden y estadísticas
├── usuarios.csv      # Archivo de datos con la información de los países
├── diagram.bpmn    # Archivo .bpmn con el diagrama BPMN 2.0
├── diagram.svg     # Imagen del diagrama BPMN 2.0
├── pruebas_y_casos
│          ├── caso_exito.png
│          ├── caso_exito_parcial.png
│          └── caso_rechazo.png
├── .gitignore      # Reglas para el archivo gitignore
└── README.md       # Este archivo
```

## Instrucciones de Ejecución

1. **Clonar el repositorio** (opción recomendada):
   ```bash
   git clone https://github.com/1mendoza/Simulador-de-chatbot-de-prestamo-bancario.git
   ```
   O bien, **descargar el proyecto como .zip** desde GitHub: botón verde **"Code"** → **"Download ZIP"**, y descomprimir la carpeta.

2. **Abrir la carpeta del proyecto en Visual Studio Code** (`File → Open Folder`).

3. **Verificar que Python esté instalado** (versión 3.x). Se puede comprobar con:
   ```bash
   python --version
   ```

4. **Ejecutar el programa** desde una terminal integrada de VS Code (`Terminal → New Terminal`):
   ```bash
   python main.py
   ```

5. **Identificarse con credenciales correctas.** Usuario: mgomez Clave: clave123. Usuarios para acceder al programa en `usuarios.csv`

6. **Utilizar el menú interactivo** que se muestra en consola para navegar entre las distintas opciones.
(1. Solicitar préstamo / 2. Salir)
(- Ingresar monto a solicitar - Esperar confirmación/denegación/confirmación parcial - Aceptar/denegar monto máximo)

## Uso de Librerías de Terceros

El proyecto utiliza únicamente módulos de la librería estándar de Python, por lo que no requiere instalación de dependencias externas (`pip install`):


## Links

- [**Repositorio de GitHub**](https://github.com/1mendoza/Simulador-de-chatbot-de-prestamo-bancario/)
- [**Documentación**](https://drive.google.com/file/d/1p2p700wSmsnw05I5Knfvj_BZzCo4r08p/view?usp=sharing)

## Ejemplos de Entrada y Salida

[**Caso de éxito**](pruebas_y_casos/caso_exito.png)

[**Caso de éxito parcial**](pruebas_y_casos/caso_exito_parcial.png)

[**Caso de rechazo**](pruebas_y_casos/caso_rechazo.png)


