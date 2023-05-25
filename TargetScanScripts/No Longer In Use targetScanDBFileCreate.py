# This is a sample Python script.
import pandas
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import requests
import psycopg2
from sqlalchemy import create_engine



def load_genes():
    required_fields = pd.read_excel(r'input_files/fields.xlsx')
    geneList = pd.read_excel(r'input_files/GeneList.xlsx')
    return geneList, required_fields


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # establishing the connection
    conn = psycopg2.connect(
        database="TargetScan", user='postgres', password='8069', host='localhost', port='5432'
    )
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Creating table as per requirement

    conservedSiteContextScoresSQL = '''DROP TABLE IF EXISTS conservedSiteContextScores; CREATE TABLE conservedSiteContextScores 
(
    GeneID	VARCHAR(512),
    GeneSymbol	VARCHAR(512),
    TranscriptID	VARCHAR(512),
    GeneTaxID	INT,
    miRNA	VARCHAR(512),
    SiteType	INT,
    UTRstart	INT,
    UTRend INT,
    "context++score" DOUBLE PRECISION,
    "context++scorepercentile"	INT,
    "weightedcontext++score" DOUBLE PRECISION,
    "weightedcontext++scorepercentile"	INT
)'''

    nonConservedSiteContextScoresSQL = '''DROP TABLE IF EXISTS nonConservedSiteContextScores; CREATE TABLE nonConservedSiteContextScores 
    (
        GeneID	VARCHAR(512),
        GeneSymbol	VARCHAR(512),
        TranscriptID	VARCHAR(512),
        GeneTaxID	INT,
        miRNA	VARCHAR(512),
        SiteType	INT,
        UTRstart	INT,
        UTRend INT,
        "context++score" DOUBLE PRECISION,
        "context++scorepercentile"	INT,
        "weightedcontext++score" DOUBLE PRECISION,
        "weightedcontext++scorepercentile"	INT
    )'''

    # Need to changes after

    cursor.execute(conservedSiteContextScoresSQL)
    cursor.execute(nonConservedSiteContextScoresSQL)
    print("Table created successfully........")

    conn.commit()
    conn.close()

    conservedValues = pd.read_csv("targetscandata/Conserved_Site_Context_Scores.txt", sep='\t')
    print(conservedValues.head())
    nonConservedValues = pd.read_csv("targetscandata/Nonconserved_Site_Context_Scores.txt", sep='\t')

    engine = create_engine('postgresql://postgres:8069@localhost:5432/TargetScan')

    conservedValues.to_sql('conservedSiteContextScores', engine, if_exists='append', index=False)
    nonConservedValues.to_sql('nonConservedSiteContextScores', engine, if_exists='append', index=False)

    #It just takes a while to go but it will store all the values in the database
