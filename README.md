# webGlycoEnzDB
All GlycoEnzDB data files and code.
Contains a Django project which runs the web interface of the GLycoEnzDB.


### Web GlycoENZ DB Django Project

To run the Django Project:
1. Open PyCharm
2. Open Project -> select djangoProject folder 
3. Go to requirements.txt and install the dependancies
4. Make sure django support is enabled in preferences -> Languages and frameworks -> Django
5. The run button should have Django configrations setup if not select add django configration
6. Refer [https://www.youtube.com/watch?v=QAHNYLVq1cc]
7. To run it from the terminal use python manage.py runserver


Simpler way to take care of all the dependencies is to use Docker:
0. Install Docker
1. Go to the django project folder
2. Build the project using Docker command:
``` docker build -t web-glycoenzdb . ```
3. Run the project using Docker command (for development purpose):
``` docker run --rm -p 8000:8000 -v $(pwd):/app --add-host=host.docker.internal:host-gateway web-glycoenzdb ```
This will run on port 8000, if we want to change we can use any other port in the argument like-
``` docker run --rm -p <PORT>:8000 -v $(pwd):/app --add-host=host.docker.internal:host-gateway web-glycoenzdb ```

4. To run the server we can run the server in detached mode:
``` docker run --rm -p 8000:8000 -d --add-host=host.docker.internal:host-gateway web-glycoenzdb ```
This would output the containerid which can be used later to stop the server
5. To stop the server we can stop the container using the following command:
``` docker stop <continer_id> ```
if continer id is unknown, it can be found using the command `docker ps`

DB configrations can be changed in settings.py


### Loading Onto Data
There is a sub project in the web-glycoenzdb called dataloader which uses the GlyconEnzOnto data in the excel file to load the data into Database.

To Run just install the dependencies in the requirement.txt and run `python loadGlycoEnzOnto.py` or use the docker command in case of dependency or package not found issues  :
` docker build -t db-loader . ` and run `docker run --rm db-loader`.

Configrations can be changed in the python file.


Note: `use host.docker.internal` instead of `localhost` when running from docker.

## New Setup (No longer using docker)
0. Env exported using ```conda env export --from-history > glyco-env.yml```
1. Create a conda environment using :
```conda env create --name glyco-env --file conda-env/glyco-env.yml```
2. Activate the environment
```conda activate glyco-env```

### Database

1. install postgresql 12 (https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)
2. Create User root/password
3. Create database glycoenzdb (CREATE DATABASE glycoenzdb;)

### DataLoader
1. To load the ontology data from the excel file, go to the dataloader folder (```cd dataloader```) and run the following command:
    ``` python loadGlycoEnzOnto.py```
    Make sure to update the database details in the python file

### Django Web Application
1. update the database details in the settings.py file
2. if it is first time connecting to DB run:
    ```python manage.py makemigrations```
    ```python manage.py migrate```
3. ~~python manage.py createsuperuser (glucoAdmin/admin)~~
4. Start the server using the following command:
    ```python manage.py runserver 0.0.0.0:8000```
5. Also start the Single cell violin plot server using the following command
    ```python dash_trial_ind.py```
 



Change Log:
- April 16, 2023: 
    1. Removed _1 to _9 from the excel file / database so that the display name is correct
    2. Moved elongation pathways: Chondrotin/Dermatan….; Heparin…./ and Keratan sulfate elongation to be part of ‘Elongation” subclass rather than “Biosynthesis/core/GAG_1” subclass.