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
        int module = x % y;

        // Print the results of the arithmetic operations
        Console.WriteLine("Addition: " + x + " + " + y + " = " + addition);
        Console.WriteLine("Subtraction: " + x + " - " + y + " = " + subtraction);
        Console.WriteLine("Multiplication: " + x + " * " + y + " = " + multiplication);
        Console.WriteLine("Division: "+ x + " / " + y + " = " + division);
        Console.WriteLine("Module: " + x + " % " + y + " = " + module);

        // Increment the value of x by 1
        x++;
        
        Console.WriteLine("Increment of variable x = " + x);
    }
}
