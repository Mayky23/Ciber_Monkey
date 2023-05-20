package Generador_Datos;

import java.util.Random;
import java.util.Scanner;

public class Data_Generator {
    private static final String[] ALPHABET = {
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    };
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String response;
        
        do {
            System.out.println("¿Cuántas personas deseas generar? (Escribe 'salir' para terminar)");
            response = scanner.nextLine();
            
            if (response.equalsIgnoreCase("salir")) {
                break;
            }
            
            try {
                int numPeople = Integer.parseInt(response);
                
                for (int i = 0; i < numPeople; i++) {
                    System.out.println("Datos de la persona #" + (i + 1));
                    System.out.println("-----------------------------------------------------");
                    System.out.println("DNI: " + generateDNI());
                    System.out.println("Nombre: " + generateName());
                    System.out.println("Email: " + generateEmail());
                    System.out.println("Cuenta bancaria: " + generateBankAccount());
                    System.out.println("Fecha de nacimiento: " + generateDateOfBirth());
                    System.out.println("Contraseña: " + generatePassword());
                    System.out.println("-----------------------------------------------------");
                }
            } catch (NumberFormatException e) {
                System.out.println("Error: Ingresa un número válido o escribe 'salir' para terminar.");
            }
        } while (true);
        
        scanner.close();
    }
    
    public static String generateDNI() {
        StringBuilder dni = new StringBuilder();
        int length = 8; // Longitud del DNI (solo números)
        Random random = new Random();
        
        // Generar los dígitos del número de DNI
        for (int i = 0; i < length; i++) {
            dni.append(random.nextInt(10));
        }
        
        // Agregar una letra mayúscula al final
        dni.append(ALPHABET[random.nextInt(ALPHABET.length)]);
        
        return dni.toString();
    }
    
    public static String generateName() {
        Random random = new Random();
        String firstName = generateRandomName(FIRST_NAMES);
        String lastName = generateRandomName(LAST_NAMES);
        
        return firstName + " " + lastName;
    }
    
    public static String generateEmail() {
        Random random = new Random();
        String firstName = generateRandomName(FIRST_NAMES).toLowerCase();
        String lastName = generateRandomName(LAST_NAMES).toLowerCase();
        String domain = generateRandomName(EMAIL_DOMAINS);
        
        // Generar variaciones del correo electrónico con puntos o guiones bajos
        int variation = random.nextInt(3);
        String email;
        
        switch (variation) {
            case 0:
                email = firstName + "." + lastName + "@" + domain;
                break;
            case 1:
                email = firstName + "_" + lastName + "@" + domain;
                break;
            default:
                email = firstName + lastName + "@" + domain;
                break;
        }
        
        return email;
    }
    
    public static String generateBankAccount() {
        Random random = new Random();
        String bank = generateRandomName(BANKS);
        StringBuilder accountNumber = new StringBuilder();
        
        for (int i = 0; i < 10; i++) {
            accountNumber.append(random.nextInt(10));
            }
            return bank + " - " + accountNumber.toString();
    }

    public static String generateDateOfBirth() {
        Random random = new Random();
        int year = random.nextInt(50) + 1970; // Año aleatorio entre 1970 y 2019
        int month = random.nextInt(12) + 1; // Mes aleatorio entre 1 y 12
        int day = random.nextInt(28) + 1; // Día aleatorio entre 1 y 28
        return String.format("%04d-%02d-%02d", year, month, day);
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

    private static String generateRandomName(String[] names) {
        Random random = new Random();
        return names[random.nextInt(names.length)];
    }

    private static final String[] FIRST_NAMES = {
        "Juan", "María", "José", "Laura", "Carlos", "Sofía", "Luis", "Ana", "Pedro", "Marta",
        "Alejandro", "Isabella", "Diego", "Valentina", "Gabriel"
    };
    
    private static final String[] LAST_NAMES = {
        "Gómez", "Rodríguez", "Fernández", "López", "Pérez", "González", "Martínez", "Sánchez", "Romero", "Torres",
        "Ortega", "Hernández", "Silva", "Ramírez", "Chavez"
    };
    
    private static final String[] EMAIL_DOMAINS = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
        "icloud.com", "mail.com", "live.com", "protonmail.com", "example.com"
    };
    
    private static final String[] BANKS = {
        "Banco A", "Banco B", "Banco C", "Banco D", "Banco E",
        "Banco F", "Banco G", "Banco H", "Banco I", "Banco J"
    };
    
}

