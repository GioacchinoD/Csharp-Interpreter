using System;

class Program
{
    static void Main()
    {
        // Print the start message for the for loop
        Console.WriteLine("Starting for loop");

        int j; // Declare the variable j

        // For loop starting at 2 and ending at 10 (inclusive)
        for (j = 2; j <= 10; j++)
        {
            // If j equals 5, skip the rest of the loop iteration and continue with the next iteration
            if (j == 5)
            {
                continue;
            }

            // Print the current value of j
            Console.WriteLine("The current value of j is: " + j);

            // If j equals 6, exit the loop immediately
            if (j == 6)
            {
                break;
            }
        }
    }
}
