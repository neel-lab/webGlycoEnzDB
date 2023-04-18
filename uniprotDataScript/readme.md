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
- Some database fields don't have the same amount of references because some reaction don't have it
