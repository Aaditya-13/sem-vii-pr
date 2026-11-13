# Practical 1: Multithreaded Client/Server Communication Using RMI

## Aim

To use Java Remote Method Invocation (RMI) so a client can call a method on a
server, and to send several requests from separate client threads.

## Theory

Java RMI lets one Java program call a method on an object running in another
Java process. The server provides a remote method. The RMI registry stores the
server reference under a name. The client looks up that name and calls the
remote method.

This program registers the server as ProcessService. The client looks it up and
starts three threads. Each thread sends a request. The server prints the name
of the thread handling the request and returns a reply.

## Files and roles

| File | Role |
|---|---|
| ProcessServer.java | Contains the remote interface, server implementation, and startup code. |
| ProcessClient.java | Finds the service and sends three requests using separate threads. |

ProcessService is declared inside ProcessServer.java to keep the program to two
Java source files.

## ProcessServer.java

~~~java
import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.*;
~~~

**Explanation:** These lines import Java RMI classes so we can use them by
their short names. The first import includes Remote and RemoteException. The
second includes Registry and LocateRegistry. The third includes
UnicastRemoteObject. The * means it imports all classes in this package.

~~~java
interface ProcessService extends Remote {
    String process(String message) throws RemoteException;
}
~~~

**Explanation:** This declares the remote interface. An interface lists the
methods a class promises to provide. ProcessService is the interface name.
extends Remote marks it as an RMI interface.

The process method receives a String called message and returns a String. The
semicolon means this line only declares the method; its instructions are in the
server class. throws RemoteException says that an RMI communication problem
may be reported to the caller. The braces mark the beginning and end of the
interface.

