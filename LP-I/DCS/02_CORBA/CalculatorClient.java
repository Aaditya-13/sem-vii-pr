import CalcModule.*;
import org.omg.CORBA.ORB;
import org.omg.CosNaming.NamingContextExt;
import org.omg.CosNaming.NamingContextExtHelper;
import java.util.Scanner;

public class CalculatorClient {
    public static void main(String[] args) {
        try {
            ORB orb = ORB.init(args, null);

            org.omg.CORBA.Object nameService =
                    orb.resolve_initial_references("NameService");
            NamingContextExt namingContext =
                    NamingContextExtHelper.narrow(nameService);

            Calculator calculator = CalculatorHelper.narrow(
                    namingContext.resolve_str("Calculator"));

            Scanner input = new Scanner(System.in);
            System.out.print("Enter first number: ");
            double a = input.nextDouble();
            System.out.print("Enter second number: ");
            double b = input.nextDouble();

            System.out.println("1. Addition");
            System.out.println("2. Subtraction");
            System.out.println("3. Multiplication");
            System.out.println("4. Division");
            System.out.print("Enter choice: ");
            int choice = input.nextInt();

            double result;
            switch (choice) {
                case 1:
                    result = calculator.add(a, b);
                    break;
                case 2:
                    result = calculator.subtract(a, b);
                    break;
                case 3:
                    result = calculator.multiply(a, b);
                    break;
                case 4:
                    result = calculator.divide(a, b);
                    break;
                default:
                    System.out.println("Invalid choice.");
                    input.close();
                    return;
            }

            System.out.println("Result = " + result);
            input.close();
        } catch (Exception e) {
            System.err.println("Client error: " + e);
        }
    }
}
