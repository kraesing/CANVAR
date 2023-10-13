# =============================================================================
#                               Project CANVAR
# =============================================================================
# author: kraesing
# mail: lau.kraesing.vestergaard@regionh.dk 
# GitHub: https://github.com/kraesing

# Importing libraries!
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import sys
import argparse
import subprocess
import pkg_resources
 
#%% Define paths for directories
WORKING_DIRECTORY = "canvar"
ARCHIVE_DIRECTORY = "archive"
INPUT_FILES_DIRECTORY = "input_files"
OUTPUT_ANNOTATED_DIRECTORY = "output_files_annotated"
CLINVAR_DATABASE_DIRECTORY = "clinvar_database_files"
LINK_INTERNET = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/" 
ASSEMBLY = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh"
ARCHIVE_VER = "archive_2.0/"

#%% Define constants for package requirements
REQUIRED_PACKAGES = {"regex == 2022.3.15", 
                     "numpy == 1.24.4", 
                     "pandas == 1.4.2", 
                     "alive-progress == 1.6.2", 
                     "tabulate == 0.8.9", 
                     "requests == 2.27.1", 
                     "wget == 3.2",
                     "openpyxl == 3.1.2"}
    
#%% Function to install required packages
def import_packages(args):
    
    missing_packages = REQUIRED_PACKAGES - {pkg.key for pkg in pkg_resources.working_set}
    if args.import_packages == "Y":
        for package in missing_packages:
            print(f"installing... {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("Needed packages have been imported")
    else:
        print("Input not available")
                           
#%% Function to create and manage directories
# Helper function to create or validate a directory
def create_or_validate_directory(directory):
    
    import time
    
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
def clinvar_table_data(clinvar_db_file):
    
    import pandas as pd
    
    clinvar_db_file_df= pd.DataFrame(clinvar_db_file, columns=["file_name"])
    clinvar_db_file_df = clinvar_db_file_df.loc[~clinvar_db_file_df["file_name"].str.contains("papu")]
    clinvar_db_file_df = clinvar_db_file_df[~clinvar_db_file_df["file_name"].str.startswith('"clinvar.vcf.gz')]
    
    
    clinvar_db_file_df["Name"] = clinvar_db_file_df["file_name"].str.split(">").str[0].str.strip('"')
    clinvar_db_file_df["Date"] = clinvar_db_file_df["file_name"].str.split(">").str[2].str.split("   ").str[-2]
    clinvar_db_file_df["Size"] = clinvar_db_file_df["file_name"].str.split(">").str[2].str.split("   ").str[-1]
    
    clinvar_db_file_df.drop(columns=["file_name"], inplace=True)
    clinvar_db_file_df = clinvar_db_file_df.reset_index(drop=True)
    
    return clinvar_db_file_df

#%% Function to check internet access.
def check_internet_connection():
    import requests
    try: 
        resp = requests.get(LINK_INTERNET, timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Function to download files. 
def download_db(args):
    	
    if not check_internet_connection():
        print("Internet connection is required for packages and download_db to run")

    import re
    import wget
    import os
    
    os.chdir(os.path.join(os.getcwd(), CLINVAR_DATABASE_DIRECTORY))
        
    l_file = args.latest_file
    
    if l_file == "latest":
        which_assembly = input("Specify Genome Reference Consortium Human assembly [37/38]: ")
        link = ASSEMBLY + f"{which_assembly}/"
        
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
        link_archive = ASSEMBLY + f"{which_assembly}/" + ARCHIVE_VER
        a_file = args.archive_file
        a_file = str(a_file)
    
        print(f"Searching ClinVar for database files from {a_file}...\n")
    
        archive_url = link_archive + a_file + "/"
     
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
    
    import re
    import pandas as pd
    
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
    print(f"Task[8/8] - Saving file into ./{CLINVAR_DATABASE_DIRECTORY}")
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
def column_identifier(ann_file_):
    
    ann_file_["Identifier"] = ann_file_["Locus"] + ":" + ann_file_["Ref"] + ":" + ann_file_["Observed Allele"]
    ann_file_["Identifier"] = ann_file_["Identifier"].astype("str")
    ann_file_["Identifier"] = ann_file_["Identifier"].str.replace("chr", "")
    
    return ann_file_

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

# Helper function for progress
def alive_bar_(ann_file):
    
    from alive_progress import alive_bar
    import time
    
    with alive_bar(ann_file.shape[0]) as bar:
        for _ in range(ann_file.shape[0]):
            time.sleep(0)
            bar()

# Helper function for handling annotations of files.
def file_type_handling(a, nlines, annotation_df):
    
    import pandas as pd
    
    doc_type = a.split(".")[-1]
        
    if doc_type == "tsv":
        ann_file = pd.read_csv(a, sep=("\t"), skiprows=nlines)
        alive_bar_(ann_file)
        
    elif doc_type == "xlsx":
        ann_file = pd.read_excel(a, skiprows=nlines)
        alive_bar_(ann_file)
           
    elif doc_type == "csv":
        ann_file = pd.read_csv(a, sep=(";"), skiprows=nlines)
        alive_bar_(ann_file)
        
    ann_file = column_identifier(ann_file)
    ann_file = pd.merge(ann_file, annotation_df, how="left", on="Identifier")
    ann_file["Clinical_significance"] = ann_file["Clinical_significance"].fillna("Manually inspection needed.")
        
    if doc_type == "tsv":
        ann_file.to_csv(a[:-len(doc_type)] + "ann" + f".{doc_type}", sep="\t")
    elif doc_type == "xlsx":
        ann_file.to_excel(a[:-len(doc_type)] + "ann" + f".{doc_type}", index=False)
    elif doc_type == "csv":
        ann_file.to_csv(a[:-len(doc_type)] + "ann" + f".{doc_type}")

# Function for annotating variants.
def annotate(args):
    
    import os
    import glob
    import pandas as pd

    os.chdir(os.path.join(os.getcwd(), CLINVAR_DATABASE_DIRECTORY))

    annotation_f = args.annotation_file
    
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
        
        file_type_handling(a=a, nlines=nlines, annotation_df=annotation_df)
    
    os.chdir("..")
    files_to_move = glob.glob(os.path.join(os.getcwd(), INPUT_FILES_DIRECTORY, "*"))
    for move_file in files_to_move:
        move_files(os.path.basename(move_file))

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
                                   help=f"Input the absolute path to where the working environment can be established. Example: [~/CANVAR.py prearrange -w H:/Path/to/dir]. After creating the working environment, change the directory to {WORKING_DIRECTORY}.")
    parser_prearrange.set_defaults(func=prearrange)

    parser_download_db = subparser.add_parser("download_db", help="Download database file from ClinVar - https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh[37/38]/")
    parser_download_db.add_argument("-l", "--latest_file", metavar="", required=False,
                                    help="Download the latest database file from ClinVar. Example: [~/CANVAR.py download_db -l latest]")
    parser_download_db.add_argument("-a", "--archive_file", metavar="", required=False,
                                    help="Input the year of which to search the ClinVar database with and choose a specific file to download. Example: [~/CANVAR.py download_db -a 2021]")
    parser_download_db.set_defaults(func=download_db)

    parser_check_construct = subparser.add_parser("check_construct", help="Creates an annotation file with the right format needed as input for 'CANVAR.py annotate'")
    parser_check_construct.add_argument("-d", "--database_file", metavar="", required=True,
                                        help="Input the database file downloaded with 'download_db -l latest'. Takes both gz and vcf as input. Example: [~/CANVAR.py check_construct -d clinvar_20230923.vcf.gz] or [~/CANVAR.py check_construct -d clinvar_20230923.vcf]")
    parser_check_construct.set_defaults(func=check_construct)

    parser_annotate = subparser.add_parser("annotate", help="Annotates variants - Remember to move files to be annotated (.tsv, .csv or .xlsx) to ./input_files")
    parser_annotate.add_argument("-f", "--annotation_file", metavar="", required=True,
                                 help="Input the output file from 'check_construct'. Example: [~/CANVAR.py annotate -f clinvar_20230923.tsv]")
    parser_annotate.set_defaults(func=annotate)

    args = parser.parse_args()
    if args.func:
        args.func(args)
