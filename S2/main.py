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
    print("\nAgente activo. Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, salir")
    sistema_activo = True

    while sistema_activo:
        cmd = input("PseudoAgente>: ").strip().lower()

        if cmd == "salir":
            print("Apagando agente. Hasta luego.")
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")

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

        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                print(f"Fecha actual: {fecha_actual}")
            else:
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

        elif cmd == "validar_pass":
            nueva_password = input("Ingresa una nueva propuesta de contrasena: ").strip()

            if len(nueva_password) < 8:
                print("[Rechazada] Debe tener al menos 8 caracteres.")
            elif nueva_password.lower() == usuario_actual.lower():
                print("[Rechazada] La contrasena no puede ser igual al nombre de usuario.")
            else:
                print("[OK] Contrasena valida.")

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
                continue

            if operador == "+":
                print(f"Resultado: {n1 + n2}")
            elif operador == "-":
                print(f"Resultado: {n1 - n2}")
            elif operador == "*":
                print(f"Resultado: {n1 * n2}")
            elif operador == "/":
                # La division por cero es una operacion matematica indefinida que genera un error en Python. Para evitar que el programa se caiga, verificamos si el segundo numero es cero antes de realizar la division.
                if n2 == 0:
                    print("[Error] No se puede dividir entre cero.")
                else:
                    print(f"Resultado: {n1 / n2}")
            else:
                print("[Error] Operador no valido.")

        else:
            print("Comando desconocido, intenta de nuevo.")
