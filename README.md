# ZANIA - FastAPI Application
I used Python FastAPI and Postgresql to build my app. I used sqlalchemy for data modeling and as ORM. I used Postgres because you guys wanted a production grade app. I couldn't find any free postgresql server online So I ran postgres on docker container locally. And shipped it like that, i.e. there will be two containers running. One postgres and other is the  FastAPI app. I used docker-compose to manage both containers.
### Requirements for testing and running
- Docker
- Docker-Compose
- python3.8
- pytest (pip install pytest)
- requests (pip install requests)
### Run tests

1. #### Run unit tests:
    1. Make sure in **docker-compose.yml** file, **dockerfile** field is set to **Dockerfile.test**
    2. Make sure in **docker-compose.yml** file **POSTGRES_DB** field is set to  **test**.
    3. Make sure in **Dockerfile.test** file CMD["pytest"] is uncommented and CMD["python","main.py"] is commented.
    4. All of the above should be there by default at first.
    5. Initially you don't need to make any changes. Just Run :
        ```bash
        docker-compose up
        ```
        or

        ```bash
        docker compose up
        ```
    6. Now you can check the output of pytest on your console.
    7. Unit test code is in the /app/test directory.
    8. After checking run:
        ```bash
        docker-compose down
        ```
        or
        ```bash
        docker compose down
        ```
2. #### Run intigration tests:
    1. Every thing same as unit test except point  **3**. Now just uncomment the CMD["python","main.py"] and comment the CMD["pytest"] in  *Dockerfile.test*
    2. Remove previously created image **zania_app**. don't remove the postgres image just the fastapi app.
    3. Now run:
        ```bash
        docker-compose up
        ```
        or

        ```bash
        docker compose up
        ```
        Now our Server is running on port 8000. you can go to **http://localhost:8000/docs** in your browser and see all the apis 

    4. Now go inside the **intigration_tests** directory and run **pytest** in your host machine. you need pytest and requests downloaded. Remember run it in your host machine.
        ```bash
        pip install pytest requests
        cd intigration_tests
        pytest
        ```
    5. Now after running pre provided api tests. you can go to **http://localhost:8000/docs** to play around with the api and test it more.
    6. **PS** : While running the application don't run the unit tests.
    Run the unit test before or after runing the intigration tests. because running unit tests will clear the test database.Thus intigration tests or further databas query via api endpoints will crash the program.

    6. After this same clean up as before.
        ```bash
        docker-compose down
        ```
        or
        ```bash
        docker compose down
        ```
    
### Deployment
1. For deployment go to docker-compose.yml and change dockerfilename to **Dockerfile.prod** and PG_DATABASE to **prod**. and run:

    ```bash
    docker-compose up
    ```
We can Nginx (as a reverse proxy or as a load balancer) and Gunicorn (as web server) for efficient deployment.



