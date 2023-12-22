import secrets

CARACTERES_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
CARACTERES_MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMEROS = "0123456789"
CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;':\"<>,.?/~`"

def generar_contrasena(longitud, opciones):
    caracteres_usados = ""

    if "min" in opciones:
        caracteres_usados += CARACTERES_MINUSCULAS
    if "may" in opciones:
        caracteres_usados += CARACTERES_MAYUSCULAS
    if "num" in opciones:
        caracteres_usados += NUMEROS
    if "esp" in opciones:
        caracteres_usados += CARACTERES_ESPECIALES

    contrasena = ''.join(secrets.choice(caracteres_usados) for _ in range(longitud))
    return contrasena

def password_generator_main():
    while True:
        opcion = input("¿Desea generar una contraseña? (s/n): ")

        if opcion.lower() == "s":
            longitud = int(input("Ingrese la longitud de la contraseña: "))
            opciones = input("Ingrese las opciones (min/may/num/esp): ").lower().split('/')
            
            contrasena = generar_contrasena(longitud, opciones)

            print("-------------------------------------------------------------------")
            print(f"La contraseña generada es: {contrasena}")
            print("-------------------------------------------------------------------")

        elif opcion.lower() == "n":
            break

        else:
            print("Opción inválida. Inténtelo de nuevo.")

if __name__ == "__main__":
    password_generator_main()
