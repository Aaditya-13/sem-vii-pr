# Practical 1: Multithreaded Client/Server Communication Using RMI

## Aim

To implement client/server process communication using Java Remote Method
Invocation (RMI), and demonstrate concurrent requests from a client.

## Theory

Java RMI lets an object in one Java Virtual Machine call a method on an object in
another Java Virtual Machine. The caller uses a remote interface as if it were a
local Java interface; the RMI runtime sends the call to the server and returns
the result or a remote exception.

The remote interface extends `java.rmi.Remote`. Each remote method declares
`RemoteException`, which reports communication or remote-call errors. The
server implements this interface and extends `UnicastRemoteObject` to export its
object so that it can receive remote calls.

The RMI registry is a naming service. The server binds its remote object to the
name `ProcessService`; the client looks up that name and obtains a remote
reference. This program creates the registry on port `1099` inside the server,
so no separate `rmiregistry` process is required.

The client uses a fixed thread pool of three threads and submits three remote
requests. The server can process calls concurrently using threads managed by
the RMI runtime. A two-second delay in the remote method makes the overlapping
requests and server thread names easier to observe. The order of the replies may
vary because the calls run concurrently.

## Files and roles

| File | Role |
|---|---|
| `ProcessService.java` | Declares the remote method used by both client and server. |
| `ProcessServer.java` | Implements and exports the service, then registers it. |
| `ProcessClient.java` | Looks up the service and makes three concurrent calls. |

## Program

### `ProcessService.java`

```java
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ProcessService extends Remote {
    String processRequest(String clientName, String message)
            throws RemoteException;
}
```
| Line(s) | Explanation |
|---|---|
| 1 | Imports `Remote`, the marker interface used to identify a Java RMI remote interface. |
| 2 | Imports `RemoteException`, used to report errors during remote communication. |
| 4 | Declares the public interface named `ProcessService`. |
| 4 | `extends Remote` marks this as an interface whose methods may be called remotely. |
| 5–6 | Declares `processRequest`: it accepts the client name and message, returns a string, and may throw `RemoteException`. |
| 7 | Closes the interface. |

### `ProcessServer.java`

```java
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
```

| Line(s) | Explanation |
|---|---|
| 1 | Imports `RemoteException` for RMI and remote-method errors. |
| 2 | Imports `LocateRegistry`, used to create an RMI registry. |
| 3 | Imports the `Registry` interface. |
| 4 | Imports `UnicastRemoteObject`, which exports objects so they can receive RMI calls. |
| 5 | Imports `AtomicInteger`, a counter that is safe to increment from multiple threads. |
| 7–8 | Declares `ProcessServer`; it extends `UnicastRemoteObject` and implements the remote contract `ProcessService`. |
| 10 | Creates a shared request counter, initially zero. |
| 12–14 | Defines the constructor. `super()` exports this object through `UnicastRemoteObject`; `RemoteException` may occur during export. |
| 16 | `@Override` indicates that the next method implements the interface method. |
| 17–18 | Begins `processRequest`, accepting the client's name and message and declaring the required remote exception. |
| 19 | Atomically increments the request counter and stores the resulting request ID. |
| 20 | Gets the name of the current server thread. |
| 22–23 | Prints the request ID, client name, and server thread to demonstrate which thread handles the call. |
| 25–26 | Pauses this call for two seconds, making overlapping requests easier to observe. |
| 27 | Catches an interruption that may happen during the pause. |
| 28 | Restores the thread's interrupted status. |
| 29 | Reports the interruption to the remote caller as a `RemoteException`. |
| 30 | Closes the `catch` block. |
| 32 | Builds and returns a reply containing the request ID and client's message. |
| 33 | Closes `processRequest`. |
| 35 | Declares the server's `main` method, where server startup begins. |
| 36 | Starts a `try` block to handle errors during startup. |
| 37 | Creates the RMI registry on port `1099`. |
| 38 | Creates the server object and registers it under the name `ProcessService`. |
| 39 | Prints a message confirming that the server is ready. |
| 40 | Catches a startup or registration exception and prints its details. |
| 41–44 | Print the exception details, then close the exception handler, `main` method, and class. |


