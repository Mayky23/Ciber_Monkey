package Escacha_puertos;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Escucha_puertos {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            System.out.print("Ingrese el puerto: ");
            int port = scanner.nextInt();

            ServerSocket serverSocket = new ServerSocket(port);
            System.out.println("Esperando conexiones entrantes en el puerto " + port + "...");

            Socket socket = serverSocket.accept();
            System.out.println("Conexión establecida desde: " + socket.getInetAddress() + ":" + socket.getPort());

            InputStream is = socket.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);

            OutputStream os = socket.getOutputStream();

            String command;
            while ((command = br.readLine()) != null) {
                if (command.toLowerCase().equals("exit")) {
                    break;
                }

                Process process = Runtime.getRuntime().exec(command);
                process.waitFor();

                InputStream processInputStream = process.getInputStream();
                BufferedReader processReader = new BufferedReader(new InputStreamReader(processInputStream));

                StringBuilder output = new StringBuilder();
                String line;
                while ((line = processReader.readLine()) != null) {
                    output.append(line).append("\n");
                }

                String commandOutput = output.toString();
                os.write(commandOutput.getBytes());
            }

            socket.close();
            serverSocket.close();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
