# Project Configurations and Documentions

## GlycoEnzDB

Load the glyco gene data into the posgress DB:

1. Install postgresql version 12.x
2. create user with USER = "postgres" & PASSWORD = "847468"
3. Create database named "glycoenzdb"
4. Update loadGlycoEnzOnto.py with db details if required.
5. Run `python dataloader/loadGlycoEnzOnto.py`

To run the Django Project:

1. git clone git@github.com:neel-lab/webGlycoEnzDB.git or download the repo from github.
2. Create new conda environment, install required packages and activate:
   conda create -y --name glyco_env
   conda install -f -y -q --name glyco_env -c conda-forge --file djangoProject/requirements.txt
   conda activate glyco_env
3. The glycoenz DB is in the /djangoProject directory.
4. cd djangoProject/
5. Run the django server - python manage.py runserver
6. Database connection details can be changed from djangoProject/settings.py

GPT text - file: djangproject/data/gpt/{gene name}.txt
Reaction images - file: djangoproject/webGlycoEnzDB/static/reaction_imgs/{gene name}.png
MI data (for top 10 TFs table ) - data/mi_results.txt
Pathway images in gene details pages are configured in the gene_figure_mapping.py file, variable `PATHWAY_GENE_MAPPING`. It links the slide number and the list of genes.

Pathways and Genes:
Default Pathway image - djangoproject/webGlycoEnzDB/static/pathway*map with map
pathway_image and genes mapping - file:data/pathway_map.json - {key: "pathway tree seperated by '*' ", value: "gene names seperated by comma"}

Server Steps:
static file changes: [TODO]

dataloader for ontology - to edit in future

## CCLE Violin Plots

## geneNetGlyco

systemctl [TODO]
