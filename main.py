"""
=============================================================
 SIMULADOR DE CHATBOT - SOLICITUD DE PRÉSTAMO BANCARIO
=============================================================
 Trabajo Práctico Integrador - Organización Empresarial
 Tecnicatura Universitaria en Programación

 Descripción:
 Simula el flujo conversacional de un chatbot bancario que
 evalúa solicitudes de préstamo según el margen disponible
 del usuario, siguiendo el modelo BPMN 2.0 definido para
 este proceso.

 El programa implementa una Máquina de Estados Finitos (FSM)
 para llevar el control de en qué paso del proceso se
 encuentra cada usuario, y persiste los cambios de margen
 en un archivo CSV que actúa como base de datos simulada.
=============================================================
"""

import csv
import os
import sys

# -------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------------------

ARCHIVO_USUARIOS = "usuarios.csv"
MARGEN_MINIMO = 50000          # Por debajo de esto, no se otorga ningún préstamo
MAX_INTENTOS_LOGIN = 3         # Establece un limite de intentos fallidos por seguridad y bloquea el sistema una vez alcanzado el limite.

# Estados posibles de la máquina de estados
ESTADO_LOGIN = "LOGIN"
ESTADO_MENU = "MENU"
ESTADO_MONTO = "MONTO"
ESTADO_EVALUACION = "EVALUACION"
ESTADO_CONFIRMAR_REDUCIDO = "CONFIRMAR_REDUCIDO"
ESTADO_FIN = "FIN"


# -------------------------------------------------------------
# FUNCIONES DE PERSISTENCIA (CSV como base de datos simulada)
# -------------------------------------------------------------

