import java.util.Scanner;

public class IP_Scanner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Ingrese la dirección de red (en formato CIDR): ");
        String cidr = sc.nextLine();
        try {
            NetworkScanner.scan(cidr);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}