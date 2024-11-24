# Project Configurations and Documentions

## GlycoEnzDB

Install postgresDB and setup "glycoenzdb":

1. Install postgresql version 12.x
2. create user with USER = "postgres" & PASSWORD = "847468"
3. Create database named "glycoenzdb"
   [Open pgAdmin-->Open Servers-->PostgreSQL 12-->right-click Databases--> create "Database..."--> name it "glycoenzdb"]
4. In pg_hba.conf (located in ~/PostgreSQL\17\data) you may need to add a line:
   host all all 0.0.0.0/0 md5
5. In postgresql.cong ensure that there is a line:
   listen_addresses = '\*'
6. To check if postgre is running:
   Press Win + R, type services.msc, and press Enter. Right-click to start if necessary

Download webGlycoEnzDB:

1. Open GitHUB desktop and clone: http://github.com/neel-lab/webGlycoEnzDB
2. Open repository in pyCharm professional directly from GitHUB desktop
3. File is stored in C:\Users\...\Documents\Github\webGlycoEnzDB

Setup PyCharm for Django server [https://www.youtube.com/watch?v=QAHNYLVq1cc]:

1. - Add New Interpreter using the bottom-right widget
   - Make new .venv in this webGlycoEnzDB folder <OK>
   - Install requirements.txt in /djangoProject folder using terminal command: "pip install -r .\requirements.txt"
2. Open settings. --> Language & Frameworks --> Enable Django Support
   - Specify Django project root direction
   - Specify location of settings.py in djangoProject/djangoProject/
   - Specify location of mange.py in djangoProject/
   - Folder pattern to track files: "migrations"
3. settings--> Language & Frameworks --> Template Languages --> select Django, html
4. Go to Tools --> Manage.py--> type "migrate". This will create a db.sqlite3 file
5. In manage.py window type: "createsuperuser". Give username and password
6. Go to Run --> Edit Configurations --> Under django server specify port localhost:8000
7. Update loadGlycoEnzOnto.py with db details if required.
8. Update settings.py with port number:
   DATABASES = {
   'default': {
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': 'glycoenzdb',
   'USER': 'postgres',
   'PASSWORD': '847468',
   'HOST': 'localhost',
   'PORT': '5432',
   }
   }
9. Run `python dataloader/loadGlycoEnzOnto.py`

Run Django Project:

1. Database connection details can be changed from djangoProject/settings.py
2. To start server, at terminal type: "python manage.py runserver localhost:8000" or better goto "run..." and execute
3. Click on http://localhost:8000/
4. There are two things here:
   To open entire glycoenzdb go to: http://localhost:8000/glycoenzdb/
   To open admin go to: http://localhost:8000/admin/
   To run the Django Project:
5. git clone git@github.com:neel-lab/webGlycoEnzDB.git or download the repo from github.
6. Create new conda environment, install required packages and activate:
   conda create -y --name glyco_env
   conda install -f -y -q --name glyco_env -c conda-forge --file djangoProject/requirements.txt
   conda activate glyco_env
7. The glycoenz DB is in the /djangoProject directory.
8. cd djangoProject/
9. Run the django server - python manage.py runserver
10. Database connection details can be changed from djangoProject/settings.py

<b>Data source:</b><br />
GPT text - file: djangproject/data/gpt/{gene name}.txt<br />
Reaction images - file: djangoproject/webGlycoEnzDB/static/reaction_imgs/{gene name}.png<br />
MI data (for top 10 TFs table ) - data/mi_results.txt<br />
Edit pathway html links - djangoproject/webGlycoEnzDB/static/pathway_figures <br />
Pathway images in gene details pages are configured in the webGlycoEnzDB/gene_figure_mapping.py file, variable `PATHWAY_GENE_MAPPING`. It links the slide number and the list of genes. Also make imilar changes in the config.js file.
pathway_image and genes mapping - file:data/pathway_map.json - {key: "pathway tree seperated by '\*' ", value: "gene names seperated by comma"}
