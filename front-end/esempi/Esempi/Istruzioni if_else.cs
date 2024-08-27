using System;

class Program
{
    static void Main()
    {
        // Print a message about the simple declaration of variables
        Console.WriteLine("Simple variable declaration");

        // Declare and initialize two integer variables
        int x = 10;
        int y = 7;

        // Print the values of x and y
        Console.WriteLine("x = " + x);
        Console.WriteLine("y = " + y);

        Console.WriteLine();  // Print an empty line to separate sections of the output

        // Print a message about starting the if-else statements
        Console.WriteLine("Starting if-else statements");

        // If-else statement to check the value of x
        if (x == 5)
        {
            Console.WriteLine("x is equal to 5");
        }
        else if (x == 6)
        {
            Console.WriteLine("x is equal to 6");
        }
        else if (x == 7)
        {
            Console.WriteLine("x is equal to 7");
        }
        else if (!(x == 10))
        {
            Console.WriteLine("x is not equal to 10");
        }
        else
        {
            Console.WriteLine("x = " + x);
        }

        // If-else statement to check the value of y
        if ((y != 2) && (y != 5))
        {
            Console.WriteLine("y is not equal to either 2 or 5");
        }
        else
        {
            Console.WriteLine("y = " + y);
        }
    }
}
