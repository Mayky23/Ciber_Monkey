package Password_Secure;

import java.security.SecureRandom;
import java.util.Scanner;

public class PasswordGenerator {
    private static final String CARACTERES_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz";
    private static final String CARACTERES_MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private static final String NUMEROS = "0123456789";
    private static final String CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;':\"<>,.?/~`";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        boolean salir = false;

        while (!salir) {
            // Preguntamos al usuario si desea generar una contraseña o salir
            System.out.print("¿Desea generar una contraseña? (s/n): ");
            String opcion = scanner.nextLine();

            if (opcion.equalsIgnoreCase("s")) {
                // Pedimos al usuario la longitud de la contraseña
                System.out.print("Ingrese la longitud de la contraseña: ");
                int longitud = scanner.nextInt();

                // Pedimos al usuario que tipos de caracteres incluir
                System.out.print("Incluir caracteres en minúsculas? (s/n): ");
                boolean incluirMinusculas = scanner.next().equalsIgnoreCase("s");

                System.out.print("Incluir caracteres en mayúsculas? (s/n): ");
                boolean incluirMayusculas = scanner.next().equalsIgnoreCase("s");

                System.out.print("Incluir números? (s/n): ");
                boolean incluirNumeros = scanner.next().equalsIgnoreCase("s");

                System.out.print("Incluir caracteres especiales? (s/n): ");
                boolean incluirEspeciales = scanner.next().equalsIgnoreCase("s");

                // Generamos la contraseña
                String contrasena = generarContrasena(longitud, incluirMinusculas, incluirMayusculas, incluirNumeros, incluirEspeciales);

                // Mostramos la contraseña generada al usuario
                System.out.println("-------------------------------------------------------------------");
                System.out.println("La contraseña generada es: " + contrasena);
                System.out.println("-------------------------------------------------------------------");

                scanner.nextLine(); // Consumir la nueva línea dejada por nextInt()
            } else if (opcion.equalsIgnoreCase("n")) {
                salir = true;
            } else {
                System.out.println("Opción inválida. Inténtelo de nuevo.");
            }
        }
    }

    private static String generarContrasena(int longitud, boolean incluirMinusculas, boolean incluirMayusculas, boolean incluirNumeros, boolean incluirEspeciales) {
        SecureRandom aleatorio = new SecureRandom();
        StringBuilder contrasena = new StringBuilder();

        // Creamos una cadena con los tipos de caracteres que incluirá la contraseña
        String caracteresUsados = "";
        if (incluirMinusculas) {
            caracteresUsados += CARACTERES_MINUSCULAS;
        }
        if (incluirMayusculas) {
            caracteresUsados += CARACTERES_MAYUSCULAS;
        }
        if (incluirNumeros) {
            caracteresUsados += NUMEROS;
        }
        if (incluirEspeciales) {
            caracteresUsados += CARACTERES_ESPECIALES;
        }

        // Generamos la contraseña usando caracteres aleatorios de la cadena creada anteriormente
        for (int i = 0; i < longitud; i++) {
            int indice = aleatorio.nextInt(caracteresUsados.length());
            contrasena.append(caracteresUsados.charAt(indice));
        }

        return contrasena.toString();
    }
}
