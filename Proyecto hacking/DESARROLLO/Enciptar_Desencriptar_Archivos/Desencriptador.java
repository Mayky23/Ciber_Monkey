package Enciptar_Desencriptar_Archivos;

import java.awt.*;
import java.io.*;
import java.security.spec.KeySpec;
import javax.crypto.*;
import javax.crypto.spec.*;
import javax.crypto.SecretKeyFactory;
import javax.crypto.SecretKey;
import javax.crypto.spec.PBEKeySpec;
import java.util.Scanner;

public class Desencriptador {

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);

        while (true) {
            // Crear un objeto FileDialog
            FileDialog fileDialog = new FileDialog((Frame) null, "Seleccione el archivo a desencriptar", FileDialog.LOAD);

            // Mostrar el diálogo de selección de archivos
            fileDialog.setVisible(true);

            // Obtener el archivo seleccionado
            String archivoEntrada = fileDialog.getFile();

            if (archivoEntrada != null) {
                // Ruta completa del archivo
                String rutaCompleta = fileDialog.getDirectory() + archivoEntrada;

                // Archivo de salida
                String archivoSalida = archivoEntrada.replace("_ENCRIPTADO.txt", "_DESENCRIPTADO.txt");

                // Obtener la contraseña del usuario
                System.out.print("Ingrese la contraseña: ");
                String clave = sc.nextLine();

                // Generar la clave de cifrado utilizando PBKDF2
                byte[] salt = new byte[16]; // Valor aleatorio para el salt
                SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
                KeySpec spec = new PBEKeySpec(clave.toCharArray(), salt, 65536, 256); // Derivar una clave de 256 bits
                SecretKey tmp = factory.generateSecret(spec);
                SecretKey claveSecreta = new SecretKeySpec(tmp.getEncoded(), "AES");

                // Lectura del archivo cifrado y extracción del IV
                FileInputStream archivoEntradaStream = new FileInputStream(rutaCompleta);
                byte[] iv = new byte[16];
                archivoEntradaStream.read(iv);
                IvParameterSpec ivParametros = new IvParameterSpec(iv);

                // Descifrador AES en modo CBC
                Cipher descifrador = Cipher.getInstance("AES/CBC/PKCS5Padding");
                descifrador.init(Cipher.DECRYPT_MODE, claveSecreta, ivParametros);

                // Lectura del archivo cifrado y escritura del archivo descifrado
                FileOutputStream archivoSalidaStream = new FileOutputStream(archivoSalida);
                byte[] buffer = new byte[1024];
                int numBytesLeidos;
                while ((numBytesLeidos = archivoEntradaStream.read(buffer)) != -1) {
                    byte[] bufferDescifrado = descifrador.update(buffer, 0, numBytesLeidos);
                    archivoSalidaStream.write(bufferDescifrado);
                }
                byte[] bufferDescifradoFinal = descifrador.doFinal();
                archivoSalidaStream.write(bufferDescifradoFinal);

                // Cierre de archivos
                archivoEntradaStream.close();
                archivoSalidaStream.close();

                System.out.println("Archivo descifrado correctamente.");
            } else {
                System.out.println("No se seleccionó ningún archivo.");

                System.out.print("¿Desea salir del programa? (s/n): ");
                String opcion = sc.nextLine();
                if (opcion.equalsIgnoreCase("s")) {
                    System.exit(0);
                }
            }
        }
    }
}

