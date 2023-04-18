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

## Some Info Needed:
- Brenda, Rhea, etc. are IDs associated with other databases that can be constructed with hyperlinks
  - Brenda: https://www.brenda-enzymes.org/enzyme.php?ecno=2.8.2.20&UniProtAcc=O60507
    - ecno will be the Brendan ID and UniProtAcc field is the Uniprot ID
  - Rhea: https://www.rhea-db.org/rhea?query=ec:2.8.2.20
    - ec is the rhea ID
  - Reactome: https://reactome.org/PathwayBrowser/#R-HSA-156584&FLG=O60507
    - The reactome ID will be placed after the # symbol and FLG is the uniprot ID
  - CAZy: http://www.cazy.org/CBM13.html
    - CAZy ID replacing CMB13
  - HGNC: https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:12020
    - Replace the HGNC:12020 or replace the 12020 for new hyperlink
  - NCBI (aka GeneID): https://www.ncbi.nlm.nih.gov/gene/2683
    - Replace the last 4 numbers
    - KEGG value -> same as NCBI value 4 numbers
  - EC
- Some database fields don't have the same amount of references because some reaction don't have it
