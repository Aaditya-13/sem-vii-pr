import java.rmi.registry.*;

public class ProcessClient {
    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            ProcessService service =
                    (ProcessService) registry.lookup("ProcessService");

            for (int i = 1; i <= 3; i++) {
                final int request = i;
                new Thread(() -> {
                    try {
                        System.out.println(service.process("Request " + request));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }).start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
