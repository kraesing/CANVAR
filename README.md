#               Project CANVAR 

## A Tool for Clinical Annotation of Variants using ClinVar databases. 

Purpose: An efficient Python script designed for annotating variants detected through next-generation sequencing within a clinical setting. 
This script provides comprehensive data from the most up-to-date ClinVar database, simplifying the process of variant analysis and aiding in clinical decision-making.

### Installation of Anaconda for the use of ClinVar on Windows (win-64)

follow the tutorial on: https://docs.anaconda.com/free/anaconda/install/windows/

### Creating a windows environment for ClinVar

In Anaconda Prompt (Miniconda3) type:

```bash
conda create -n canvar python=3.9.12 m2-base=1.0.0
```

- The m2-base package enables the use of UNIX commands. 

### Activate the environment

```bash
conda activate canvar
```  