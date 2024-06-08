## Installation:

1. Download or clone this repository
2. Install Docker and verify the installation by following steps 1, 2 and 3 here: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
2. Install docker-compose:
'''
sudo apt install docker-compose
'''
3. In the Dockerfile file, change the WORKDIR (line number 4) to the location of the 'flask_mongodb_crud' folder

## Running the application:

1. Run the following command from within the 'flask_mongodb_crud' folder:
'''
sudo docker-compose up --build -V
'''
2. Download and run postman: https://www.postman.com/downloads/

## Running the test cases:
1. Comment line number 11 and uncomment line number 13, so that the code becomes:
'''
# CMD python application.py

CMD pytest testing.py -s
'''
2. Run the following command from within the 'flask_mongodb_crud' folder:
'''
sudo docker-compose up --build -V
'''