from django.shortcuts import render
import pandas as pd
from json import dumps
import os
import re
from itertools import zip_longest
# Create your views here.

from django.http import HttpResponse
from .models import GlycoOnto

GENE_INFORMATION_FILE = '../data/gene_general_information.csv'
GENE_COMMENT_FILE = '../data/gene_other_information.csv'
PATHWAY_GENE_MAPPING_FILE = '../data/pathway_gene_figure_mapping.csv'
HTML_FOLDER = '../data/html600/'
FIGURE_FOLDER = '../data/figures/'
MI_RESULTS_FILE = '../data/mi_results.txt'
GPT_TEXT_FILE = '../data/gpt/'


def index(request):
    data = GlycoOnto.objects.all()
    return render(request, 'GlycoEnzDB.html', {'data': data})


def search(request, gene_name=''):

    # Ontology Data
    onto_data = GlycoOnto.objects.all()
    onto_df = pd.DataFrame(onto_data.values())

    onto_graph_functions = {}
    onto_graph_pathways = {}
    gene_names = {}

    functions = onto_df['function'].unique()

    for func in functions:
        onto_graph_functions[func] = {}
        sub_functions = onto_df.loc[onto_df['function'] == func]['sub_function'].unique()
        gene_names[func + '_NULL_NULL_NULL'] = sorted(list(onto_df.loc[onto_df['function'] == func][
                                                                  'gene_name'].unique()))

        for s_func in sub_functions:
            onto_graph_functions[func][s_func] ={}
            sub_sub_functions = onto_df.loc[(onto_df['function'] == func) &
                                            (onto_df['sub_function'] == s_func)]['sub_sub_function'].unique()

            gene_names[func + '_' + s_func + '_NULL_NULL'] = sorted(list(onto_df.loc[(onto_df['function'] == func) &
                                                                              (onto_df['sub_function'] == s_func)][
                                                                      'gene_name'].unique()))

            for s_s_func in sub_sub_functions:
                onto_graph_functions[func][s_func][s_s_func] = {}
                sub_sub_sub_functions = onto_df.loc[(onto_df['function'] == func)
                                                                                & (onto_df['sub_function'] == s_func)
                                                                                & (onto_df['sub_sub_function'] == s_s_func)]['sub_sub_sub_function'].unique()
                gene_names[func + '_' + s_func + '_' + s_s_func + '_NULL'] = sorted(list(
                    onto_df.loc[(onto_df['function'] == func)
                                & (onto_df['sub_function'] == s_func)
                                & (onto_df['sub_sub_function'] == s_s_func)]['gene_name'].unique()))
                
                for s_s_s_func in sub_sub_sub_functions:
                    onto_graph_functions[func][s_func][s_s_func][s_s_s_func] = \
                        sorted(list(onto_df.loc[(onto_df['function'] == func)
                                    & (onto_df['sub_function'] == s_func)
                                    & (onto_df['sub_sub_function'] == s_s_func)
                                    & (onto_df['sub_sub_sub_function'] == s_s_s_func)]['gene_name'].unique()))

                    gene_names[func + '_' + s_func + '_' + s_s_func + '_' + s_s_s_func] = \
                        onto_graph_functions[func][s_func][s_s_func][s_s_s_func]

    pathways = onto_df['pathway'].unique()

    for path in pathways:
        onto_graph_pathways[path] = {}
        sub_paths = onto_df.loc[onto_df['pathway'] == path]['sub_pathway'].unique()
        gene_names[path + '_NULL_NULL_NULL_NULL_NULL'] = sorted(list(onto_df.loc[onto_df['pathway'] == path][
                                                                  'gene_name'].unique()))

        for s_path in sub_paths:
            onto_graph_pathways[path][s_path] ={}
            sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path) &
                                            (onto_df['sub_pathway'] == s_path)]['sub_sub_pathway'].unique()

            gene_names[path + '_' + s_path + '_NULL_NULL_NULL_NULL'] = sorted(list(onto_df.loc[(onto_df['pathway'] == path) &
                                            (onto_df['sub_pathway'] == s_path)]['gene_name'].unique()))
            for s_s_path in sub_sub_pathways:
                onto_graph_pathways[path][s_path][s_s_path] = {}
                sub_sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path)
                                                    & (onto_df['sub_pathway'] == s_path)
                                                    & (onto_df['sub_sub_pathway'] == s_s_path)][
                    'sub_sub_sub_pathway'].unique()
                gene_names[path + '_' + s_path + '_' + s_s_path + '_NULL_NULL_NULL'] = sorted(list(onto_df.loc[(onto_df['pathway'] == path)
                                                    & (onto_df['sub_pathway'] == s_path)
                                                    & (onto_df['sub_sub_pathway'] == s_s_path)]['gene_name'].unique()))
                
                for s_s_s_path in sub_sub_sub_pathways:
                    onto_graph_pathways[path][s_path][s_s_path][s_s_s_path] = {}
                    sub_sub_sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path)
                                                        & (onto_df['sub_pathway'] == s_path)
                                                        & (onto_df['sub_sub_pathway'] == s_s_path)
                                                        & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)][
                        'sub_sub_sub_sub_pathway'].unique()
                    gene_names[path + '_' + s_path + '_' + s_s_path + '_' + s_s_s_path + '_NULL_NULL'] = sorted(list(onto_df.loc[(onto_df['pathway'] == path)
                                                        & (onto_df['sub_pathway'] == s_path)
                                                        & (onto_df['sub_sub_pathway'] == s_s_path)
                                                        & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)]['gene_name'].unique()))
                    
                    for s_s_s_s_path in sub_sub_sub_sub_pathways:
                        onto_graph_pathways[path][s_path][s_s_path][s_s_s_path][s_s_s_s_path] = {}
                        sub_sub_sub_sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path)
                                                            & (onto_df['sub_pathway'] == s_path)
                                                            & (onto_df['sub_sub_pathway'] == s_s_path)
                                                            & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)
                                                            & (onto_df['sub_sub_sub_sub_pathway'] == s_s_s_s_path)][
                            'sub_sub_sub_sub_sub_pathway'].unique()
                        gene_names[path + '_' + s_path + '_' + s_s_path + '_' + s_s_s_path + '_' + s_s_s_s_path +'_NULL'] = sorted(list(onto_df.loc[(onto_df['pathway'] == path)
                                                            & (onto_df['sub_pathway'] == s_path)
                                                            & (onto_df['sub_sub_pathway'] == s_s_path)
                                                            & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)
                                                            & (onto_df['sub_sub_sub_sub_pathway'] == s_s_s_s_path)]['gene_name'].unique()))

                        for s_s_s_s_s_path in sub_sub_sub_sub_sub_pathways:
                            onto_graph_pathways[path][s_path][s_s_path][s_s_s_path][s_s_s_s_path][s_s_s_s_s_path] = \
                                sorted(list(onto_df.loc[(onto_df['pathway'] == path)
                                            & (onto_df['sub_pathway'] == s_path)
                                            & (onto_df['sub_sub_pathway'] == s_s_path)
                                            & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)
                                            & (onto_df['sub_sub_sub_sub_pathway'] == s_s_s_s_path )
                                            & (onto_df['sub_sub_sub_sub_sub_pathway'] == s_s_s_s_s_path)]['gene_name'].unique()))

                            gene_names[path + '_' + s_path + '_' + s_s_path + '_' + s_s_s_path + '_' + s_s_s_s_path + '_' + s_s_s_s_s_path] = \
                                onto_graph_pathways[path][s_path][s_s_path][s_s_s_path][s_s_s_s_path][s_s_s_s_s_path]
    # General information
    gene_general_info = {'message': "Welcome to GlycoEnzDB"}
    gene_html = ""
    figure_url = ""
    reaction_img = ""
    tf_table_html = ""
    gpt_txt = ""
    if gene_name:
        gene_general_info = get_gene_general_info(GENE_INFORMATION_FILE, gene_name)
        gene_general_info['Comments'] = get_gene_other_info(GENE_COMMENT_FILE, gene_name)
        gene_html = get_gene_html(HTML_FOLDER, gene_name)
        figure_url = get_pathway_fig_url(PATHWAY_GENE_MAPPING_FILE, gene_name)
        reaction_img = f'/reaction_imgs/{gene_name}.png' 
        tf_table_html = get_tf_html(MI_RESULTS_FILE, gene_name)
        gpt_txt = get_gpt_txt(GPT_TEXT_FILE, gene_name)

    return render(request, 'GlycoEnzDB.html', {'onto_graph_pathways': onto_graph_pathways,
                                               'onto_graph_functions': onto_graph_functions,
                                               'gene_names': dumps(gene_names),
                                               'gene_name':gene_name,
                                               'gene_general_info': gene_general_info,
                                               'gene_html': gene_html,
                                               'figure_url': figure_url,
                                               'reaction_img': reaction_img,
                                               'tf_table_html': tf_table_html,
                                               'gpt_txt': gpt_txt})


