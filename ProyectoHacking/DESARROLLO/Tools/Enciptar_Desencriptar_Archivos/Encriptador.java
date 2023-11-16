package Enciptar_Desencriptar_Archivos;

import java.io.*;
import java.security.SecureRandom;
import java.util.Scanner;
import javax.crypto.*;
import javax.crypto.spec.*;
import java.awt.*;
import java.security.spec.KeySpec;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Encriptador {

    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner(System.in);

        // Crear un objeto FileDialog
        FileDialog fileDialog = new FileDialog((Frame) null, "SELECCIONA EL ARCHIVO ENCRIPTAR:", FileDialog.LOAD);

        // Mostrar el diálogo de selección de archivos
        fileDialog.setVisible(true);

        // Obtener el archivo seleccionado
        String archivoEntrada = fileDialog.getFile();

        if (archivoEntrada != null) {
            // Ruta completa del archivo
            String rutaCompleta = fileDialog.getDirectory() + archivoEntrada;

            // Archivo de salida
            String archivoSalida = archivoEntrada + "_ENCRIPTADO.txt";

            // Obtener la contraseña del usuario
            System.out.print("INGRESA LA CONTRASEÑA PARA EL CIFRADO DEL ARCHIVO: ");
            String clave = scanner.nextLine();

            // Clave de cifrado y vector de inicialización (IV)
            byte[] salt = new byte[16]; // Valor aleatorio para el salt
            SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
            KeySpec spec = new PBEKeySpec(clave.toCharArray(), salt, 65536, 256); // Derivar una clave de 256 bits
            SecretKey tmp = factory.generateSecret(spec);
            SecretKey claveSecreta = new SecretKeySpec(tmp.getEncoded(), "AES");
            byte[] iv = new byte[16];
            SecureRandom random = new SecureRandom();
            random.nextBytes(iv);
            IvParameterSpec ivParametros = new IvParameterSpec(iv);

            // Cifrador AES en modo CBC
            Cipher cifrador = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cifrador.init(Cipher.ENCRYPT_MODE, claveSecreta, ivParametros);

            // Lectura del archivo de entrada y escritura del archivo cifrado
            FileInputStream archivoEntradaStream = new FileInputStream(rutaCompleta);
            FileOutputStream archivoSalidaStream = new FileOutputStream(archivoSalida);

            archivoSalidaStream.write(iv);

            byte[] buffer = new byte[1024];
            int numBytesLeidos;

            while ((numBytesLeidos = archivoEntradaStream.read(buffer)) != -1) {
                byte[] bufferCifrado = cifrador.update(buffer, 0, numBytesLeidos);
                archivoSalidaStream.write(bufferCifrado);
            }
            byte[] bufferCifradoFinal = cifrador.doFinal();
            archivoSalidaStream.write(bufferCifradoFinal);

            // Cierre de archivos
            archivoEntradaStream.close();
            archivoSalidaStream.close();

            System.out.println("ARCHIVO CIFRADO CORECTAMENTE");

        } else {
            System.out.println("NO SE SELECCIONÓ NINGUN ARCHIVO");

            System.out.print("¿Desea salir del programa? (s/n): ");
            String opcion = scanner.nextLine();

            if (opcion.equalsIgnoreCase("s")) {
                System.exit(0);
            }
        }
        scanner.close();
    }
}

