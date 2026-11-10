import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.concurrent.atomic.AtomicInteger;

public class ProcessServer extends UnicastRemoteObject
        implements ProcessService {

    private final AtomicInteger requestCount = new AtomicInteger();

    public ProcessServer() throws RemoteException {
        super();
    }

    @Override
    public String processRequest(String clientName, String message)
            throws RemoteException {
        int id = requestCount.incrementAndGet();
        String thread = Thread.currentThread().getName();

        System.out.println("Request " + id + " from " + clientName
                + " handled by " + thread);

        try {
            Thread.sleep(2000); // Makes concurrent processing visible
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RemoteException("Request interrupted", e);
        }

        return "Request " + id + " processed: " + message;
    }

    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("ProcessService", new ProcessServer());
            System.out.println("RMI server is ready on port 1099.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
