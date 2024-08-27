using System;

class Program
{
    static void Main()
    {
        // Note: Attempting to assign a string value to an integer variable will result in a compilation error
        // The variable 'number' is of type 'int', but "Hello world!" is a string
        int number = "Hello world!";

        // This line will not be executed due to the compilation error above
        Console.WriteLine(number);
    }
}

