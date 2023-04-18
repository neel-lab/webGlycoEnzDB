## Purpose
The uniprotScript.py access the UniProt database API and then queries it based on 
the organism taxonomy ID and return fields. It will produce a semicolon separated values file in Excel with the return fields
populated. The input is an Excel file with a list of genes. 

## How to:
1. Input file directory has the gene file where all the genes are in a column
2. Ensure the input file directory has the fields excel in each column
3. Make sure the unipro_API_call method fields contain all the fields that you want
   - The fields can be found here: https://www.uniprot.org/help/return_fields
   - The taxonomy ID can be changed to another organism
4. The main function will be run when you run the script
   - The main function will load all the fields and gene list, and then it will iterate through each gene in the gene list 
   to the API call. The required fields will pull the information from the response of the API. It will produce a new dataframe with just one
   row that has the information in the required field. From there the new row is added into the required field dataframe that 
   will be returned through conversion to a csv file. There will be a constant print of the gene that the script is currently
   at so if there is any errors, the user can know which specific gene is breaking the code if you add more and new fields to the API calls.
5. The script will produce the csv file in the output file directory.

## Add links (examples given below for B4GALT1):
1.	General information: 
HGNC: https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:924\n
NCBI: https://www.ncbi.nlm.nih.gov/gene/2683\n
UniProt: https://www.uniprot.org/uniprotkb/P15291/entry\n
CAZy: http://www.cazy.org/GT7.html\n
GlyGen: https://glygen.org/protein/P15291\n

2. Notes:\n
This is available in original database output\n

3. Catalytic activity:\n
Reactions are available but we need to convert these to DawGlycan format\n

4. Reaction and disease links:\n
Rhea: https://www.rhea-db.org/rhea/12404\n
E.C. Number (IUBMB): https://iubmb.qmul.ac.uk/enzyme/EC2/4/1/22.html\n
Brenda: https://www.brenda-enzymes.org/enzyme.php?ecno=2.4.1.256\n
Reactome: https://reactome.org/PathwayBrowser/#R-HSA-1912420\n
KEGG: https://www.genome.jp/dbget-bin/www_bget?hsa:2683\n
OMIM: https://www.omim.org/entry/137060
