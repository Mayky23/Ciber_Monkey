package Hack_Tool;

import java.util.Scanner;

import Auditar_BD_SQL.Auditar_BD;
import CIDR_Calculadora.Calculadora_CIDR;
import DDos_Atack.DDos_Atack;
import DESCUBRIR_HOST.Descubrir_Host;
import Enciptar_Desencriptar_Archivos.Desencriptador;
import Enciptar_Desencriptar_Archivos.Encriptador;
import Escacha_puertos.Escucha_puertos;
import Generador_Datos.Data_Generator;
import Generador_Datos.Data_Limit;
import Inyeccion_SQL.SQL_Injection;
import PORTS_SCANNER.PORTS_Scanner;
import Password_Cracking.Password_Cracking;
import Password_Secure.PasswordGenerator;
import Wifi_Scanner.Wifi_Scanner;

public class Net_Hunter {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        int option = 0;

        while (option != 15) {
            clearScreen(); // Borra el texto anterior antes de mostrar el menú

            
            System.out.println(" /$$   /$$             /$$           /$$   /$$                       /$$                            ");
            System.out.println("| $$$ | $$            | $$          | $$  | $$                      | $$                            ");
            System.out.println("| $$$$| $$  /$$$$$$  /$$$$$$        | $$  | $$ /$$   /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$     ");
            System.out.println("| $$ $$ $$ /$$__  $$|_  $$_/        | $$$$$$$$| $$  | $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$    ");
            System.out.println("| $$  $$$$| $$$$$$$$  | $$          | $$__  $$| $$  | $$| $$  \\ $$  | $$    | $$$$$$$$| $$  \\__/  ");
            System.out.println("| $$\\  $$$| $$_____/  | $$ /$$      | $$  | $$| $$  | $$| $$  | $$  | $$ /$$| $$_____/| $$         ");
            System.out.println("| $$ \\  $$|  $$$$$$$  |  $$$$/      | $$  | $$|  $$$$$$/| $$  | $$  |  $$$$/|  $$$$$$$| $$         ");
            System.out.println("|__/  \\__/ \\_______/   \\___/        |__/  |__/ \\______/ |__/  |__/   \\___/   \\_______/|__/    ");

            System.out.println("\n -By: MARH--------------------------------------------------------------------------------------");

            System.out.println("\n==================================");
            System.out.println("| 1. CALCULAR CIDR               |");               
            System.out.println("| 2. MOSTRAR REDES WIFI          |");
            System.out.println("| 3. DESCUBRIR IP ACTIVA         |");
            System.out.println("| 4. ESCANEAR PUERTOS            |");
            System.out.println("| 5. ESCUCHA DE PUERTOS          |");
            System.out.println("| 6. ATAQUE DDoS                 |");
            System.out.println("| 7. CREAR CONTRASEÑA            |");
            System.out.println("| 8. CRACKEAR CONTRASEÑA         |");
            System.out.println("| 9. ENCRIPTAR ARCHIVO           |");
            System.out.println("| 10. DESENCRIPTAR ARCHIVO       |");
            System.out.println("| 11. GENERAR DATOS              |");
            System.out.println("| 12. GENERAR DATOS LÍMITE       |");
            System.out.println("| 13. INYECCIÓN SQL              |");
            System.out.println("| 14. AUDITAR BD SQL             |");
            System.out.println("| 15. SALIR DEL PROGRAMA         |");
            System.out.println("==================================");
            System.out.print("\nSELECCIONA UNA OPCIÓN: ");

            option = sc.nextInt();
            sc.nextLine(); // Consumir el salto de línea residual

            switch (option) {
                case 1:
                    System.out.println("CALCULANDO CIDR...");
                    System.out.println("----------------------------------");
                    Calculadora_CIDR.main(args);
                    break;
                case 2:
                    System.out.println("MOSTRANDO REDES WIFI...");
                    System.out.println("----------------------------------");
                    Wifi_Scanner.main(args);
                    break;
                case 3:
                    System.out.println("DESCUBRIENDO IP ACTIVA...");
                    System.out.println("----------------------------------");
                    Descubrir_Host.main(args);
                    break;
                case 4:
                    System.out.println("ESCANEANDO PUERTOS...");
                    System.out.println("----------------------------------");
                    PORTS_Scanner.main(args);
                    break;
                case 5:
                    System.out.println("ESCUCHANDO PUERTOS...");
                    System.out.println("----------------------------------");
                    Escucha_puertos.main(args);
                    break;
                case 6:
                    System.out.println("REALIZANDO ATAQUE DDoS...");
                    System.out.println("----------------------------------");
                    DDos_Atack.main(args);
                    break;
                case 7:
                    System.out.println("CREANDO CONTRASEÑA...");
                    System.out.println("----------------------------------");
                    PasswordGenerator.main(args);
                    break;
                case 8:
                    System.out.println("CRACKEANDO CONTRASEÑA...");
                    System.out.println("----------------------------------");
                    Password_Cracking.main(args);
                    break;
                case 9:
                    System.out.println("ENCRIPTANDO ARCHIVO...");
                    System.out.println("----------------------------------");
                    Encriptador.main(args);
                    break;
                case 10:
                    System.out.println("DESENCRIPTANDO ARCHIVO...");
                    System.out.println("----------------------------------");
                    Desencriptador.main(args);
                    break;
                case 11:
                    System.out.println("GENERANDO DATOS...");
                    System.out.println("----------------------------------");
                    Data_Generator.main(args);
                    break;
                case 12:
                    System.out.println("GENERANDO DATOS LIMITE...");
                    System.out.println("----------------------------------");
                    Data_Limit.main(args);
                    break;
                case 13:
                    System.out.println("REALIZANDO SQL INJECTION...");
                    System.out.println("----------------------------------");
                    SQL_Injection.main(args);
                    break;
                case 14:
                    System.out.println("AUDITANDO BD SQL...");
                    System.out.println("----------------------------------");
                    Auditar_BD.main(args);
                    break;
                case 15:
                    System.out.println("SALIENDO DEL PROGRAMA...");
                    System.out.println("----------------------------------");
                    break;
                default:
                    System.out.println("OPCIÓN INVÁLIDA, INTÉNTALO DE NUEVO");
                    System.out.println("----------------------------------");
            }

            if (option != 15) {
                System.out.print("PRESIONA ENTER PARA CONTINUAR");
                sc.nextLine();
            }
        }
    }

    public static void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
}
