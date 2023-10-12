#               Project CANVAR 

## A Tool for Clinical Annotation of Variants using ClinVar databases. 
- doi:

Purpose: An efficient Python script designed for annotating variants detected through next-generation sequencing within a clinical setting. 
This script provides comprehensive data from the most up-to-date ClinVar database, simplifying the process of variant analysis and aiding in clinical decision-making.

___________________________________________________
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
```Options: -h, --help```

The general use is simplified by the following:

```bash
~/CANVAR_dir/python CANVAR.py "function" --option  
```

Help can be accessed via -h or --help for all functions.
```bash
~/CANVAR_dir/python CANVAR.py --help
```
```bash
~/CANVAR_dir/python CANVAR.py "function" --help
```  

___________________________________________________
### CANVAR.py packages 
```Options: -i, --import_packages```

The "packages" function serves to install and import the essential packages required for the proper functioning of CANVAR.
NOTE: Internet connection is required for the installation of packages. 

```bash
~/CANVAR_dir/python CANVAR.py packages --import_packages Y
```

___________________________________________________
### CANVAR.py prearrange 
```Options: -w, --wrkdir```

The "prearrange" function establishes an environment that encompasses the parent directory and subdirectories for CANVAR. 

Directories created:
- ```~/canvar/```
- ```~/canvar/archive``` 
- ```~/canvar/clinvar_database_files``` 
- ```~/canvar/input_files```
- ```~/canvar/output_files_annotated```

```bash
~/CANVAR_dir/python CANVAR.py prearrange --wrkdir .
```

and subsequently change directory to ```~/canvar/```

```bash
cd canvar
```

___________________________________________________
### CANVAR.py download_db 
```Options: -l, --latest_file / -a, --archive_file```

The "download_db" function establishes a connection to ClinVar's File Transfer Protocol (FTP).
This is allowing you to download the most recent version of the database or an older version. 

FTP's: 
- GRCh37: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/
- GRCh38: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/

For the latest up-to-date ClinVar database file
```bash
~/canvar/python ../CANVAR.py download_db --latest_file latest 
```

For older versions of ClinVar database files (example: 2021)
```bash
~/canvar/python ../CANVAR.py download_db --archive_file 2021  
```

___________________________________________________
### CANVAR.py check_construct 
```Options: -d, --database_file```

The "check_construct" function utilizes the ClinVar's downloaded database file to create the required file for annotating variants. 
After this process is completed, the annotation file comprises the following details: 
- Location
- Nucleotide change 
- Gene symbol
- Clinical significance
- Reference SNP cluster ID (RS id)
- Mutation type
- ClinVar review status 
- ClinVar disease name

Creating the annotation file from .gz format (example: ClinVar database file from 20230617).
```bash
~/canvar/python ../CANVAR.py check_construct --database_file clinvar_20230617.vcf.gz
```

Creating the annotation file from .vcf (unpacked) format (example: ClinVar database file from 20230617).
```bash
~/canvar/python ../CANVAR.py check_construct --database_file clinvar_20230617.vcf
```

___________________________________________________
### CANVAR.py annotate
```Options: -f, --annotation_file```

The "annotate" function relies on the annotation file generated by the "check_construct" function. The annotation file to be used for annotating variants from user input files must be provided in the argument. 
The process of annotating user input files is associated with the ```~/canvar/input_files``` directory. 


It's important to note that the user input files must include variables denoting locus position, reference allele, and observed allele, with the designated variable names being: 
- Locus 
- Ref 
- Observed Allele

NOTE: To perform annotation, files intended for annotation must be placed in the ```~/canvar/input_files``` directory.

___________________________________________________

Following the annotation process, the input file will have additional columns appended, including: 
- Identifier
- Gene_symbol
- Clinical_significance
- RS_id
- Mutation_type
- ClinVar_review_status
- ClinVar_disease_name 

In cases where a variant is not found in the ClinVar database, it is marked with "Manually inspection needed" in the "Clinical_significance" column.

Once annotation is complete, the original files are relocated to the ```~/canvar/archive``` directory, and the annotated files with a ".ann" extension are transferred to the ```~/canvar/output_files_annotated``` directory.

___________________________________________________
### License
[MIT](https://choosealicense.com/licenses/mit/)