def get_gene_general_info(filename, gene_name):
       # Get the current directory
        current_dir = os.path.dirname(__file__)

        # Construct the path to the file
        file_path = os.path.join(current_dir, filename)        

        general_information_df =  pd.read_csv(file_path)
        general_information_df.fillna("", inplace=True)
        general_information_df = general_information_df.loc[general_information_df['Gene Name'] == gene_name]

        if len(general_information_df) > 0:
            gene_general_info = general_information_df.to_dict('records')[0]
            gene_general_info['HGNC number'] = re.sub("[^0-9]", "", gene_general_info['HGNC number'])
            gene_general_info['GeneID'] = re.sub("[^0-9]", "", gene_general_info['GeneID'])
            gene_general_info['CAZy'] = gene_general_info['CAZy'].replace(";","")
            gene_general_info['Catalytic: Rhea'] = list(map( lambda x: re.sub("[^0-9]", "", x), gene_general_info['Catalytic: Rhea'].split(";")))
            gene_general_info['Catalytic: EC'] = list(map(lambda x: {'name':x, 'url': x.replace(".", "/")}, gene_general_info['Catalytic: EC'].split(";")))
            gene_general_info['Brenda'] = gene_general_info['Brenda'].split(";")
            gene_general_info['Reactome ID'] = gene_general_info['Reactome ID'].split(";")
            gene_general_info['OMIM'] = gene_general_info['OMIM'].split(";")

            # gene_general_info['Catalytic Activity'] = list(zip_longest(gene_general_info['Catalytic: Rhea'], gene_general_info['Catalytic: EC'], 
            #                                                    gene_general_info['Brenda'], gene_general_info['Reactome ID'], fillvalue=''))
        else:
            gene_general_info['message'] = "Invalid Gene Name in the URL"

        return gene_general_info

