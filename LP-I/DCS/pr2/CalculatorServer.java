import CalcModule.*;
import org.omg.CORBA.ORB;
import org.omg.CORBA.BAD_PARAM;
import org.omg.PortableServer.*;
import org.omg.CosNaming.*;

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

            Calculator calculator = CalculatorHelper.narrow(
                    rootPOA.servant_to_reference(new CalculatorImpl()));
            NamingContextExt naming = NamingContextExtHelper.narrow(
                    orb.resolve_initial_references("NameService"));
            naming.rebind(naming.to_name("Calculator"), calculator);

            System.out.println("CORBA Calculator Server is ready.");
            orb.run();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
