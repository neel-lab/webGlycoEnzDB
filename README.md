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

