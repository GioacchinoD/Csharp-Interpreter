using System;

class Program
{
    static void Main()
    {
        // Declare and initialize an array of strings with 4 elements
        // Note: The array contains an integer (55) which is incorrect for a string array
        string[] cars = new string[4] {"Volvo", "BMW", "Ford", 55};

        // Print the length of the cars array
        Console.WriteLine("cars_array_length: " + cars.Length);

        // For loop to iterate through all elements of the cars array
        for (int i = 0; i < cars.Length; i++)
        {
            // Print the value of the current element in the cars array
            Console.WriteLine("The element at position " + i + " in the cars array is: " + cars[i]);
        }
    }
}

