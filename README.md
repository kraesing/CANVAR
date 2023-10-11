#               Project CANVAR 

## A Tool for Clinical Annotation of Variants using ClinVar databases. 
- doi:

Purpose: An efficient Python script designed for annotating variants detected through next-generation sequencing within a clinical setting. 
This script provides comprehensive data from the most up-to-date ClinVar database, simplifying the process of variant analysis and aiding in clinical decision-making.

### Installation of Anaconda for the use of ClinVar on Windows (win-64)

follow the tutorial on: https://docs.anaconda.com/free/anaconda/install/windows/

___________________________________________________
### Creating a windows environment for ClinVar

In Anaconda Prompt (Miniconda3) type:

```bash
conda create -n canvar python=3.9.12 m2-base=1.0.0
```

- The m2-base package enables the usage of UNIX commands. 

___________________________________________________
### Activate the environment

```bash
conda activate canvar
```

___________________________________________________
### Create directory for the CANVAR.py file and place it (optional)
- if the CANVAR.py file is placed elsewhere - the absolut path must be provided in the step "Running CANVAR.py".

```bash
mkdir ~/CANVAR_dir
``` 
 
___________________________________________________
### Change directory to CANVAR_dir

```bash
cd ~/CANVAR_dir
```

___________________________________________________
### Running CANVAR.py

The general use is simplified by the following:

```bash
~/CANVAR_dir/python CANVAR.py "function" -option  
```

Help can be accessed via -h or --help for all function.
```bash
~/CANVAR_dir/python CANVAR.py --help
```
```bash
~/CANVAR_dir/python CANVAR.py "function" --help
```  

___________________________________________________
### CANVAR.py packages

The "packages" function serves to install and import the essential packages required for the proper functioning of CANVAR.
NOTE: Internet connection is required for the installation of packages. 

```bash
~/CANVAR_dir/python CANVAR.py packages --import_packages Y
```

___________________________________________________
### CANVAR.py prearrange
The "prearrange" function establishes an environment that encompasses the parent directory and subdirectories for CANVAR. 

Directories created:
- ~/ClinVar_dir
- ~/ClinVar_dir/archive 
- ~/ClinVar_dir/ClinVar_database_files 
- ~/ClinVar_dir/input_files
- ~/ClinVar_dir/output_files_annotated 

```bash
~/CANVAR_dir/python CANVAR.py prearrange --wrkdir .
```

and subsequently change directory to ~/ClinVar_dir

```bash
cd ClinVar_dir
```

___________________________________________________
### CANVAR.py download_db







