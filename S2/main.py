# 🛠️ Taller Semana 1: El Núcleo del Agente y Control de Acceso
# Oscar Danilo Sanabria Sogamoso

from datetime import datetime

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
        cmd = input("PseudoAgente>: ").strip().lower()

        if cmd == "salir":
            print("Apagando agente. Hasta luego.")
            mensaje = "Se ha solicitado terminar la sesión."
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")
            mensaje = "Se envió un ping y se devuelve un pong."

        elif cmd == "contar":
            frase = input("Ingresa una frase: ").strip().lower()
            total_vocales = 0
            total_consonantes = 0

            for ch in frase:
                # El método isalpha() verifica si el caracter es una letra del alfabeto. Esto nos permite ignorar espacios, números y signos de puntuación en el conteo de vocales y consonantes.
                if ch.isalpha():
                    if ch in "aeiou":
                        total_vocales += 1
                    else:
                        total_consonantes += 1

            print(f"Frase: {frase}")
            print(f"Vocales: {total_vocales}")
            print(f"Consonantes: {total_consonantes}")
            mensaje = f"La palabra ingresada fue {frase} y se obtuvo como resultado: Vocales - {total_vocales} | Consonantes {total_consonantes} siendo el total: {len(frase)}"

        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                print(f"Fecha actual: {fecha_actual}")
                mensaje = f"La fecha actual es: {fecha_actual}"
            else:
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
                mensaje = "Este comando requiere privilegios de administrador."

        elif cmd == "validar_pass":
            nueva_password = input("Ingresa una nueva propuesta de contrasena: ").strip()

            if len(nueva_password) < 8:
                print("[Rechazada] Debe tener al menos 8 caracteres.")
                mensaje = "Contraseña rechazada: debe tener al menos 8 caracteres."
            elif nueva_password.lower() == usuario_actual.lower():
                print("[Rechazada] La contrasena no puede ser igual al nombre de usuario.")
                mensaje = "Contraseña rechazada: no puede ser igual al nombre de usuario."
            else:
                print("[OK] Contrasena valida.")
                mensaje = "Contraseña validada correctamente."

        elif cmd == "calculadora":
            # La función input() retorna texto. Si no convertimos a float, Python intentaria
            # sumar/castear strings y tendriamos errores de tipo en operaciones matematicas.
            n1_txt = input("Ingresa el primer numero: ").strip()
            operador = input("Ingresa el operador (+, -, *, /): ").strip()
            n2_txt = input("Ingresa el segundo numero: ").strip()

            # El bloque try-except captura errores de conversion (por ejemplo, si el usuario ingresa "abc" en lugar de un numero)
            try:
                n1 = float(n1_txt)
                n2 = float(n2_txt)
            except ValueError:
            # Si ocurre un error de conversion, mostramos un mensaje de error y usamos 'continue' para saltar a la siguiente iteracion del bucle, evitando que el programa se caiga.
                print("[Error] Debes ingresar valores numericos validos.")
                mensaje = "Error en la calculadora: valores numéricos inválidos."
                # Registrar el error en el historial
                d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "cmd": cmd,
                        "rol": rol_actual,
                        "descripcion": mensaje}
                historial_chat.append(d_log)
                continue

            if operador == "+":
                resultado = n1 + n2
                print(f"Resultado: {resultado}")
                mensaje = f"Operación: {n1} + {n2} = {resultado}"
            elif operador == "-":
                resultado = n1 - n2
                print(f"Resultado: {resultado}")
                mensaje = f"Operación: {n1} - {n2} = {resultado}"
            elif operador == "*":
                resultado = n1 * n2
                print(f"Resultado: {resultado}")
                mensaje = f"Operación: {n1} * {n2} = {resultado}"
            elif operador == "/":
                # La division por cero es una operacion matematica indefinida que genera un error en Python. Para evitar que el programa se caiga, verificamos si el segundo numero es cero antes de realizar la division.
                if n2 == 0:
                    print("[Error] No se puede dividir entre cero.")
                    mensaje = "Error en división: intento de dividir entre cero."
                else:
                    resultado = n1 / n2
                    print(f"Resultado: {resultado}")
                    mensaje = f"Operación: {n1} / {n2} = {resultado}"
            else:
                print("[Error] Operador no valido.")
                mensaje = "Operador no válido."

        elif cmd == "historial":
            # Usando .split() podemos dividir el comando en sus partes para verificar si hay parámetros
            partes_cmd = cmd.split()
            if len(partes_cmd) > 1:
                parametro = partes_cmd[1].lower()
                if parametro == "all":
                    if len(historial_chat) == 0:
                        print("[PseudoAgente] El historial está vacío.")
                    else:
                        print("\n=== Historial Completo ===")
                        for i, registro in enumerate(historial_chat, 1):
                            print(f"\n[{i}] Timestamp: {registro['timestamp']}")
                            print(f"    Comando: {registro['cmd']}")
                            print(f"    Rol: {registro['rol']}")
                            print(f"    Descripción: {registro['descripcion']}")
                    mensaje = "Se mostró el historial completo."
                elif parametro == "clear":
                    historial_chat.clear()
                    print("[PseudoAgente] Historial eliminado.")
                    mensaje = "Historial eliminado."
                else:
                    print("[PseudoAgente] Parámetro desconocido. Use 'historial all' o 'historial clear'.")
                    mensaje = "Parámetro de historial desconocido."
            else:
                # Modo búsqueda: el usuario ingresa una palabra clave
                if len(historial_chat) == 0:
                    print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
                else:
                    palabra_clave = input("Ingresa la palabra clave a buscar: ").strip().lower()
                    coincidencias = []
                    # Iteramos sobre el historial buscando si la palabra clave está contenida en la descripción
                    # Usamos .lower() en ambas cadenas para que la búsqueda sea insensible a mayúsculas y minúsculas
                    for registro in historial_chat:
                        if palabra_clave in registro['descripcion'].lower():
                            coincidencias.append(registro)
                    
                    if len(coincidencias) == 0:
                        print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
                        mensaje = f"Búsqueda realizada por: {palabra_clave} (sin resultados)."
                    else:
                        print(f"\n=== Resultados de búsqueda para '{palabra_clave}' ===")
                        print(f"Se encontraron {len(coincidencias)} coincidencia(s):\n")
                        for i, registro in enumerate(coincidencias, 1):
                            print(f"[{i}] Autor: {registro['rol']}")
                            print(f"    Mensaje: {registro['descripcion']}")
                            print(f"    Timestamp: {registro['timestamp']}\n")
                        mensaje = f"Búsqueda realizada por: {palabra_clave} ({len(coincidencias)} resultado(s))."

        else:
            print("Comando desconocido, intenta de nuevo.")
            mensaje = "Comando desconocido."
        
        # Registrar cada acción en el historial del agente (excepto historial clear que ya lo maneja)
        if cmd != "historial" or (len(cmd.split()) > 1 and cmd.split()[1].lower() != "clear"):
            d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cmd": cmd,
                    "rol": rol_actual,
                    "descripcion": mensaje}
            historial_chat.append(d_log)
