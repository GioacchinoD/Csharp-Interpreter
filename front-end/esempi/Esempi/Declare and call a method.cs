using System;

class Program
{
    static bool CheckEvenOdd(int number)
    {
        // Check if the number is even or odd
        Console.WriteLine("The number recived is: " + number);
        return number % 2 == 0;
    }

    static void MyMethod(bool result, int input) 
    {
        // Check the result and print whether the number is even or odd
        if (result)
        {
            Console.WriteLine("The number " + input + " is even.");
        }
        else
        {
            Console.WriteLine("The number " + input + " is odd.");
        }
    }

    static void Main()
    {
        Console.WriteLine("Enter an integer:");

        // Read the user input and convert it to an integer
        int input = Console.ReadLine();

        // Call the method to check if the number is even or odd
        bool result = CheckEvenOdd(input);
        
        MyMethod(result, input);
        

    }
}