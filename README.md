# Csharp-Interpreter web based

A web-based interpreter for C#. 
The front-end part uses React and Next.js to provide a dynamic and responsive user experience. 
The back-end part is built in Python and uses Lark, a modern parsing library for Python.

Lark documentation: https://lark-parser.readthedocs.io/en/stable/ \
Lark repository: https://github.com/lark-parser/lark \
C# grammar reference: https://ecma-international.org/wp-content/uploads/ECMA-334_7th_edition_december_2023.pdf

## Specification of the C# language restriction considered

* Data types:

      - Integer (int)
      - Boolean (bool)
      - String (string)
      - Array type [extra]

* Logical Operators:

      - Logical AND (&&)
      - Logical OR (||)
      - Logical NOT (!)

* Arithmetic Operators: 
  
      - Addition (+)
      - Subtraction (-)
      - Multiplication (*)
      - Division (/)
      - Modulus (%)

* Comparison Operators:

      - Equal to (==)
      - Not equal to (!=)
      - Grater than (>)
      - Less than (<)
      - Greater than or equal to (>=)
      - Less than or equal to (<=)

* Branching Construction:

      - if statement
      - if-else statement
      - switch statement [extra]

* Loop Construction:

      - while loop statement
      - for loop statement [extra]

* Assignment Operations:

      - identifier += expression
      - identifier -= expression
      - identifier *= expression
      - identifier /= expression
      - identifier++
      - identifier--

* Input Instruction:

      - Console.ReadLine()

* Output Instruction:

      - Console.WriteLine()

* Comments (ignored by grammar)

      - single line comment (//)
      - multi line comment (/* */)

* Array [extra]

      - array declaration 
      - array assignment
      - array access
      - array length

* String Methods [extra]

      - string length (txt.Length)
      - ToUpper() (txt.ToUpper())
      - ToLower() (txt.ToLower())

* Method Declaration [extra]

      - static 'type' Identifier (list_of_parameters) {body}
          + static: Means that the method belongs to the Program class and not a object of the Program class
          + type: It is possible to use the void keyword when the method does not have to return a value. 
                  If the method must return a value, you can use one of the primitive data types (string, int, bool)
                  instead of the void keyword and use the return statement inside the method.
          + list_of_parameters: They are optional. Parameters act as variables within the method.
                  They are specified after the method name, in parentheses. You can add as many parameters as you wish,
                  simply separationg them with a comma.
          + body: Is the body of the method.

* Method Call [extra]:

      - Identifier (list_of_parameters)

* Other statements:

      - break statement [extra]
      - continue statement [extra]
      - return statement [extra]

## Managed error

* Syntax Error:
      
        - Missing open round bracket '('
        - Missing closed round bracket ')'
        - Missing open square parenthesis '['
        - Missing closed square parenthesis ']'
        - Missing open claw bracket '{'
        - Missing closed claw bracket '}'
        - Missing the semicolon ';'
        - Missing equal '='

* Semantic Error:

      - Unsupported Operation Type
      - Index Out of Range

* Other types of errors:

      - Type error
      - Errors for variables
      - Errors for arrays
      - Errors for methods reserved for strings

# Instructions for the execution of the project

## Downloads of required dependencies
1. Clone the repository or download the project:
```bash 
git clone https://github.com/GioacchinoD/Csharp-Interpreter.git
```

2. Go into the front-end folder and install the necessary dependencies using the following command. 

    If necessary, you can install Node.js by following the instructions at this link: https://nodejs.org/en/download/package-manager (It is preferable to use the 20.16.0 version)
```bash         
cd front-end

# By default, all modules listed as dependencies in package.json will be installed.
npm install
```
3. In the back-end folder is a conda virtual environment configuration file containing all the necessary dependencies. 

    If necessary, you can install anaconda by following the instructions at this link: https://www.anaconda.com 
```bash 
cd back-end

# Create the environment from the environment.yml file
conda env create -f environment.yml
```
## Run the project

### Launching the back-end

1. Open a terminal
2. Go to back-end directory in the project folder
3. Run the following command to activate the conda environment:
```bash 
# Verify that the project environment has been installed correctly
conda env list  

# Activate the project environment
conda activate csharp_interpreter_venv  
```

4. Run the script:
```bash     
python main.py
```
### Launching the front-end

1. Open a terminal
2. Go to front-end directory in the project folder
3. Run the following command to launch the front-end part:
```bash 
#For Windows system
npm run start_project_windows 

#For Linux system
npm run project_start_linux

# For Mac system
npm run project_start_mac 
```
