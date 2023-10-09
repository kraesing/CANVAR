# =============================================================================
#                               Project CANVAR
# =============================================================================
# author: kraesing
# mail: lau.kraesing.vestergaard@regionh.dk 
# GitHub: https://github.com/kraesing

# overall impression is rather positive
# I enjoy the fact that code is divided into chunks / functions
# error handling is an issue from my perspective, but no much to do about if in python
# periodic logging with print statements is a plus
# consider setting up an option for verbosity
# if you intend to publish this in an academic journal I believe this would be of interest
# however, if you intend to release for production, meaning for the community to really use it
# I suggest to invest more time on testing & indentifying potential shortcommings
# there is nothing more annoying that software that does not work properly 
# definetely substantial improvement from the previous version I saw
# I would love to know your impressions & insights regarding this version
# Importing libraries!
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import sys
import argparse
import subprocess
import time
import pkg_resources
 
#%% Define paths for directories
WORKING_DIRECTORY = "ClinVar_dir"
ARCHIVE_DIRECTORY = "archive"
INPUT_FILES_DIRECTORY = "input_files"
OUTPUT_ANNOTATED_DIRECTORY = "output_files_annotated"
CLINVAR_DATABASE_DIRECTORY = "ClinVar_database_files"

#%% Define constants for package requirements
REQUIRED_PACKAGES = {"regex", "numpy", "pandas", "alive-progress", "tabulate", "requests", "wget"}
    

