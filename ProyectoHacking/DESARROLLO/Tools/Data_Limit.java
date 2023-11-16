package Generador_Datos;

import java.util.Random;
import java.util.Scanner;

public class Data_Limit {

    private static final String[] ALPHABET = {
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    };

    public static String generateDNI() {
        StringBuilder dni = new StringBuilder();
        int length = 9; // Longitud del DNI
        Random random = new Random();
        
        for (int i = 0; i < length-1; i++) {
            if (random.nextBoolean()) {
                dni.append(ALPHABET[random.nextInt(ALPHABET.length)]); // Agregar letra aleatoria
            } else {
                dni.append(random.nextInt(10)); // Agregar número aleatorio
            }
        }
        dni.append(ALPHABET[random.nextInt(ALPHABET.length)]); // Agregar una letra mayúscula al final
        return dni.toString();
    }

    public static String generateName() {
        StringBuilder name = new StringBuilder();
        int length = 10; // Longitud del nombre
        Random random = new Random();
        
        for (int i = 0; i < length-1; i++) {
            if (random.nextBoolean()) {
                name.append(ALPHABET[random.nextInt(ALPHABET.length)]); // Agregar letra aleatoria
            } else {
                name.append(random.nextInt(10)); // Agregar número aleatorio
            }
        }
        name.append(random.nextInt(10)); // Agregar un número al final
        return name.toString();
    }

    public static String generateEmail() {
        StringBuilder email = new StringBuilder();
        int length = 8; // Longitud del nombre de usuario del correo electrónico
        Random random = new Random();
        
        for (int i = 0; i < length; i++) {
            if (random.nextBoolean()) {
                email.append(ALPHABET[random.nextInt(ALPHABET.length)]); // Agregar letra aleatoria
            } else {
                email.append(random.nextInt(10)); // Agregar número aleatorio
            }
        }
        email.append("@example.com"); // Agregar dominio
        return email.toString();
    }

    public static String generateBankAccount() {
        StringBuilder account = new StringBuilder();
        int length = 10; // Longitud de la cuenta bancaria
        Random random = new Random();
        
        for (int i = 0; i < length; i++) {
            account.append(ALPHABET[random.nextInt(ALPHABET.length)]); // Agregar letra aleatoria
        }
        return account.toString();
    }

    public static String generateDateOfBirth() {
        StringBuilder dob = new StringBuilder();
        int year = (int)(Math.random() * (2023 - 1900 + 1)) + 1900; // Año aleatorio entre 1900 y 2023
        int month = (int)(Math.random() * 13); // Mes aleatorio entre 0 y 12
        int day = (int)(Math.random() * 32); // Día aleatorio entre 0 y 31
        
        dob.append(year);
        dob.append("-");
        if (month < 10) {
            dob.append("0");
        }
        dob.append(month);
        dob.append("-");
        
        if (day < 10) {
            dob.append("0");
        }
        dob.append(day);
    
        return dob.toString();
    }
    
    public static String generatePassword() {
        StringBuilder password = new StringBuilder();
        int length = 8; // Longitud de la contraseña
        Random random = new Random();
        String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
    
        for (int i = 0; i < length; i++) {
            password.append(characters.charAt(random.nextInt(characters.length())));
        }
    
        return password.toString();
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String response = "";
        
        do {
            System.out.println("¿Cuántas personas deseas generar? (Escribe 'salir' para terminar)");
            response = scanner.nextLine();
            
            if (response.equalsIgnoreCase("salir")) {
                break;
            }
            
            try {
                int numPeople = Integer.parseInt(response);
                
                for (int i = 0; i < numPeople; i++) {
                    System.out.println("Datos de la persona #" + (i+1));
                    System.out.println("-----------------------------------------------------");
                    System.out.println("DNI: " + generateDNI());
                    System.out.println("Name: " + generateName());
                    System.out.println("Email: " + generateEmail());
                    System.out.println("Bank Account: " + generateBankAccount());
                    System.out.println("Date of Birth: " + generateDateOfBirth());
                    System.out.println("Password: " + generatePassword());
                    System.out.println("-----------------------------------------------------");
                }
            } catch (NumberFormatException e) {
                System.out.println("Error: Ingresa un número válido o escribe 'salir' para terminar.");
            }
        } while (true);
        
        scanner.close();
    }
}
    
