package DESCUBRIR_HOST;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.UnknownHostException;

public class Descubrir_Host {

    public static void main(String[] args) {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String input = "";

        while (!input.equals("salir")) {
            try {
                // Solicita la dirección IP al usuario
                System.out.print("Ingrese una dirección IP (o escriba 'salir' para salir): ");
                input = in.readLine();

                if (input.equals("salir")) {
                    System.out.println("Saliendo del programa...");
                    break;
                }

                // Convierte la dirección IP a un objeto InetAddress
                InetAddress ip = InetAddress.getByName(input);

                // Realiza un ping a la dirección IP para verificar si está activa
                if (ip.isReachable(5000)) {
                    System.out.println("La dirección IP " + ip.getHostAddress() + " ESTA ACTIVA.");
                } else {
                    System.out.println("La dirección IP " + ip.getHostAddress() + " NO ESTA ACTIVA.");
                }
            } catch (UnknownHostException e) {
                System.out.println("Dirección IP inválida. ingrese una dirección IP válida.");
            } catch (Exception e) {
                System.out.println("Ocurrió un error. Por favor intente de nuevo.");
            }
        }
    }
}
