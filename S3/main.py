# 🛠️ Taller Semana 1: El Núcleo del Agente y Control de Acceso
# Oscar Danilo Sanabria Sogamoso

from datetime import datetime
from typing import Dict, List, Tuple

# Darle un Alias a la estructura de memoria nos ayuda a trabajar con IA porque deja explícito
# qué forma tienen los recuerdos del agente, y así el código es más legible y más fácil de validar.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


def contar_letras(frase: str) -> Tuple[int, int, int]:
    """Cuenta vocales, consonantes y total de letras alfabéticas en una frase."""
    total_vocales = 0
    total_consonantes = 0
    for ch in frase.lower():
        if ch.isalpha():
            if ch in "aeiou":
                total_vocales += 1
            else:
                total_consonantes += 1
    total_letras = total_vocales + total_consonantes
    return total_vocales, total_consonantes, total_letras


def validar_password(nueva_password: str, usuario_actual: str) -> str:
    """Valida una contraseña según longitud mínima y si coincide con el usuario."""
    if len(nueva_password) < 8:
        return "[Rechazada] Debe tener al menos 8 caracteres."
    if nueva_password.lower() == usuario_actual.lower():
        return "[Rechazada] La contrasena no puede ser igual al nombre de usuario."
    return "[OK] Contrasena valida."


def calculadora(n1_txt: str, operador: str, n2_txt: str) -> str:
    """Ejecuta una operación matemática y retorna el resultado en texto."""
    n1 = float(n1_txt)
    n2 = float(n2_txt)

    if operador == "+":
        return f"Resultado: {n1 + n2}"
    if operador == "-":
        return f"Resultado: {n1 - n2}"
    if operador == "*":
        return f"Resultado: {n1 * n2}"
    if operador == "/":
        if n2 == 0:
            raise ZeroDivisionError("No se puede dividir entre cero.")
        return f"Resultado: {n1 / n2}"
    raise ValueError("Operador no valido.")


def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """Procesa acciones de historial (all, clear o búsqueda) y retorna texto formateado."""
    accion_normalizada = accion.strip().lower()

    if accion_normalizada == "all":
        if len(memoria) == 0:
            return "[PseudoAgente] El historial está vacío."
        salida = ["=== Historial Completo ==="]
        for i, registro in enumerate(memoria, 1):
            salida.append(f"\n[{i}] Timestamp: {registro['timestamp']}")
            salida.append(f"    Comando: {registro['cmd']}")
            salida.append(f"    Rol: {registro['rol']}")
            salida.append(f"    Descripción: {registro['descripcion']}")
        return "\n".join(salida)

    if accion_normalizada == "clear":
        memoria.clear()
        return "[PseudoAgente] Historial eliminado."

    palabra_clave = accion_normalizada
    if palabra_clave.startswith("buscar:"):
        palabra_clave = palabra_clave.split(":", 1)[1].strip().lower()

    if len(memoria) == 0:
        return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

    coincidencias: MemoriaAgente = []
    for registro in memoria:
        # Para saber si una palabra está "dentro" de otra usamos el operador in, y junto con .split()
        # podemos resolver singularidades del comando separando verbo y parámetro antes de comparar.
        if palabra_clave in registro["descripcion"].lower():
            coincidencias.append(registro)

    if len(coincidencias) == 0:
        return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

    salida = [
        f"=== Resultados de búsqueda para '{palabra_clave}' ===",
        f"Se encontraron {len(coincidencias)} coincidencia(s):",
    ]
    for i, registro in enumerate(coincidencias, 1):
        salida.append(f"\n[{i}] Autor: {registro['rol']}")
        salida.append(f"    Mensaje: {registro['descripcion']}")
        salida.append(f"    Timestamp: {registro['timestamp']}")
    return "\n".join(salida)


def obtener_fecha_hoy(rol_actual: str) -> str:
    """Retorna la fecha actual solo para usuarios admin."""
    if rol_actual != "admin":
        # Aquí lanzamos (raise) un error de permisos y ese error viaja al menú principal,
        # donde el bloque except lo atrapa para mostrar una alerta elegante sin crashear.
        raise PermissionError("Privilegios insuficientes")
    return datetime.now().strftime("%Y-%m-%d")

print("----- Sistema de Agente Seguro -----")

# Perfiles del sistema (usuario, password, rol)
# Esta constante esteblece un diccionario de datos con las credenciales de acceso.
CREDENCIALES = {
    "invitado": {"password": "user12", "rol": "invitado"},
    "admin": {"password": "admon12", "rol": "admin"},
}

usuario_actual = ""
rol_actual = ""
acceso_concedido = False
intentos = 0

# Este contador evita intentos infinitos: cada falla suma 1, y al llegar a 3
# cortamos el login para proteger el sistema de intentos repetidos.
while intentos < 3 and not acceso_concedido:
    usuario_ingresado = input("Usuario: ").strip().lower()
    password_ingresada = input("Contrasena: ").strip()
    # El método strip() elimina espacios en blanco al inicio y al final de la cadena, lo que ayuda a evitar errores de ingreso por espacios accidentales. El método lower() convierte el texto a minúsculas, permitiendo que el ingreso del usuario no sea sensible a mayúsculas o minúsculas.
    if (
        usuario_ingresado in CREDENCIALES
        and password_ingresada == CREDENCIALES[usuario_ingresado]["password"]
    ):
        acceso_concedido = True
        usuario_actual = usuario_ingresado
        rol_actual = CREDENCIALES[usuario_ingresado]["rol"]
        print(f"[OK] Bienvenido, {usuario_actual}. Rol: {rol_actual}")
    else:
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"[Error] Credenciales invalidas. Intentos restantes: {restantes}")

