import pandas as pd
import os

# Step 1: Read the Excel file and extract unique gene names
excel_path = r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\dataloader\data\GlycoEnzOntoDB.xlsx"
df = pd.read_excel(excel_path)
master_list = set(df['gene_name'].dropna().unique())

# Single cell data
singlecell = r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\singlecellData\singleCellData\Supplementary Tables.xlsx"
df = pd.read_excel(singlecell, skiprows=2)
single_cell = set(df['Gene Symbol'].dropna().unique())
print("singlecell - list members that are missing from master_list (add these!): ", master_list-single_cell)
print("Available in single_cell, but not really needed:", single_cell-master_list)
print()

# Uniprot data
Uniprot_file = r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\uniprotDataScript\input_files\GeneList.xlsx"
df = pd.read_excel(Uniprot_file)
Uniprot_data = set(df['Genes'].dropna().unique())
print("Uniprot_data - list members that are missing from master_list (add these!): ", master_list-Uniprot_data)
print("Available in Uniprot_data, but not really needed:", Uniprot_data-master_list)
print()

# General information
file = r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\djangoProject/data/gene_general_information.csv"
df = pd.read_csv(file)
general_list = set(df['Gene Name'].dropna().unique())
print("general_list - list members that are missing from master_list (add these!): ", master_list-general_list)
print("Available in general_list, but not really needed:", general_list-master_list)
print()

# need to add checks for general text
parameters = ['CRISPR', 'GPT', 'drawglycan', 'TF', "TF_geneNetGlyco"]
paths = [r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\djangoProject\webGlycoEnzDB\static\CRISPR\CRISPRa",
         r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\djangoProject\data\gpt",
         r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\djangoProject\webGlycoEnzDB\static\reaction_imgs",
         r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\djangoProject\data\html600",
         r"C:\Users\neel\Documents\GitHub\webGlycoEnzDB\geneNetGlyco\figures\glycogenes\html600"]
delimiters = ["-", ".", ".", ".", "."]


combined_data = zip(parameters, paths, delimiters)

# Step 2: Read file names from the CRISPRa directory
for parameter, path, delimiter in combined_data:
    file_names = os.listdir(path)
    param_list = [file.split(delimiter)[0] for file in file_names]  # Remove text after the first '-'
    param_list_set = set(param_list)
    unique_to_master = master_list - param_list_set
    unique_to_CRISPRa = param_list_set - master_list
    print(parameter, "-list members that are missing from master_list (add these!): ", unique_to_master)
    print("Available in " + parameter + "-list, but not really needed:", unique_to_CRISPRa)
    print()