~~~java
public class ProcessServer extends UnicastRemoteObject
        implements ProcessService {
~~~

**Explanation:** This declares the server class. public means other Java
classes can use it. The filename must match the public class name:
ProcessServer.java.

extends UnicastRemoteObject gives the server RMI behavior so it can receive
remote calls. implements ProcessService means this class will provide the
process method listed in the interface. The opening brace begins the class body.

~~~java
    public ProcessServer() throws RemoteException {
        super();
    }
~~~

**Explanation:** This is the constructor. Java runs a constructor when it
creates a new object. Its name matches the class name, ProcessServer.
super() calls the constructor of the parent class UnicastRemoteObject, which
exports this object for RMI. The constructor can throw RemoteException if that
export fails.

~~~java
    public String process(String message) throws RemoteException {
~~~

**Explanation:** This begins the implementation of the remote process method.
Its name and parameter match the interface declaration. It receives the
client's message and returns a String. RemoteException is declared because
the call is made through RMI.

~~~java
        System.out.println("Server handled " + message + " on "
                + Thread.currentThread().getName());
~~~

**Explanation:** Prints a message in the server terminal. System.out.println
displays text. The + joins text and values. message is the text sent by the
client. Thread.currentThread().getName() gets the name of the server thread
currently handling this request. The statement is split across two lines for
readability; it is one print command.

~~~java
        try {
            Thread.sleep(1000); // Makes concurrent requests easier to see
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
~~~

**Explanation:** Thread.sleep(1000) pauses this server thread for 1000
milliseconds, or one second. This makes overlapping requests easier to notice;
the pause is only for demonstration.

Java requires sleep to be inside try/catch because it can be interrupted.
catch handles that interruption, and e stores information about it.
Thread.currentThread().interrupt() restores the thread's interrupted status.

~~~java
        return "Processed: " + message;
    }
~~~

**Explanation:** return sends a result back to the client. The + joins
"Processed: " with the message. If the client sent "Request 1", the reply is
"Processed: Request 1". The final brace closes the process method.

~~~java
    public static void main(String[] args) {
~~~

**Explanation:** This is the server program's starting method. Java looks for
main when you run the class. static means Java can run it without first
creating a ProcessServer object. String[] args can hold command-line
arguments; this program does not use them.

~~~java
        try {
            Registry registry = LocateRegistry.createRegistry(1099);
~~~

**Explanation:** try begins error handling for startup. LocateRegistry is a
Java RMI helper. createRegistry(1099) starts the registry on port 1099.
Registry registry stores a reference to that registry. Since this code creates
the registry, you do not need to run a separate rmiregistry command.

~~~java
            registry.rebind("ProcessService", new ProcessServer());
~~~

**Explanation:** new ProcessServer() creates the server object. rebind places
it in the registry under the name "ProcessService". The client must look up
this exact name to find the service.

~~~java
            System.out.println("RMI server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
~~~

**Explanation:** Prints a message confirming startup. catch handles an
exception if startup fails. e.printStackTrace() prints error details to the
terminal. Exception is a general error type.

~~~java
    }
}
~~~

**Explanation:** The first brace closes the main method. The second closes the
ProcessServer class.

## ProcessClient.java

~~~java
import java.rmi.registry.*;
~~~

**Explanation:** Imports the RMI registry classes the client needs to find the
server.

~~~java
public class ProcessClient {
    public static void main(String[] args) {
~~~

**Explanation:** Declares the client class and its main starting method. Since
the class is public, its filename must be ProcessClient.java. String[] args
can receive command-line values, but this program does not use them.

~~~java
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
~~~

**Explanation:** try begins error handling for connecting to the registry.
getRegistry("localhost", 1099) gets a reference to a registry on this same
computer, at port 1099. It does not start the registry; the server already
started it. The variable registry holds the reference.

~~~java
            ProcessService service =
                    (ProcessService) registry.lookup("ProcessService");
~~~

**Explanation:** lookup asks the registry for the service named
"ProcessService", the same name used by the server. The returned remote
reference is cast to ProcessService so Java knows which method the client can
call. The variable service holds that reference.

~~~java
            for (int i = 1; i <= 3; i++) {
~~~

**Explanation:** This for loop repeats three times. It starts i at 1, continues
while i is at most 3, and increases i by one after each round. That gives
request numbers 1, 2, and 3.

~~~java
                final int request = i;
~~~

**Explanation:** Copies the current value of i into request. final means
request cannot be reassigned. The thread task needs this fixed value because
the loop continues changing i while the threads run.

~~~java
                new Thread(() -> {
~~~

**Explanation:** new Thread creates a thread. The code inside its braces is
the task the thread should run. The symbol -> introduces a lambda, Java's
short form for providing that task.

~~~java
                    try {
                        System.out.println(service.process("Request " + request));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
~~~

**Explanation:** The thread calls the remote process method and sends a
message such as "Request 1". It prints the reply returned by the server.
The catch handles a failure from this individual request, and
e.printStackTrace() prints details about it.

~~~java
                }).start();
~~~

**Explanation:** The brace closes the thread's task. start() starts the thread
so it runs separately. Without start(), the task would not run as a new thread.

~~~java
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
~~~

**Explanation:** The first brace closes the for loop after all three threads
have been started. The catch handles errors from connecting to the registry or
looking up the service.

~~~java
    }
}
~~~

**Explanation:** The first brace closes main. The second closes the
ProcessClient class.

## How to compile and run

Open two terminals in the pr1 folder. Compile both source files together:

~~~powershell
javac ProcessServer.java ProcessClient.java
~~~

In the first terminal, start the server and leave it running:

~~~powershell
java ProcessServer
~~~

In the second terminal, start the client:

~~~powershell
java ProcessClient
~~~

The server creates the registry itself, so do not start a separate rmiregistry.
The server terminal prints which thread handled each request. The client
terminal prints the replies. Their order can vary because threads may run in
different orders.

## Execution flow to remember

1. ProcessService declares the remote method.
2. ProcessServer implements the method and registers itself.
3. ProcessClient looks up the service by its registered name.
4. The client starts three threads; each calls the remote method.
5. The server returns a reply, which the client prints.

## Viva questions and short answers

1. **What is Java RMI?**  
   It lets one Java program call a method on an object in another Java process.

2. **What is a remote interface?**  
   It lists methods that can be called through RMI.

3. **Why does ProcessService extend Remote?**  
   It marks the interface as an RMI remote interface.

4. **Why does process declare RemoteException?**  
   The remote call can fail while the client and server communicate.

5. **What is the RMI registry?**  
   A naming service that lets a server register an object and a client find it.

6. **What does rebind do?**  
   It registers an object under a name, replacing an older entry with that name.

7. **Why does ProcessServer extend UnicastRemoteObject?**  
   To export the server object so it can receive remote calls.

8. **How does this program demonstrate multithreading?**  
   The client starts three threads, each of which sends a remote request.

9. **Why is Thread.sleep(1000) used?**  
   It pauses requests briefly so overlapping calls are easier to observe.

10. **Why can the output order change?**  
    Threads may be scheduled in different orders each time the program runs.

