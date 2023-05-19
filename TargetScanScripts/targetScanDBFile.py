# This is a sample Python script.
import pandas
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from sqlalchemy import create_engine


# Press the green button in the gutter to run the script.
def trimdata(dataframe, genelist):
    dataFrameTrimmed = dataframe[(dataframe["Gene Tax ID"] == 9606) & (dataframe["Gene Symbol"].isin(genelist))
                                 & (dataframe["context++ score"] < -0.25) & (dataframe["context++ score percentile"] > 90)]
    return dataFrameTrimmed


# ABO

if __name__ == '__main__':
    geneDataframe = pd.read_excel(r'targetscandata/GeneList.xlsx')
    geneList = geneDataframe.iloc[:, 0].tolist()

    conservedValues = pd.read_csv("targetscandata/Conserved_Site_Context_Scores.txt", sep='\t')
    conservedValuesHumansTrimmed = trimdata(conservedValues, geneList)
    conservedValuesHumansTrimmed.to_csv(path_or_buf="TrimmedDataFiles/conservedTrimmed.csv", index=False)

    # GeneList shows 403
    # Without context++ score reduction: the conservedValues have 5743: only has 296 unique Gene Symbols in Excel
    # Without Gene Symbol in geneList: 13072 unique Gene Symbols
    # With everything -> only has 246 Gene Symbols

    nonConservedValues = pd.read_csv("targetscandata/Nonconserved_Site_Context_Scores.txt", sep='\t')
    nonConservedValuesHumansTrimmed = trimdata(nonConservedValues, geneList)
    nonConservedValuesHumansTrimmed.to_csv(path_or_buf="TrimmedDataFiles/nonConservedTrimmed.csv", index=False)

    miRFamily = pd.read_csv("targetscandata/miR_Family_Info.txt", sep='\t')
    miRFamilyHumansTrimmed = miRFamily[miRFamily["Species ID"] == 9606]
    miRFamilyHumansTrimmed.to_csv(path_or_buf="TrimmedDataFiles/miRFamilyHumansTrimmed.csv", index=False)

    conservedValuesHumansTrimmed["Conserved"] = "Conserved"
    nonConservedValuesHumansTrimmed["Conserved"] = "Nonconserved"
    mergedValues = pd.concat([conservedValuesHumansTrimmed, nonConservedValuesHumansTrimmed], ignore_index=True)

    reducedMergedValues = mergedValues[mergedValues["miRNA"].isin(miRFamilyHumansTrimmed["MiRBase ID"])]

    mergedValuesAddColumns = pd.DataFrame(columns=["Mature Sequence", "Seed+m8"])

    # Site Types: 7mer-1a (1), 7mer-m8(2), 8mer (3), or 6mer (4)
    count = 0
    for row in mergedValues["Site Type"]:
        if row == 3:
            mergedValues["Site Type"][count] = "8mer"
        elif row == 2:
            mergedValues["Site Type"][count] = "7mer-m8"
        elif row == 1:
            mergedValues["Site Type"][count] = "7mer-1a"
        else:
            mergedValues["Site Type"][count] = "6mer"
        count += 1

    for index, row in mergedValues.iterrows():
        mirFamilyInfoPerGene = miRFamilyHumansTrimmed[miRFamilyHumansTrimmed["MiRBase ID"] == (row[4])]
        mergedValuesAddColumns.loc[len(mergedValuesAddColumns)] = [mirFamilyInfoPerGene["Mature sequence"].values[0],
                                                                   mirFamilyInfoPerGene["Seed+m8"].values[0]]

    mergedValues["Mature Sequence"] = mergedValuesAddColumns["Mature Sequence"]
    mergedValues["Seed+m8"] = mergedValuesAddColumns["Seed+m8"]

    mergedValues.to_csv(path_or_buf="TrimmedDataFiles/mergedValues.csv", index=False)
