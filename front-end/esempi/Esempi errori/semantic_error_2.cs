using System;

class Program
{
    static void Main()
    {
        // Declare and initialize an array of strings with 4 elements
        string[] cars = new string[4] {"Volvo", "BMW", "Ford", "Mazda"};

        // Print the length of the cars array
        Console.WriteLine("cars_array_length: " + cars.Length);

        // For loop to iterate through all elements of the cars array
        // Note: This loop will throw an exception because it tries to access an index out of bounds.
        for (int i = 0; i <= cars.Length; i++) // The condition should be i < cars.Length to avoid the error
        {
            // Print the value of the current element in the cars array
            Console.WriteLine("The element at position " + i + " in the cars array is: " + cars[i]);
        }
    }
}