from django.shortcuts import render
import pandas as pd
# Create your views here.

from django.http import HttpResponse
from .models import GlycoOnto


def index(request):
    data = GlycoOnto.objects.all()
    return render(request, 'GlycoEnzDB.html', {'data': data})


def search(request, search_type='', main='', sub1='', sub2='', sub3=''):
    gene_name = request.GET.get('geneName')
    onto_data = GlycoOnto.objects.all()
    onto_df = pd.DataFrame(onto_data.values())

    onto_graph_functions = {}
    onto_graph_pathways = {}
    gene_names = {}

    functions = onto_df['function'].unique()

    for func in functions:
        onto_graph_functions[func] = {}
        sub_functions = onto_df.loc[onto_df['function'] == func]['sub_function'].unique()
        gene_names[func + '_NULL_NULL_NULL'] = list(onto_df.loc[onto_df['function'] == func][
                                                                  'gene_name'])

        for s_func in sub_functions:
            onto_graph_functions[func][s_func] ={}
            sub_sub_functions = onto_df.loc[(onto_df['function'] == func) &
                                            (onto_df['sub_function'] == s_func)]['sub_sub_function'].unique()

            gene_names[func + '_' + s_func + '_NULL_NULL'] = list(onto_df.loc[(onto_df['function'] == func) &
                                                                              (onto_df['sub_function'] == s_func)][
                                                                      'gene_name'])

            for s_s_func in sub_sub_functions:
                onto_graph_functions[func][s_func][s_s_func] = {}
                sub_sub_sub_functions = onto_df.loc[(onto_df['function'] == func)
                                                                                & (onto_df['sub_function'] == s_func)
                                                                                & (onto_df['sub_sub_function'] == s_s_func)]['sub_sub_sub_function'].unique()
                gene_names[func + '_' + s_func + '_' + s_s_func + '_NULL'] = list(
                    onto_df.loc[(onto_df['function'] == func)
                                & (onto_df['sub_function'] == s_func)
                                & (onto_df['sub_sub_function'] == s_s_func)]['gene_name'])
                
                for s_s_s_func in sub_sub_sub_functions:
                    onto_graph_functions[func][s_func][s_s_func][s_s_s_func] = \
                        list(onto_df.loc[(onto_df['function'] == func)
                                    & (onto_df['sub_function'] == s_func)
                                    & (onto_df['sub_sub_function'] == s_s_func)
                                    & (onto_df['sub_sub_sub_function'] == s_s_s_func)]['gene_name'])

                    gene_names[func + '_' + s_func + '_' + s_s_func + '_' + s_s_s_func] = \
                        onto_graph_functions[func][s_func][s_s_func][s_s_s_func]

    pathways = onto_df['pathway'].unique()

    for path in pathways:
        onto_graph_pathways[path] = {}
        sub_paths = onto_df.loc[onto_df['pathway'] == path]['sub_pathway'].unique()
        gene_names[path + '_NULL_NULL_NULL_NULL_NULL'] = list(onto_df.loc[onto_df['pathway'] == path][
                                                                  'gene_name'])

        for s_path in sub_paths:
            onto_graph_pathways[path][s_path] ={}
            sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path) &
                                            (onto_df['sub_pathway'] == s_path)]['sub_sub_pathway'].unique()

            gene_names[path + '_' + s_path + '_NULL_NULL_NULL_NULL'] = list(onto_df.loc[(onto_df['pathway'] == path) &
                                            (onto_df['sub_pathway'] == s_path)]['gene_name'])
            for s_s_path in sub_sub_pathways:
                onto_graph_pathways[path][s_path][s_s_path] = {}
                sub_sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path)
                                                    & (onto_df['sub_pathway'] == s_path)
                                                    & (onto_df['sub_sub_pathway'] == s_s_path)][
                    'sub_sub_sub_pathway'].unique()
                gene_names[path + '_' + s_path + '_' + s_s_path + '_NULL_NULL_NULL'] = list(onto_df.loc[(onto_df['pathway'] == path)
                                                    & (onto_df['sub_pathway'] == s_path)
                                                    & (onto_df['sub_sub_pathway'] == s_s_path)]['gene_name'])
                
                for s_s_s_path in sub_sub_sub_pathways:
                    onto_graph_pathways[path][s_path][s_s_path][s_s_s_path] = {}
                    sub_sub_sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path)
                                                        & (onto_df['sub_pathway'] == s_path)
                                                        & (onto_df['sub_sub_pathway'] == s_s_path)
                                                        & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)][
                        'sub_sub_sub_sub_pathway'].unique()
                    gene_names[path + '_' + s_path + '_' + s_s_path + '_' + s_s_s_path + '_NULL_NULL'] = list(onto_df.loc[(onto_df['pathway'] == path)
                                                        & (onto_df['sub_pathway'] == s_path)
                                                        & (onto_df['sub_sub_pathway'] == s_s_path)
                                                        & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)]['gene_name'])
                    
                    for s_s_s_s_path in sub_sub_sub_sub_pathways:
                        onto_graph_pathways[path][s_path][s_s_path][s_s_s_path][s_s_s_s_path] = {}
                        sub_sub_sub_sub_sub_pathways = onto_df.loc[(onto_df['pathway'] == path)
                                                            & (onto_df['sub_pathway'] == s_path)
                                                            & (onto_df['sub_sub_pathway'] == s_s_path)
                                                            & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)
                                                            & (onto_df['sub_sub_sub_sub_pathway'] == s_s_s_s_path)][
                            'sub_sub_sub_sub_sub_pathway'].unique()
                        gene_names[path + '_' + s_path + '_' + s_s_path + '_' + s_s_s_path + '_' + s_s_s_s_path +'_NULL'] = list(onto_df.loc[(onto_df['pathway'] == path)
                                                            & (onto_df['sub_pathway'] == s_path)
                                                            & (onto_df['sub_sub_pathway'] == s_s_path)
                                                            & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)
                                                            & (onto_df['sub_sub_sub_sub_pathway'] == s_s_s_s_path)]['gene_name'])

                        for s_s_s_s_s_path in sub_sub_sub_sub_sub_pathways:
                            onto_graph_pathways[path][s_path][s_s_path][s_s_s_path][s_s_s_s_path][s_s_s_s_s_path] = \
                                list(onto_df.loc[(onto_df['pathway'] == path)
                                            & (onto_df['sub_pathway'] == s_path)
                                            & (onto_df['sub_sub_pathway'] == s_s_path)
                                            & (onto_df['sub_sub_sub_pathway'] == s_s_s_path)
                                            & (onto_df['sub_sub_sub_sub_pathway'] == s_s_s_s_path )
                                            & (onto_df['sub_sub_sub_sub_sub_pathway'] == s_s_s_s_s_path)]['gene_name'])

                            gene_names[path + '_' + s_path + '_' + s_s_path + '_' + s_s_s_path + '_' + s_s_s_s_path + '_' + s_s_s_s_s_path] = \
                                onto_graph_pathways[path][s_path][s_s_path][s_s_s_path][s_s_s_s_path][s_s_s_s_s_path]

    from json import dumps
    return render(request, 'GlycoEnzDB.html', {'onto_graph_pathways': onto_graph_pathways,
                                               'onto_graph_functions': onto_graph_functions,
                                               'gene_names': dumps(gene_names)})