if not acceso_concedido:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
else:
    print("\nAgente activo. Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, salir")
    sistema_activo = True
    
    # Inicializar el historial de actividades del agente (lista de diccionarios con timestamp, cmd, rol, descripcion)
    historial_chat = []
    mensaje = ""

    while sistema_activo:
        cmd_entrada = input("PseudoAgente>: ").strip().lower()
        partes_cmd = cmd_entrada.split()
        try:
            cmd = partes_cmd[0]
        except IndexError:
            print("[Error] Debes ingresar un comando.")
            mensaje = "Entrada vacía de comando."
            continue

        if cmd == "salir":
            print("Apagando agente. Hasta luego.")
            mensaje = "Se ha solicitado terminar la sesión."
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")
            mensaje = "Se envió un ping y se devuelve un pong."

        elif cmd == "contar":
            frase = input("Ingresa una frase: ").strip().lower()
            total_vocales, total_consonantes, total_letras = contar_letras(frase)

            print(f"Frase: {frase}")
            print(f"Vocales: {total_vocales}")
            print(f"Consonantes: {total_consonantes}")
            mensaje = f"La palabra ingresada fue {frase} y se obtuvo como resultado: Vocales - {total_vocales} | Consonantes {total_consonantes} siendo el total: {total_letras}"

        elif cmd == "fecha_hoy":
            try:
                fecha_actual = obtener_fecha_hoy(rol_actual)
                print(f"Fecha actual: {fecha_actual}")
                mensaje = f"La fecha actual es: {fecha_actual}"
            except PermissionError as e:
                print(f"[Acceso Denegado] {e}")
                mensaje = str(e)

        elif cmd == "validar_pass":
            nueva_password = input("Ingresa una nueva propuesta de contrasena: ").strip()
            resultado_validacion = validar_password(nueva_password, usuario_actual)
            print(resultado_validacion)
            if resultado_validacion.startswith("[OK]"):
                mensaje = "Contraseña validada correctamente."
            elif "8 caracteres" in resultado_validacion:
                mensaje = "Contraseña rechazada: debe tener al menos 8 caracteres."
            else:
                mensaje = "Contraseña rechazada: no puede ser igual al nombre de usuario."

        elif cmd == "calculadora":
            # La función input() retorna texto. Si no convertimos a float, Python intentaria
            # sumar/castear strings y tendriamos errores de tipo en operaciones matematicas.
            n1_txt = input("Ingresa el primer numero: ").strip()
            operador = input("Ingresa el operador (+, -, *, /): ").strip()
            n2_txt = input("Ingresa el segundo numero: ").strip()

            # El bloque try-except captura errores de conversion (por ejemplo, si el usuario ingresa "abc" en lugar de un numero)
            try:
                resultado_calculadora = calculadora(n1_txt, operador, n2_txt)
                print(resultado_calculadora)
                mensaje = resultado_calculadora
            except ValueError as e:
            # Si ocurre un error de conversion, mostramos un mensaje de error y usamos 'continue' para saltar a la siguiente iteracion del bucle, evitando que el programa se caiga.
                if "Operador" in str(e):
                    print("[Error] Operador no valido.")
                    mensaje = "Operador no válido."
                else:
                    print("[Error] Debes ingresar valores numericos validos.")
                    mensaje = "Error en la calculadora: valores numéricos inválidos."
                # Registrar el error en el historial
                d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "cmd": cmd,
                        "rol": rol_actual,
                        "descripcion": mensaje}
                historial_chat.append(d_log)
                continue
            except ZeroDivisionError:
                print("[Error] No se puede dividir entre cero.")
                mensaje = "Error en división: intento de dividir entre cero."
                d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "cmd": cmd,
                        "rol": rol_actual,
                        "descripcion": mensaje}
                historial_chat.append(d_log)
                continue

        elif cmd == "historial":
            # Usando .split() podemos dividir el comando en sus partes para verificar si hay parámetros
            if len(partes_cmd) > 1:
                parametro = partes_cmd[1].lower()
                if parametro in ("all", "clear"):
                    resultado_historial = gestionar_historial(parametro, historial_chat)
                    print(resultado_historial)
                    if parametro == "all":
                        mensaje = "Se mostró el historial completo."
                    else:
                        mensaje = "Historial eliminado."
                else:
                    print("[PseudoAgente] Parámetro desconocido. Use 'historial all' o 'historial clear'.")
                    mensaje = "Parámetro de historial desconocido."
            else:
                # Modo búsqueda: el usuario ingresa una palabra clave
                palabra_clave = input("Ingresa la palabra clave a buscar: ").strip().lower()
                resultado_historial = gestionar_historial(f"buscar:{palabra_clave}", historial_chat)
                print(resultado_historial)
                if "No encontré" in resultado_historial:
                    mensaje = f"Búsqueda realizada por: {palabra_clave} (sin resultados)."
                else:
                    mensaje = f"Búsqueda realizada por: {palabra_clave} (con resultados)."

        else:
            print("Comando desconocido, intenta de nuevo.")
            mensaje = "Comando desconocido."
        
        # Registrar cada acción en el historial del agente (excepto historial clear que ya lo maneja)
        if cmd != "historial" or (len(partes_cmd) > 1 and partes_cmd[1].lower() != "clear"):
            d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cmd": cmd,
                    "rol": rol_actual,
                    "descripcion": mensaje}
            historial_chat.append(d_log)
