import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ProcessClient {
    public static void main(String[] args) {
        String clientName = args.length > 0 ? args[0] : "Client";

        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            ProcessService service =
                    (ProcessService) registry.lookup("ProcessService");

            ExecutorService pool = Executors.newFixedThreadPool(3);
            for (int i = 1; i <= 3; i++) {
                final int request = i;
                pool.submit(() -> {
                    try {
                        String reply = service.processRequest(clientName,
                                "Hello from request " + request);
                        System.out.println(Thread.currentThread().getName()
                                + " received: " + reply);
                    } catch (Exception e) {
                        System.err.println("Request failed: " + e.getMessage());
                    }
                });
            }
            pool.shutdown();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
