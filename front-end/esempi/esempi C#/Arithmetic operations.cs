using System;

class Program
{
    static void Main()
    {
        // Declare variables
        int a = 10;
        int b = 5;

        // Addition
        int sum = a + b;
        Console.WriteLine("Addition: " + a + " + " + b + " = " + sum);

        // Subtraction
        int difference = a - b;
        Console.WriteLine("Subtraction: " + a + " - " + b + " = " + difference);

        // Multiplication
        int product = a * b;
        Console.WriteLine("Multiplication: " + a + " * " + b + " = " + product);

        // Division
        int quotient = a / b;
        Console.WriteLine("Division: " + a + " / " + b + " = " + quotient);

        // Modulus
        int remainder = a % b;
        Console.WriteLine("Modulus: " + a + " % " + b + " = " + remainder);
    }
}