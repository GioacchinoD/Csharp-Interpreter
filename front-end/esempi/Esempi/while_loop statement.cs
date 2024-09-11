using System;

class Program
{
    static void Main()
    {
        int i = 0;  // Initialize the variable i to 0

        // Start a while loop that runs as long as i is less than 5
        while (i < 5)
        {
            // If i equals 3, increment i and skip the rest of the loop iteration
            if (i == 3)
            {
                i++;
                continue;  // Skip the remaining code in this iteration and move to the next iteration
            }

            // Print the current value of i
            Console.WriteLine("The current value of i is: " + i);

            i++;  // Increment i by 1
        }
    }
}
