#               Project CANVAR 

## A Tool for Clinical Annotation of Variants using ClinVar databases. 

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