#%% Function to install required packages
def import_packages(args):
    
    missing_packages = REQUIRED_PACKAGES - {pkg.key for pkg in pkg_resources.working_set}

    # not super familiar with pyhon & pip package manager
    # but it feels like this could use an error catcher
    # also, package versions?
    if args.import_packages == "Y":
        for package in missing_packages:
            print(f"installing... {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Importing required packages.
        import os
        import time 
        import glob
        import gzip
        import shutil
        import io
        import numpy as np
        import pandas as pd
        import re
        from alive_progress import alive_bar
        from tabulate import tabulate    
        
        print("Needed packages have been imported")
    else:
        print("Input not available")
        
                   
#%% Function to create and manage directories
# Helper function to create or validate a directory
def create_or_validate_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        time.sleep(1)
        print(f"Subdirectory: {directory} ...created")
    else:
        time.sleep(1)
        print(f"Subdirectory: {directory} ...up-to-date")

# Function to create directories        
def prearrange(args):

    # Create or validate directories
    create_or_validate_directory(WORKING_DIRECTORY)
    create_or_validate_directory(os.path.join(WORKING_DIRECTORY, ARCHIVE_DIRECTORY))
    create_or_validate_directory(os.path.join(WORKING_DIRECTORY, INPUT_FILES_DIRECTORY))
    create_or_validate_directory(os.path.join(WORKING_DIRECTORY, OUTPUT_ANNOTATED_DIRECTORY))
    create_or_validate_directory(os.path.join(WORKING_DIRECTORY, CLINVAR_DATABASE_DIRECTORY))

    print(20 * "__")

#%% Function to download database files
# Helper function to visualize ClinVar database files. 
def tab_print(clinvar_df, option):
    from tabulate import tabulate
    print(tabulate(clinvar_df, headers='keys', tablefmt='github', showindex=option))

# Helper function to create tabled data
def clinvar_table_data(df):
    # better variable naming... probably
    import pandas as pd
    df_ = pd.DataFrame(df, columns=["file_name"])
    df_ = df_.loc[~df_["file_name"].str.contains("papu")]
    df_ = df_[~df_["file_name"].str.startswith('"clinvar.vcf.gz')]
    
    
    df_["Name"] = df_["file_name"].str.split(">").str[0].str.strip('"')
    df_["Date"] = df_["file_name"].str.split(">").str[2].str.split("   ").str[-2]
    df_["Size"] = df_["file_name"].str.split(">").str[2].str.split("   ").str[-1]
    
    df_.drop(columns=["file_name"], inplace=True)
    df_ = df_.reset_index(drop=True)
    
    return df_

#%% Function to check internet access.
def check_internet_connection():
    import requests
    # I would consider inputing the address as a variable
    # I do understand that you would most likely not work with other website
    # but still it would be more convenient for maintenace
    try: 
        resp = requests.get("https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Function to download files. 
def download_db(args):
    	
    # this boolean seems backwards to me
    # why not:
    # if !check_internet_connectionnection():
    # and get rid of the else
    if check_internet_connection():
        print("")
    else:
        print("Internet connection is required for packages and download_db to run")

    import pandas as pd 
    import re
    import wget
    import os
    
    os.chdir(os.path.join(os.getcwd(), CLINVAR_DATABASE_DIRECTORY))
        
    l_file = args.latest_file
    
    # I do not know whether python supports enums or something alike for type safety here
    # otherwise, consider prechecking for odd values
    if l_file == "latest":
        which_assembly = input("Specify Genome Reference Consortium Human assembly [37/38]: ")
        # again the ealier point of the hard-coded address
        # also, would this work with either version?
        link = f"https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh{which_assembly}/"
        
        print("Searching for latest database file at link...")
        
        import requests
        r = requests.get(link)
        r.close()

        content = r.text
        clinvar_files = re.findall(r"(?<=href=).*?(?=\n<a)", content)

        str_database = []
        for clin_f in clinvar_files[0:]:
            if clin_f.startswith('"clinvar') and '.vcf.gz"' in clin_f:
                str_database.append(clin_f)
        
        clinvar_files_df = clinvar_table_data(str_database)
        
        
        if not clinvar_files_df.empty:
            print("Latest files available at:")
            tab_print(clinvar_df=clinvar_files_df, option=False)

            download = input("Download the latest file? [Y/N]: ")

            # consider using boolean directly?
            if download.startswith("Y"):
                chosen_file = clinvar_files_df.iloc[0]["Name"]
                download_url = link + chosen_file
                print(f"Downloading {chosen_file}...")
                wget.download(download_url)
                print(f"\n{chosen_file} has been downloaded and placed in {CLINVAR_DATABASE_DIRECTORY}")
            else:
                print("No file downloaded.")
        else:
            print("No suitable database files found.")
    else: 
        which_assembly = input("Which Genome Reference Consortium Human Build? [37/38]: ")
        link1 = f"https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh{which_assembly}/archive_2.0/"
        a_file = args.archive_file
        a_file = str(a_file)
    
        print(f"Searching ClinVar for database files from {a_file}...\n")
    
        archive_url = link1 + a_file + "/"
     
        import requests

        r = requests.get(archive_url)
        r.close()

        content = r.text
        arc_files = re.findall(r"(?<=href=).*?(?=\n<a)", content)

        arc_database = []
        for arc_f in arc_files[0:]:
            if arc_f.startswith('"clinvar') and '.vcf.gz"' in arc_f:
                arc_database.append(arc_f)
        
        arc_files_df = clinvar_table_data(arc_database)
        
        if not arc_files_df.empty:
            print(f"Archive files available for year {a_file}:\n")
            tab_print(clinvar_df=arc_files_df, option=True)
    
            choose_file = input("Select file to download (by index): ")
    
            try:
                choose_file = int(choose_file)
                if choose_file >= 0 and choose_file < len(arc_files_df):
                    chosen_file = arc_files_df.iloc[choose_file]["Name"]
                    download_url = archive_url + chosen_file
                    print(f"Downloading {chosen_file}...")
                    wget.download(download_url)
                    print(f"\n{chosen_file} has been downloaded and placed in {CLINVAR_DATABASE_DIRECTORY}")
                else:
                    print("Invalid index. No file downloaded.")
            except ValueError:
                print("Invalid input. No file downloaded.")
        else:
            print(f"No suitable archive files found for year {a_file}.")

#%% Function to create file for annotation of variants
# Helper function to filter ClinVar variants
def Clinvar_filtering(data_vcf, name):
    # necessary import here, where they not all handled by function?
    import re
    import pandas as pd
    # consider replacing strings with variables
    # mainly for maintenace purposes
    # Clinical significance
    print("Task[1/8] - Creating column: Clinical_significance")
    data_vcf["Clinical_significance"] = data_vcf["INFO"].apply(lambda x: re.findall(r"(?<=CLNSIG).*?(?=;)", x)).astype("str")
    data_vcf["Clinical_significance"] = [re.sub(r'[^a-zA-Z/.]+', '_', s) for s in data_vcf["Clinical_significance"]]
    data_vcf["Clinical_significance"] = data_vcf["Clinical_significance"].apply(lambda x: x.rstrip("_")).apply(lambda x: x.lstrip("_")).apply(lambda x: x.replace("_", " "))

    # Gene symbol 
    print("Task[2/8] - Creating column: Gene_symbol ")
    data_vcf["Gene_symbol"] = data_vcf["INFO"].apply(lambda x: re.findall(r"(?<=GENEINFO).*?(?=;)", x)).astype("str")
    data_vcf["Gene_symbol"] = data_vcf["Gene_symbol"].apply(lambda x: x.split(":")[0]).apply(lambda x: x.replace("['=", ""))

    # a ";" is added to the end of the "INFO" column to have a end mark. This is needed as re.findall finds "something" inbetween two patterns. a "space" can not be used. 
    data_vcf["INFO"] = data_vcf["INFO"].apply(lambda x: x+";")

    # RS_ids
    print("Task[3/8] - Creating column: RS_id")
    data_vcf["RS_id"] = data_vcf["INFO"].apply(lambda x: re.findall(r"(?<=RS).*?(?=;)", x)).astype("str").apply(lambda x: re.sub('[^0-9]',"", x)).astype("str")

    data_vcf["RS_id"] = ["RS"+x if len(x) > 1 else x for x in data_vcf["RS_id"]]

    ## Mutation type of the variant e.g. missense, frameshift etc. 
    print("Task[4/8] - Creating column: Mutation_type")
    data_vcf["Mutation_type"] = data_vcf["INFO"].apply(lambda x: re.findall(r"(?<=MC).*?(?=;)", x)).astype("str")
    data_vcf["Mutation_type"] = data_vcf["Mutation_type"].apply(lambda x: x.split("|")[-1]).apply(lambda x: x[0:-2])
        
    ## ClinVar review status
    print("Task[5/8] - Creating column: ClinVar_review_status")
    data_vcf["ClinVar_review_status"] = data_vcf["INFO"].apply(lambda x: re.findall(r"(?<=CLNREVSTAT).*?(?=;)", x)).astype("str")
    data_vcf["ClinVar_review_status"] = data_vcf["ClinVar_review_status"].apply(lambda x: x.replace("['=", "")).apply(lambda x: x.replace("']", ""))
    
    ## Disease associations
    print("Task[6/8] - Creating column: ClinVar_disease_name")
    data_vcf["ClinVar_disease_name"] = data_vcf["INFO"].apply(lambda x: re.findall(r"(?<=CLNDN).*?(?=;)", x)).astype("str")
    data_vcf["ClinVar_disease_name"] = data_vcf["ClinVar_disease_name"].apply(lambda x: x.replace("['=", "")).apply(lambda x: x.replace("']", ""))        

    ## Identifier is a created ID for the variant. It contains build from 4 columns; CHR:POS:REF:ALT. The intention with this column is to use it as a column to merge variants on from once own dataset. 
    print("Task[7/8] - Creating column: Identifier")
    data_vcf["POS"] = data_vcf["POS"].astype("str")
    data_vcf["Identifier"] = data_vcf["CHR"] +":"+ data_vcf["POS"] +":"+ data_vcf["REF"] +":"+ data_vcf["ALT"]
        
    # Saving file    
    print("Task[8/8] - Saving file into ./ClinVar_database_files")
    ClinVar_final = data_vcf.copy()
        
    order_columns = ["Identifier", "Gene_symbol", "Clinical_significance", "RS_id", "Mutation_type", "ClinVar_review_status", "ClinVar_disease_name"]
        

    ClinVar_final = ClinVar_final[order_columns]
    
    # Adding identifier for validation of file    
    V_data = {"Identifier": ["0:000000:Valid:File"]}
    Valid_file = pd.DataFrame(V_data)
    ClinVar_final = pd.concat([ClinVar_final, Valid_file], ignore_index=True)
    
    ClinVar_final.to_csv(name, index=False, sep="\t")
        
    print("\nAnnotation file created!")

# Construction of the annotation file.
def check_construct(args):
    
    import gzip
    import shutil
    import time
    import pandas as pd
    import io
    import re
    import os
    
    os.chdir(os.path.join(os.getcwd(), CLINVAR_DATABASE_DIRECTORY))

    db_file = args.database_file

    def read_vcf(file):
        with open(file, 'r') as f:
            lines = [l for l in f if not l.startswith('##')]
            return pd.read_csv(
                io.StringIO(''.join(lines)),
                dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
                       'QUAL': str, 'FILTER': str, 'INFO': str},
                sep='\t'
            ).rename(columns={'#CHROM': 'CHR'})

    if db_file.endswith(".gz"):
        print("Decompressing the database file...")
        db_file_out = db_file[:-3]
        with gzip.open(db_file, "rb") as f_in:
            with open(db_file_out, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f"{db_file_out}.gz has been decompressed and is available in {CLINVAR_DATABASE_DIRECTORY}")
        time.sleep(2)

        print(f"Creating annotation file from: {db_file_out}...")
        data_vcf_file = read_vcf(db_file_out)
        tsv_file_name = db_file_out[:-4] + ".tsv"
        test = Clinvar_filtering(data_vcf=data_vcf_file, name=tsv_file_name)
        

    elif db_file.endswith(".vcf"):
        print(f"Creating annotation file from: {db_file}...")
        data_vcf_file = read_vcf(db_file)
        tsv_file_name = db_file[:-4] + ".tsv"
        test = Clinvar_filtering(data_vcf=data_vcf_file, name=tsv_file_name)

#%% Function to annotate input files
# Helper function to skip commented lines in input files.
def check_and_skip(file_to_check):
    lines_to_check = []
    with open(file_to_check, "r") as ftc:
        try: 
            for line in ftc: 
                if line.startswith("##"):
                    lines_to_check.append(line)
            return len(lines_to_check)
        except:
            return 0

# Helper function to create identifier column
def column_identifier(an_file_):
    
    an_file_["Identifier"] = an_file_["Locus"] + ":" + an_file_["Ref"] + ":" + an_file_["Observed Allele"]
    an_file_["Identifier"] = an_file_["Identifier"].astype("str")
    an_file_["Identifier"] = an_file_["Identifier"].str.replace("chr", "")
    
    return an_file_

# Helper function to move files
def move_files(file):
    import shutil
    if ".ann" in file:
        try:
            shutil.move(os.path.join(INPUT_FILES_DIRECTORY, file), os.path.join(OUTPUT_ANNOTATED_DIRECTORY, file))
            print("Annotated files moved successfully to ./output_files_annotated.")
        except shutil.SameFileError:
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except:
            print("Error occurred while moving the file.")
    elif ".ann" not in file:
        try:
            shutil.move(os.path.join(INPUT_FILES_DIRECTORY, file), os.path.join(ARCHIVE_DIRECTORY, file))
            print("Original files moved successfully to ./archive.")
        except shutil.SameFileError:
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except:
            print("Error occurred while moving the file.")

# Function for annotating variants.
def annotate(args):
    
    import os
    import glob
    import pandas as pd
    from alive_progress import alive_bar
    import time
    import shutil

    os.chdir(os.path.join(os.getcwd(), CLINVAR_DATABASE_DIRECTORY))

    annotation_f = args.annotation_file
    
    #os.chdir(CLINVAR_DATABASE_DIRECTORY)
    annotation_df = pd.read_csv(annotation_f, sep="\t")
    
    for f in annotation_df.Identifier.iloc[[-1]]:
      if f != "0:000000:Valid:File":
          print("Invalid annotation file encountered!")
          exit()

    print("Starting annotation of variants in files from ./input_files...")
    
    os.chdir(r"..")
    os.chdir(os.path.join(os.getcwd(), INPUT_FILES_DIRECTORY))
    files_for_annotation = glob.glob("*")

    if len(files_for_annotation) == 0:
        print("./input_files is empty - provide files for annotation.")
        return

    for a in files_for_annotation:
        print(f"Annotating file: {a}")
        nlines = check_and_skip(a)

        # could you replace each of these blocks with a function?
        # because they seem repetive
        if a.endswith(".tsv"):
            an_file = pd.read_csv(a, sep=("\t"), skiprows=nlines)
            with alive_bar(an_file.shape[0]) as bar:
                for _ in range(an_file.shape[0]):
                    time.sleep(0)
                    bar()
                an_file = column_identifier(an_file)
                an_file = pd.merge(an_file, annotation_df, how="left", on="Identifier")
                an_file["Clinical_significance"] = an_file["Clinical_significance"].fillna("Manually inspection needed.")
                an_file.to_csv(a[:-3] + "ann" + ".tsv", sep="\t")

        elif a.endswith(".xlsx"):
            an_file = pd.read_excel(a, skiprows=nlines)
            with alive_bar(an_file.shape[0]) as bar:
                for _ in range(an_file.shape[0]):
                    time.sleep(0)
                    bar()
                an_file = column_identifier(an_file)
                an_file = pd.merge(an_file, annotation_df, how="left", on="Identifier")
                an_file["Clinical_significance"] = an_file["Clinical_significance"].fillna("Manually inspection needed.")
                an_file.to_excel(a[:-4] + "ann" + ".xlsx", index=False)

        elif a.endswith(".csv"):
            an_file = pd.read_csv(a, skiprows=nlines)
            with alive_bar(an_file.shape[0]) as bar:
                for _ in range(an_file.shape[0]):
                    time.sleep(0)
                    bar()
                an_file = column_identifier(an_file)
                an_file = pd.merge(an_file, annotation_df, how="left", on="Identifier")
                an_file["Clinical_significance"] = an_file["Clinical_significance"].fillna("Manually inspection needed.")
                an_file.to_csv(a[:-3] + "ann" + ".csv")

    
    os.chdir("..")
    files_to_move = glob.glob(os.path.join(os.getcwd(), INPUT_FILES_DIRECTORY, "*"))
    for move_file in files_to_move:
        move_files(os.path.basename(move_file))

# AWESOME!
# ROLLING!
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="========== CANVAR ==========", epilog="Author: kraesing // Contact: lau.kraesing.vestergaard@regionh.dk // GitHub: https://github.com/kraesing // Molecular Unit, Department of Pathology, Herlev Hospital, University of Copenhagen, DK-2730 Herlev, Denmark." )
    subparser = parser.add_subparsers(help="Info")

    parser_import_packages = subparser.add_parser("packages", help="Installation and importation of packages for CANVAR")
    parser_import_packages.add_argument("-i", "--import_packages", type=str, metavar="", required=True,
                                        help="No input, command only. Example: [~/CANNOV.py packages -i Y]")
    parser_import_packages.set_defaults(func=import_packages)

    parser_prearrange = subparser.add_parser("prearrange", help="Creates the working environment for CANVAR")
    parser_prearrange.add_argument("-w", "--wrkdir", type=str, metavar="", required=True,
                                   help="Input the absolute path to where the working environment can be established. Example: [~/CANVAR.py prearrange -w H:/Path/to/dir]. After creating the working environment, change the directory to /ClinVar_dir.")
    parser_prearrange.set_defaults(func=prearrange)

    parser_download_db = subparser.add_parser("download_db", help="Download database file from ClinVar - https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh[37/38]/")
    parser_download_db.add_argument("-l", "--latest_file", metavar="", required=False,
                                    help="Download the latest database file from ClinVar. Example: [~/CANVAR.py download_db -l latest]")
    parser_download_db.add_argument("-a", "--archive_file", metavar="", required=False,
                                    help="Input the year of which to search the ClinVar database with and choose a specific file to download. Example: [~/CANVAR.py download_db -a 2023]")
    parser_download_db.set_defaults(func=download_db)

    parser_check_construct = subparser.add_parser("check_construct", help="Creates an annotation file with the right format needed as input for 'CANVAR.py annotate'")
    parser_check_construct.add_argument("-d", "--database_file", metavar="", required=True,
                                        help="Input the database file downloaded with 'download_db -l latest'. Takes both gz and vcf as input. Example: [~/CANVAR.py check_construct -d clinvar_20230923.vcf.gz] or [~/CANNOV.py check_construct -d clinvar_20230923.vcf]")
    parser_check_construct.set_defaults(func=check_construct)

    parser_annotate = subparser.add_parser("annotate", help="Annotates variants - Remember to move files to be annotated (.tsv, .csv or .xlsx) to ./input_files")
    parser_annotate.add_argument("-f", "--annotation_file", metavar="", required=True,
                                 help="Input the output file from 'check_construct'. Example: [~/CANVAR.py annotate -f clinvar_20230923.tsv]")
    parser_annotate.set_defaults(func=annotate)

    args = parser.parse_args()
    if args.func:
        args.func(args)
