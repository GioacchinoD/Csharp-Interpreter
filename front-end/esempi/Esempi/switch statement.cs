using System;

class Program
{
    static void Main()
    {
        // Print a message indicating the start of the switch statement
        Console.WriteLine("Beginning of switch statement");

        // Declare and initialize an integer variable
        int day = 7;

        // Switch statement to determine the day of the week
        switch (day)
        {
            case 6:
                // If day equals 6, print that today is Saturday
                Console.WriteLine("Today is Saturday.");
                break;
            case 7:
                // If day equals 7, print that today is Sunday
                Console.WriteLine("Today is Sunday.");
                break;
            default:
                // For any other value, print a message looking forward to the weekend
                Console.WriteLine("Looking forward to the Weekend.");
                break;
        }
    }
}
