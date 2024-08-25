# Downloads of required dependencies
There is a conda virtual environment configuration file containing all the necessary dependencies. \
If necessary, you can install anaconda by following the instructions at this link: https://www.anaconda.com 

```bash
# Create the environment from the environment.yml file
conda env create -f environment.yml
```
## Launching the back-end

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