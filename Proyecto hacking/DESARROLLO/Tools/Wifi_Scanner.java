package Wifi_Scanner;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Wifi_Scanner {
    public static void main(String[] args) {
        System.out.print("¿Desea escanear las redes WiFi? (s/n): ");
        Scanner scanner = new Scanner(System.in);
        String respuesta = scanner.nextLine().trim();

        if (respuesta.equalsIgnoreCase("s")) {
            obtenerPerfilesWiFi();
        } else {
            System.out.println("Programa finalizado.");
        }
    }

    private static void obtenerPerfilesWiFi() {
        List<String> perfiles = new ArrayList<>();
        try {
            Process process = Runtime.getRuntime().exec("netsh wlan show profile");
            process.waitFor();
            InputStream is = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.contains(":")) {
                    String[] datos = line.split(":");
                    if (datos.length >= 2) {
                        perfiles.add(datos[1].trim());
                    }
                }
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        mostrarContrasenas(perfiles);
    }

    private static void mostrarContrasenas(List<String> perfiles) {
        for (int i = 0; i < perfiles.size(); i++) {
            String perfil = perfiles.get(i);
            System.out.println("RED " + (i + 1) + ": " + perfil);
            String[] cmd = {"netsh", "wlan", "show", "profile", perfil, "key=clear"};
            try {
                Process process = Runtime.getRuntime().exec(cmd);
                process.waitFor();
                InputStream is = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                String line;
                List<String> resultado = new ArrayList<>();
                while ((line = reader.readLine()) != null) {
                    resultado.add(line);
                }
                List<String> contrasenas = new ArrayList<>();
                for (String linea : resultado) {
                    if (linea.contains("Contenido de la clave")) {
                        String[] splitLine = linea.split(":");
                        contrasenas.add(splitLine[1].trim());
                    }
                }
                if (!contrasenas.isEmpty()) {
                    for (int j = 0; j < contrasenas.size(); j++) {
                        System.out.println("PASSWORD " + (j + 1) + ": " + contrasenas.get(j));
                    }
                } else {
                    System.out.println("PASSWORD 1: No encontrada");
                }
                System.out.println("----------------------------------------------------------------------------------");
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
