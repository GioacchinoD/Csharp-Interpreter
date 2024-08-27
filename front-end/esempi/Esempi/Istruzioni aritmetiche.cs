using System;

class Program
{
    static void Main()
    {
        // Print a message indicating simple variable declarations
        Console.WriteLine("Simple variable declarations");

        // Declare and initialize two integer variables
        int x = 10;
        int y = 7;

        // Print the values of the variables x and y
        Console.WriteLine("x = " + x);
        Console.WriteLine("y = " + y);

        Console.WriteLine();  // Print an empty line for better readability

        // Print a message indicating the start of arithmetic operations
        Console.WriteLine("Beginning of arithmetic operations");

        // Perform various arithmetic operations
        int subtraction = x - y;
        int addition = x + y;
        int multiplication = x * y;
        int division = x / y;
        int modulo = x % y;

        // Increment the value of x by 1
        x++;

        // Print the results of the arithmetic operations
        Console.WriteLine("Addition = " + addition);
        Console.WriteLine("Subtraction = " + subtraction);
        Console.WriteLine("Multiplication = " + multiplication);
        Console.WriteLine("Division = " + division);
        Console.WriteLine("Modulo = " + modulo);
        Console.WriteLine("Increment of variable x = " + x);
    }
}
