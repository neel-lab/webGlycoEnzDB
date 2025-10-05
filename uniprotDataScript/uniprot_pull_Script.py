# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import requests, os


def uniprot_API_call(gene):
    # Fields will have all the returning values at uniprot api call
    # https://www.uniprot.org/help/return_fields
    fields = "accession,id,gene_names,organism_name,organism_id,protein_name,cc_catalytic_activity,xref_cazy,xref_brenda,xref_reactome,rhea,xref_hgnc,xref_geneid,xref_mim"
    url = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(organism_id:9606)%20AND%20gene=" + gene + "&fields=" + fields
    response = requests.get(url)
    return response.json()


def accessDataFromCall(json, returnFields, gene):
    # Actual method that goes through and selects the information needed
    newRow = pd.DataFrame(columns=returnFields.columns.tolist())
    newRow.loc[0, 'Gene Name'] = gene
    if len(json["results"]) != 0:
        newRow.loc[0, 'Uniprot ID'] = json["results"][0]['primaryAccession']
        newRow.loc[0, 'Organism'] = json["results"][0]['organism']['scientificName']
        newRow.loc[0, 'Taxonomy-ID'] = json["results"][0]['organism']['taxonId']

        for key in json['results'][0]['genes'][0].keys():
            if key == 'synonyms':
                newRow.loc[0, 'Gene synonym'] = json['results'][0]['genes'][0]['synonyms'][0].get('value')

        catalytic_act_values = catalytic_act_rhea_values = ""

        catalytic_ec_set = set()

        for activity in json['results'][0]['comments']:
            catalytic_act_values += activity['reaction'].get('name') + ';'
            for reactionItem in activity['reaction']:
                if reactionItem == 'reactionCrossReferences':
                    for database in activity['reaction'].get('reactionCrossReferences'):
                        if database.get('database') == 'Rhea':
                            catalytic_act_rhea_values += database.get('id') + ';'
                if reactionItem == 'ecNumber':
                    for item in activity['reaction']:
                        if item == 'ecNumber':
                            catalytic_ec_set.add(activity['reaction'].get('ecNumber'))

        newRow.loc[0, 'Catalytic: Reaction'] = catalytic_act_values
        newRow.loc[0, 'Catalytic: Rhea'] = catalytic_act_rhea_values

        shortName = alternativeNames = omim_values = hgnc_values = brenda_values = reactome_values = cazy_values = geneId_values = ""

        for proteinDescriptionName in json['results'][0]['proteinDescription']:
            if proteinDescriptionName == 'recommendedName':
                for styleName in json['results'][0]['proteinDescription']['recommendedName'].keys():
                    if styleName == 'shortNames':
                        for name in json['results'][0]['proteinDescription']['recommendedName']['shortNames']:
                            shortName += name.get('value') + ';'
                    if styleName == 'fullName':
                        newRow.loc[0, 'Recommended Name'] = json['results'][0]['proteinDescription']['recommendedName']['fullName'].get('value')
                    if styleName == 'ecNumbers':
                        for element in json['results'][0]['proteinDescription']['recommendedName']['ecNumbers']:
                            catalytic_ec_set.add(element.get('value'))
            if proteinDescriptionName == 'alternativeNames':
                for name in json['results'][0]['proteinDescription']['alternativeNames']:
                    alternativeNames += name['fullName'].get('value') +';'
                    try:
                        if name['ecNumbers']:
                            # Since ecNumbers is a list, iterate through it or access by index
                            for ec_item in name['ecNumbers']:
                                if isinstance(ec_item, dict) and ec_item.get('value'):
                                    print(f"alt: {ec_item['value'] + ';'}")
                    except (KeyError, TypeError) as e:
                        pass

        catalytic_act_ec_values = ';'.join([ec for ec in catalytic_ec_set if ec is not None])
        if catalytic_act_ec_values:
            catalytic_act_ec_values += ';'
        newRow.loc[0, 'Catalytic: EC'] = catalytic_act_ec_values
        newRow.loc[0, 'Alternative Names'] = alternativeNames
        newRow.loc[0, 'Short Names'] = shortName

        for database in json['results'][0]['uniProtKBCrossReferences']:
            if database.get('database') == 'HGNC':
                hgnc_values += database.get('id') + ';'
            if database.get('database') == 'BRENDA':
                brenda_values += database.get('id') + ';'
            if database.get('database') == 'Reactome':
                reactome_values += database.get('id') + ';'
            if database.get('database') == 'CAZy':
                cazy_values += database.get('id') + ';'
            if database.get('database') == 'MIM':
                omim_values += database.get('id') + ';'
            if database.get('database') == 'GeneID':
                geneId_values += database.get('id') + ';'

        newRow.loc[0, 'Brenda'] = brenda_values
        newRow.loc[0, 'Reactome ID'] = reactome_values
        newRow.loc[0, 'CAZy'] = cazy_values
        newRow.loc[0, 'HGNC number'] = hgnc_values
        newRow.loc[0, 'GeneID'] = geneId_values
        newRow.loc[0, 'OMIM'] = omim_values

    return newRow

def load_genes(dir1):
    # Loading all the genes needed and have the required fields populated
    fields_full_path = os.path.join(dir1, 'fields.xlsx')
    required_fields = pd.read_excel(fields_full_path)
    GeneList_full_path = os.path.join(dir1, 'GeneList.xlsx')
    geneList = pd.read_excel(GeneList_full_path)
#    data = {'Genes': ['GBA1', 'CEMIP', 'ARSA']}            # to add just a few genes to the database
#    geneList = pd.DataFrame(data)
    return geneList, required_fields


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    data_dir = r'C:\Users\neel\Box\cbe-neel\cbe-neel-shared\Website_management\GlycoEnzDB'
    geneList, required_fields = load_genes(data_dir)
    # p1.load_genes
    for gene in geneList.values:
    #gene='TPST1'
        print(gene)
        newRow = pd.DataFrame(columns=required_fields.columns.tolist())
        responseValue = uniprot_API_call(gene[0])
        newRow = accessDataFromCall(responseValue, required_fields, gene[0])
        required_fields.loc[len(required_fields)] = newRow.loc[0]
    output_path = os.path.join(data_dir, 'results.csv')

    # If you want to save it to a new file, you can just change the name results.csv into something else
    required_fields.to_csv(path_or_buf=output_path)