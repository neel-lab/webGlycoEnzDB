## Purpose
The targetScanDBFile.py will read the text files produced by TargetScan through manual download 
and extraction using https://www.ezyzip.com/unzip-tar-gz-file-online.html# The script will then query
the files based on human, the gene symbol, the context++ score and the context++ score percentile. TargetScan
will then be used with https://grch37.ensembl.org/index.html to find the sequence value of each miRNA.

TargetScan Files: https://www.targetscan.org/cgi-bin/targetscan/data_download.vert80.cgi


## How to:
1. _targetscandata_ directory will contain the text files from TargetScan and the gene list as an excel file
2. The main function will be run when you run the script
   - The main function will load all the genes, and then it will read the text files. After reading the files
   it will then select a subsection of the entirety of the data set through the method: trimdata(dataframe, genelist). 
   This method will allow you to change the criteria on selecting the subset as well as reduce the time needed to search
   the dataset by adding multiple conditions through each row search. It will then produce three csv files, one for conserved
   sites and one for non-conserved sites and one reduced miRFamily csv file that only shows human genes.
3. All of the csv files will be located within the _TrimmedDataFiles_ directory



Ensembl Variables Used:
- Transcript stable ID version
- cDNA sequences
- Gene name
- Gene Stable ID
- Transcript length including UTRs and CDS
- cDNA coding start
- cDNA coding end