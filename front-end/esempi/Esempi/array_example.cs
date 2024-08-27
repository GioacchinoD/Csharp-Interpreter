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
        for (int i = 0; i < cars.Length; i++)
        {
            // Print the value of the current element in the cars array
            Console.WriteLine("The element at position " + i + " in the cars array is: " + cars[i]);
        }

        Console.WriteLine();  // Print an empty line to separate sections of the output

        // Declare an array of integers
        int[] numbers;

        // Initialize the numbers array with 5 elements
        numbers = new int[5] {1, 2, 3, 4, 5};

        // For loop to iterate through all elements of the numbers array
        for (int j = 0; j < numbers.Length; j++)
        {
            // Print the value of the current element in the numbers array
            Console.WriteLine("The element at position " + j + " in the numbers array is: " + numbers[j]);
        }
    }
}