def cargar_usuarios(ruta_archivo):
    """
    Lee el archivo CSV y devuelve una lista de diccionarios,
    uno por cada usuario registrado.
    """
    usuarios = []
    try:
        with open(ruta_archivo, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                fila["margen_disponible"] = float(fila["margen_disponible"])
                usuarios.append(fila)
    except FileNotFoundError:
        print(f"\n No se encontró el archivo '{ruta_archivo}'.")
        sys.exit(1)
    return usuarios


def guardar_usuarios(ruta_archivo, usuarios):
    """
    Reescribe el archivo CSV completo con los datos actualizados.
    Se usa luego de aprobar un préstamo, para descontar el margen.
    """
    campos = ["usuario", "contraseña", "margen_disponible"]
    with open(ruta_archivo, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for u in usuarios:
            escritor.writerow(u)


def buscar_usuario(usuarios, nombre_usuario):
    """Busca un usuario por nombre dentro de la lista. Devuelve el dict o None."""
    for u in usuarios:
        if u["usuario"] == nombre_usuario:
            return u
    return None


# -------------------------------------------------------------
# FUNCIONES DE INTERFAZ (entrada/salida amigable)
# -------------------------------------------------------------

def encabezado(titulo):
    print("\n" + "=" * 55)
    print(f" {titulo}")
    print("=" * 55)


def linea():
    print("-" * 55)


def pedir_si_no(mensaje):
    """
    Pide al usuario una respuesta sí/no, validando la entrada
    hasta recibir una opción reconocida (camino infeliz).
    """
    while True:
        respuesta = input(f"{mensaje} (si/no): ").strip().lower()
        if respuesta in ("si", "sí", "s"):
            return True
        elif respuesta in ("no", "n"):
            return False
        else:
            print(">> Respuesta no reconocida. Por favor escribí 'si' o 'no'.")


def pedir_monto(mensaje):
    """
    Pide un monto numérico positivo al usuario, validando
    errores de entrada (texto, negativos, vacío).
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            monto = float(entrada)
            if monto <= 0:
                print(">> El monto debe ser un número positivo. Intentá de nuevo.")
                continue
            return monto
        except ValueError:
            print(">> Entrada inválida. Ingresá solo números (ej: 100000).")


def formato_pesos(monto):
    """Formatea un número como moneda para mostrar en pantalla."""
    return f"${monto:,.0f}".replace(",", ".")


# -------------------------------------------------------------
# ESTADO: LOGIN
# -------------------------------------------------------------

def estado_login(usuarios):
    """
    Gestiona el ingreso de credenciales. Permite reintentos
    hasta MAX_INTENTOS_LOGIN; si se agotan, finaliza el programa.
    Devuelve el usuario autenticado o None si se agotaron los intentos.
    """
    encabezado("BIENVENIDO AL BOT DE PRÉSTAMOS")
    print("Por favor, ingresá tus credenciales para continuar.\n")

    intentos = 0
    while intentos < MAX_INTENTOS_LOGIN:
        nombre = input("Usuario: ").strip()
        clave = input("Contraseña: ").strip()

        usuario_encontrado = buscar_usuario(usuarios, nombre)

        if usuario_encontrado is not None and usuario_encontrado["contraseña"] == clave:
            print(f"\n>> ¡Bienvenido/a, {nombre}!")
            return usuario_encontrado
        else:
            intentos += 1
            restantes = MAX_INTENTOS_LOGIN - intentos
            if restantes > 0:
                print(f">> Usuario o contraseña incorrectos. Te quedan {restantes} intento(s).\n")
            else:
                print(">> Se agotaron los intentos disponibles.")

    return None


# -------------------------------------------------------------
# ESTADO: MENÚ PRINCIPAL
# -------------------------------------------------------------

def estado_menu():
    """
    Muestra el menú principal y devuelve la opción elegida
    como entero validado (1 o 2).
    """
    encabezado("MENÚ PRINCIPAL")
    print("1. Solicitar préstamo")
    print("2. Salir")
    linea()

    while True:
        opcion = input("Elegí una opción (1-2): ").strip()
        if opcion in ("1", "2"):
            return int(opcion) 
        else:
            print(">> Opción inválida. Elegí 1 o 2.")

def traer_margen(usuario):
    margen = usuario["margen_disponible"]
    return margen
# -------------------------------------------------------------
# ESTADO: EVALUACIÓN DEL PRÉSTAMO (Gateway principal)
# -------------------------------------------------------------

def evaluar_prestamo(usuario, monto_solicitado, usuarios):
    """
    Implementa el gateway principal de decisión del proceso BPMN:

      - Camino feliz: margen >= monto solicitado
      - Camino parcial: margen_minimo <= margen < monto solicitado
      - Camino de rechazo: margen < margen_minimo

    Actualiza el CSV si el préstamo se aprueba (total o parcial).
    """
    margen = usuario["margen_disponible"]

    encabezado("EVALUACIÓN DE LA SOLICITUD")
    print(f"Monto solicitado: {formato_pesos(monto_solicitado)}")
    print(f"Margen disponible: {formato_pesos(margen)}")
    linea()

    # --- CAMINO 1: FELIZ ---
    if margen >= monto_solicitado:
        usuario["margen_disponible"] -= monto_solicitado
        guardar_usuarios(ARCHIVO_USUARIOS, usuarios)
        print(">> ✅ PRÉSTAMO APROBADO")
        print(f">> Se aprobó el monto completo de {formato_pesos(monto_solicitado)}.")
        print(f">> Nuevo margen disponible: {formato_pesos(usuario['margen_disponible'])}")
        return

    # --- CAMINO 3: RECHAZO TOTAL ---
    if margen < MARGEN_MINIMO:
        print(">> ❌ PRÉSTAMO RECHAZADO")
        print(">> Tu margen disponible no alcanza el mínimo requerido")
        print(f">> para acceder a cualquier línea de préstamo ({formato_pesos(MARGEN_MINIMO)}).")
        return

    # --- CAMINO 2: APROBACIÓN PARCIAL ---
    print(">> ⚠️  MARGEN INSUFICIENTE PARA EL MONTO SOLICITADO")
    print(f">> El máximo que podemos ofrecerte es: {formato_pesos(margen)}")
    linea()

    acepta = pedir_si_no("¿Deseás continuar la operación por ese monto?")

    if acepta:
        monto_final = margen
        usuario["margen_disponible"] -= monto_final
        guardar_usuarios(ARCHIVO_USUARIOS, usuarios)
        print("\n>> ✅ PRÉSTAMO APROBADO (monto ajustado)")
        print(f">> Se aprobó el monto de {formato_pesos(monto_final)}.")
        print(f">> Nuevo margen disponible: {formato_pesos(usuario['margen_disponible'])}")
    else:
        print("\n>> Operación cancelada por el usuario.")
        print(">> No se realizaron cambios en tu cuenta.")


# -------------------------------------------------------------
# FLUJO DE SOLICITUD DE PRÉSTAMO (orquesta los estados MONTO -> EVALUACION)
# -------------------------------------------------------------

def flujo_solicitud_prestamo(usuario, usuarios):
    encabezado("SOLICITUD DE PRÉSTAMO")
    margen = usuario["margen_disponible"]
    print(f"Margen disponible: {formato_pesos(margen)} ")
    monto = pedir_monto("Ingresá el monto que deseás solicitar: $")
    evaluar_prestamo(usuario, monto, usuarios)


# -------------------------------------------------------------
# PROGRAMA PRINCIPAL (orquesta la máquina de estados)
# -------------------------------------------------------------

def main():
    usuarios = cargar_usuarios(ARCHIVO_USUARIOS)
    estado_actual = ESTADO_LOGIN
    usuario_actual = None

    while estado_actual != ESTADO_FIN:

        if estado_actual == ESTADO_LOGIN:
            usuario_actual = estado_login(usuarios)
            if usuario_actual is None:
                print("\n>> Sesión finalizada por exceso de intentos fallidos.")
                estado_actual = ESTADO_FIN
            else:
                estado_actual = ESTADO_MENU

        elif estado_actual == ESTADO_MENU:
            opcion = estado_menu()
            if opcion == 1:
                estado_actual = ESTADO_MONTO
            else:  # opcion == 2
                estado_actual = ESTADO_FIN

        elif estado_actual == ESTADO_MONTO:
            flujo_solicitud_prestamo(usuario_actual, usuarios)
            estado_actual = ESTADO_MENU  # vuelve al menú tras cada operación

    encabezado("FIN DE LA SESIÓN")
    print("Gracias por utilizar nuestro servicio. ¡Hasta pronto!\n")


if __name__ == "__main__":
    main()