def get_gene_other_info(filename, gene_name):
       # Get the current directory
        current_dir = os.path.dirname(__file__)

        # Construct the path to the file
        file_path = os.path.join(current_dir, filename)        

        other_info_df =  pd.read_csv(file_path)
        other_info_df.fillna("", inplace=True)
        other_info_df = other_info_df.loc[other_info_df['GeneSymbol'] == gene_name]

        comments = []
        if len(other_info_df) > 0:
            comment = other_info_df['Comments'].iloc[0]
            for c in comment.split("*"):
                c = c.strip()
                if c:
                    comments.append(c)
        return comments


def get_gene_html(filename, gene_name):
    
    current_dir = os.path.dirname(__file__)
    # Construct the path to the file
    file_path = os.path.join(current_dir, filename + gene_name+ '.html')

    try:
        with open(file_path, 'r') as file:
            html_string = file.read()
            return html_string
    except FileNotFoundError:
        return ""

def get_tf_html(filename, gene_name):
    
    current_dir = os.path.dirname(__file__)
    # Construct the path to the file
    file_path = os.path.join(current_dir, filename)

    try:
        tf_df = pd.read_csv(file_path, sep='\t')
        tf_df.columns = ['TF','Gene', 'Score']
        tf_df = tf_df[tf_df['Gene'] == gene_name]
        tf_table_html = tf_df[['TF', 'Score']].sort_values(by='Score', ascending=False).head(10).to_html(index=False)
        return tf_table_html
    except FileNotFoundError:
        return ""      

def get_pathway_fig_url(filename, gene_name):
     
    PATHWAY_GENE_MAPPING = {'Nucleotide': 'HK1,HK2,HK3,GCK,G6PC1,GPI,MPI,PMM1,PMM2,GMPPA,GMPPB,GNPDA1,GNPDA2,NAGK,UAP1,GNPNAT1,GFPT1,GFPT2,GALK2,NANS,CMAS,DPM1,DPM2,DPM3,GMDS,TSTA3,FPGT,FCGS,GNE,GALE,GALK1,GALT,ALG5,UGP2,HGDH,UXS1,PGM1,PGM2,PGM3,CMAH,RENBP'}
    url = ''

    for p in PATHWAY_GENE_MAPPING:
        if gene_name in PATHWAY_GENE_MAPPING[p].replace(' ', '').split(','):
            url = f'/glycoenzdb/static/pathway_figures/{p}/{p}.html'
            return url
    return url

def get_gpt_txt(folder_name, gene_name):
    
    current_dir = os.path.dirname(__file__)
    # Construct the path to the file
    file_path = os.path.join(current_dir, folder_name + gene_name+ '.txt')

    try:
        with open(file_path, 'r') as file:
            gpt_txt = file.read()
            gpt_txt = gpt_txt.strip()
            return gpt_txt
    except FileNotFoundError:
        return ""
         