### `ProcessClient.java`

```java
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
```
| Line(s) | Explanation |
|---|---|
| 1 | Imports `LocateRegistry` so the client can connect to the registry. |
| 2 | Imports the `Registry` interface used for service lookup. |
| 3 | Imports `ExecutorService`, the interface for managing worker threads. |
| 4 | Imports `Executors`, which provides methods for creating thread pools. |
| 6 | Declares the client class. |
| 7 | Declares the client's `main` method. |
| 8 | Uses the first command-line argument as the client name, or defaults to `Client`. |
| 10 | Starts a `try` block for connecting to and calling the RMI service. |
| 11 | Gets a registry reference on the local computer at port `1099`. |
| 12–13 | Looks up the service by name and casts its remote reference to `ProcessService`. |
| 15 | Creates a fixed thread pool with three worker threads. |
| 16 | Begins a loop that will submit three requests numbered 1, 2, and 3. |
| 17 | Copies the loop number into a `final` variable so the lambda task can use it. |
| 18 | Submits a task to the pool; each submitted task can run on a worker thread. |
| 19 | Starts a `try` block inside the task for errors from this individual request. |
| 20–21 | Calls the remote method with the client name and a request-specific message, then stores the returned string. |
| 22–23 | Prints the client worker thread name and the reply received from the server. |
| 24–26 | Catches an error from this request and prints its message, then closes the request's `catch` block. |
| 27 | Closes the submitted task. |
| 28 | Stops the pool from accepting new tasks; the three tasks already submitted are allowed to finish. |
| 29–31 | Catches connection or lookup errors and prints their full details. |
| 32–33 | Close the `main` method and `ProcessClient` class. |

## How to compile and run

Open a terminal in the folder containing the three `.java` files.

Compile:

```powershell
javac ProcessService.java ProcessServer.java ProcessClient.java
```

Start the server in the first terminal:

```powershell
java ProcessServer
```

Start the client in a second terminal:

```powershell
java ProcessClient
```

Optionally, provide a client name:

```powershell
java ProcessClient Alice
```

The server prints each request ID and the RMI thread that handles it. The client
prints the returned messages. Request IDs and output order can differ between
runs.


## Execution flow to remember

1. Define the remote contract in `ProcessService`.
2. Implement and export the remote object in `ProcessServer`.
3. Create the registry and bind the service under a name.
4. Look up the service from `ProcessClient`.
5. Submit multiple calls to the client thread pool and print each reply.

## Viva questions and short answers

1. **What is Java RMI?**  
   Java RMI is a mechanism for invoking methods on Java objects running in
   another Java Virtual Machine.

2. **What is a remote interface?**  
   It is an interface that extends `Remote` and declares methods that can be
   called remotely.

3. **Why does `processRequest` throw `RemoteException`?**  
   A remote call can fail because of network, registry, or server communication
   problems, so RMI methods must account for `RemoteException`.

4. **What is the purpose of the RMI registry?**  
   It maps a service name to a remote object reference so clients can look up
   the service.

5. **What does `rebind` do?**  
   It binds a name to a remote object, replacing any previous binding with that
   name.

6. **Why does `ProcessServer` extend `UnicastRemoteObject`?**  
   It exports the object so the RMI runtime can receive remote method calls.

7. **How does this program demonstrate multithreading?**  
   The client submits three calls to a three-thread executor, and the RMI
   server handles incoming calls on its runtime-managed threads.

8. **Why is `AtomicInteger` used for the request count?**  
   Multiple server threads may update the count concurrently; `AtomicInteger`
   increments it safely.

9. **Why is there a two-second sleep in the server method?**  
   It makes the concurrent requests easier to observe. It is only for the
   demonstration and is not needed in a real service.

10. **Why might the request output order change on different runs?**  
    Concurrent threads can be scheduled in different orders, so the order of
    processing and replies is not guaranteed.
