import CalcModule.*;
import org.omg.CORBA.ORB;
import org.omg.CORBA.BAD_PARAM;
import org.omg.PortableServer.POA;
import org.omg.PortableServer.POAHelper;
import org.omg.CosNaming.NamingContextExt;
import org.omg.CosNaming.NamingContextExtHelper;
import org.omg.CosNaming.NameComponent;

public class CalculatorServer {

    static class CalculatorImpl extends CalculatorPOA {
        public double add(double a, double b) {
            return a + b;
        }

        public double subtract(double a, double b) {
            return a - b;
        }

        public double multiply(double a, double b) {
            return a * b;
        }

        public double divide(double a, double b) {
            if (b == 0) {
                throw new BAD_PARAM("Division by zero");
            }
            return a / b;
        }
    }

    public static void main(String[] args) {
        try {
            ORB orb = ORB.init(args, null);

            POA rootPOA = POAHelper.narrow(
                    orb.resolve_initial_references("RootPOA"));
            rootPOA.the_POAManager().activate();

            CalculatorImpl servant = new CalculatorImpl();
            org.omg.CORBA.Object ref = rootPOA.servant_to_reference(servant);
            Calculator calculator = CalculatorHelper.narrow(ref);

            org.omg.CORBA.Object nameService =
                    orb.resolve_initial_references("NameService");
            NamingContextExt namingContext =
                    NamingContextExtHelper.narrow(nameService);

            NameComponent[] path = namingContext.to_name("Calculator");
            namingContext.rebind(path, calculator);

            System.out.println("CORBA Calculator Server is ready.");
            orb.run();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
