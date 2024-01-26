import argparse
import hashlib
import time
import itertools
import os

def verificar_contraseña(hash, contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest().upper() == hash.upper()

def fuerza_bruta(hash, longitud_maxima):
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for longitud in range(1, longitud_maxima + 1):
        for contraseña in itertools.product(caracteres, repeat=longitud):
            if verificar_contraseña(hash, ''.join(contraseña)):
                return ''.join(contraseña)

def ataque_diccionario(hash, wordlist):
    if not os.path.exists(wordlist):
        return "El archivo de diccionario no existe."
    with open(wordlist) as f:
        for contraseña in f:
            if verificar_contraseña(hash, contraseña.strip()):
                return contraseña.strip()

def ataque_diccionario_con_reemplazos(hash, ordlist, reemplazos):
    if not os.path.exists(wordlist):
        return "El archivo de diccionario no existe."
    with open(wordlist) as f:
        for contraseña in f:
            contraseña = contraseña.strip()
            transformaciones = [contraseña] + [contraseña.replace(*reemplazo) for reemplazo in reemplazos]
            for t in transformaciones:
                if verificar_contraseña(hash, t):
                    return t

def ataque_dirigido(hash, palabras):
    for posibilidad in itertools.permutations(palabras):
        if verificar_contraseña(hash, ''.join(posibilidad)):
            return ''.join(posibilidad)

def Contrasena_Cracking_main():
    tiempo_inicio = time.time()

    parser = argparse.ArgumentParser(description="Descifrador de contraseñas simple.")
    parser.add_argument("command", nargs="?", help="Comando a ejecutar (escriba 'help' para obtener ayuda)")
    parser.add_argument("--hash", help="Hash de la contraseña a descifrar")
    parser.add_argument("--length_max", type=int, help="Longitud máxima de las contraseñas a probar")
    parser.add_argument("--dictionary", help="Archivo de diccionario de contraseñas")
    parser.add_argument("--replacements", help="Reemplazos a aplicar en el diccionario (formato: a/b,c/d,...)")
    parser.add_argument("--words", help="Lista de palabras para el ataque dirigido")

    args = parser.parse_args()

    if args.command == "help":
        print(
			"************************************************************************************************************\n"
			"*   HELP                                                                                                  *\n"
			"************************************************************************************************************\n"
			"* brute_force: Intenta todas las contraseñas alfanuméricas posibles                                        *\n"
			"* con longitud menor o igual a --length_max.                                                               *\n"
			"*----------------------------------------------------------------------------------------------------------*\n"
			"* dict: Intenta todas las contraseñas contenidas en un archivo de                                          *\n"
			"* diccionario proporcionado por --dictionary.                                                              *\n"
			"*----------------------------------------------------------------------------------------------------------*\n"
			"* dict_repl: Intenta todas las contraseñas contenidas en un archivo de diccionario proporcionado por       *\n"
			"* --dictionary y, para cada contraseña, prueba las contraseñas obtenidas mediante reemplazos dados         *\n"
			"* por --replacements. Un reemplazo reemplaza todas las ocurrencias del carácter antiguo por el nuevo en    *\n"
			"* la contraseña.                                                                                           *\n"
			"*----------------------------------------------------------------------------------------------------------*\n"
			"* targeted: Intenta todas las posibles permutaciones de todos los                                          *\n"
			"* posibles subconjuntos de una lista de palabras dada por --words.                                         *\n"
			"************************************************************************************************************\n"
)

    elif args.command == "brute_force":
        if not args.hash or not args.length_max:
            print("Faltan argumentos para el comando brute_force.")
        else:
            contraseña = fuerza_bruta(args.hash, args.length_max)
            if contraseña:
                print("CONTRASEÑA DESCUBIERTA:", contraseña)
                print("Tiempo transcurrido:", time.time() - tiempo_inicio, "segundos.")
            else:
                print("No se pudo descifrar la contraseña con este método y estos parámetros.")
    elif args.command == "dict":
        if not args.hash or not args.dictionary:
            print("Faltan argumentos para el comando dict.")
        else:
            contraseña = ataque_diccionario(args.hash, args.dictionary)
            if contraseña:
                print("CONTRASEÑA DESCUBIERTA:", contraseña)
            else:
                print("No se pudo descifrar la contraseña con este método y estos parámetros.")
    elif args.command == "dict_repl":
        if not args.hash or not args.dictionary or not args.replacements:
            print("Faltan argumentos para el comando dict_repl.")
        else:
            reemplazos = [r.split("/") for r in args.replacements.split(",")]
            contraseña = ataque_diccionario_con_reemplazos(args.hash, args.dictionary, reemplazos)
            if contraseña:
                print("CONTRASEÑA DESCUBIERTA:", contraseña)
            else:
                print("No se pudo descifrar la contraseña con este método y estos parámetros.")
    elif args.command == "targeted":
        if not args.hash or not args.words:
            print("Faltan argumentos para el comando targeted.")
        else:
            contraseña = ataque_dirigido(args.hash, args.words.split(","))
            if contraseña:
                print("CONTRASEÑA DESCUBIERTA:", contraseña)
            else:
                print("No se pudo descifrar la contraseña con este método y estos parámetros.")
    else:
        print("Comando no reconocido.")

if __name__ == "__main__":
    Contrasena_Cracking_main()
