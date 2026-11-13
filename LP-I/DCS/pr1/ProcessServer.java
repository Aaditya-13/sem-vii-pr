import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.*;

interface ProcessService extends Remote {
    String process(String message) throws RemoteException;
}

public class ProcessServer extends UnicastRemoteObject
        implements ProcessService {

    public ProcessServer() throws RemoteException {
        super();
    }

    public String process(String message) throws RemoteException {
        System.out.println("Server handled " + message + " on "
                + Thread.currentThread().getName());

        try {
            Thread.sleep(1000); // Makes concurrent requests easier to see
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        return "Processed: " + message;
    }

    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("ProcessService", new ProcessServer());
            System.out.println("RMI server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
