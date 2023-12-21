import secrets

CARACTERES_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
CARACTERES_MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMEROS = "0123456789"
CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;':\"<>,.?/~`"

def generar_contrasena(longitud, incluir_minusculas, incluir_mayusculas, incluir_numeros, incluir_especiales):
    caracteres_usados = ""
    if incluir_minusculas:
        caracteres_usados += CARACTERES_MINUSCULAS
    if incluir_mayusculas:
        caracteres_usados += CARACTERES_MAYUSCULAS
    if incluir_numeros:
        caracteres_usados += NUMEROS
    if incluir_especiales:
        caracteres_usados += CARACTERES_ESPECIALES

    contrasena = ''.join(secrets.choice(caracteres_usados) for _ in range(longitud))
    return contrasena

def main():
    while True:
        # Preguntamos al usuario si desea generar una contraseña o salir
        opcion = input("¿Desea generar una contraseña? (s/n): ")

        if opcion.lower() == "s":
            # Pedimos al usuario la longitud de la contraseña
            longitud = int(input("Ingrese la longitud de la contraseña: "))

            # Pedimos al usuario qué tipos de caracteres incluir
            incluir_minusculas = input("Incluir caracteres en minúsculas? (s/n): ").lower() == "s"
            incluir_mayusculas = input("Incluir caracteres en mayúsculas? (s/n): ").lower() == "s"
            incluir_numeros = input("Incluir números? (s/n): ").lower() == "s"
            incluir_especiales = input("Incluir caracteres especiales? (s/n): ").lower() == "s"

            # Generamos la contraseña
            contrasena = generar_contrasena(longitud, incluir_minusculas, incluir_mayusculas, incluir_numeros, incluir_especiales)

            # Mostramos la contraseña generada al usuario
            print("-------------------------------------------------------------------")
            print(f"La contraseña generada es: {contrasena}")
            print("-------------------------------------------------------------------")

        elif opcion.lower() == "n":
            break

        else:
            print("Opción inválida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
