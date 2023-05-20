package CIDR_Calculadora;

import java.net.InetAddress;
import java.util.Scanner;

public class Calculadora_CIDR {

    public static void main(String[] args) throws Exception {
        // Lee la dirección IP desde la entrada del usuario


        while (true) {
            // Lee la dirección IP desde la entrada del usuario
            System.out.print("\n Ingrese una dirección IP (o 'no' para terminar): ");
            Scanner sc = new Scanner(System.in);
            String ipString = sc.nextLine();
            
            if (ipString.equals("no")) {
                // Si el usuario escribe "no", sale del bucle
                break;
            }
            
            // Convierte la dirección IP a un objeto InetAddress
            InetAddress ip = InetAddress.getByName(ipString);

            // Calcula la máscara de subred en formato CIDR
            int prefixLength = getPrefixLength(ip);
            System.out.println(ipString + "/" + prefixLength);
        }
    }

    public static int getPrefixLength(InetAddress ip) {
        // Obtiene la dirección IP en forma de arreglo de bytes
        byte[] bytes = ip.getAddress();

        // Inicializa la máscara de subred y el índice de bits
        int mask = 0;
        int bitIndex = 7;

        // Itera a través de los bytes de la dirección IP
        for (byte b : bytes) {
            // Itera a través de los bits de cada byte
            for (int i = 0; i < 8; i++) {
                // Si el bit es 1, establece el bit correspondiente en la máscara de subred
                if ((b & (1 << bitIndex)) != 0) {
                    mask++;
                }

                // Disminuye el índice de bits
                bitIndex--;
            }
        }

        // Retorna la máscara de subred en formato CIDR
        return mask;
    }

}


