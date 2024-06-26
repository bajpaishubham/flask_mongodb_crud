## A. Installation:

1. Download or clone this repository
2. Install Docker and verify the installation by following steps 1, 2 and 3 [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
3. Install docker-compose:
```
sudo apt install docker-compose
```
4. In the Dockerfile file, change the WORKDIR (line number 4) to the location of the `flask_mongodb_crud` folder

## B. Running the application:

1. Run the following command from within the `flask_mongodb_crud` folder:
```
sudo docker-compose up --build -V
```
2. Download and run [postman](https://www.postman.com/downloads/)

## C. Running the test cases:
1. Comment line number 11 and uncomment line number 13, so that the code becomes:
```
# CMD python application.py

CMD pytest testing.py -s
```
2. Run the following command from within the `flask_mongodb_crud` folder:
```
sudo docker-compose up --build -V
```

## D. Examples of how to interact with the API:
### D1. Welcome endpoint:
Method: `GET`   
Route: `/`   
Description: Provides welcome message on the default url

#### Example Request:
Method: `GET`   
Route: `/`

#### Example Response:
```
{
"Hello User": "Welcome to the application for CRUD operations on a JSON database"
}
```

### D2. Document creation endpoint:

Method: `POST`   
Route: `/data`   
Description: Accepts a JSON object and stores it in the database

#### Example Request:

Method: `POST`   
Route: `/data`   
Body:
```
{
"name": "John",
"age": 30,
"city": "New York"
}
```

#### Example Response:
```
{
"id": "60c72b2f4f1a2c1a4c8b4567"
}
```

### D3. Document retrieval endpoint:
Method: `GET`   
Route: `/data/{id}`   
Description: Retrieves the JSON object associated with the given ID from the database

#### Example Request:
Method: `GET`   
Route: `/data/60c72b2f4f1a2c1a4c8b4567`

#### Example Response:
```
{
"_id": "60c72b2f4f1a2c1a4c8b4567",
"name": "John",
"age": 30,
"city": "New York"
}
```

### D4. Document update endpoint:
Method: `PUT`   
Route: `/data/{id}`   
Description: Updates the existing JSON object with the given ID in the database

#### Example Request:
Method: `PUT`   
Route: `/data/60c72b2f4f1a2c1a4c8b4567`   
Body:
```
{
"name": "Jane",
"age": 25,
"city": "Los Angeles"
}
```

#### Example Response:
```
{
"message": "Data updated successfully"
}
```

### D5. Document delete endpoint:
Method: `DELETE`   
Route: `/data/{id}`   
Description: Deletes the JSON object with the given ID from the database

#### Example Request:
Method: `DELETE`   
Route: `/data/60c72b2f4f1a2c1a4c8b4567`

#### Example Response:
```
{
"message": "Data deleted successfully"
}
```

## E. File Descriptions:
1. `Demonstration.webm`: Demonstration video
2. `demonstration_steps.txt`: Contains the steps followed during the demonstration and the JSON used
3. `application.py`: Contains the main Flask application
4. `testing.py`: Contains the unit test cases
5. `Dockerfile`: Dockerfile for the main application
6. `docker-compose.yml`: Contains the settings for this multi-container Docker application
7. `requirements.txt`: Contains the python packages needed to be installed for running the application within the container
8. `TASKS.md`: Contains the tasks for the assignment
9. `README.md`: Contains the description of the whole project
