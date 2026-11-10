import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ProcessService extends Remote {
    String processRequest(String clientName, String message)
            throws RemoteException;
}
