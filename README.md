# SPM Project - LJPS System

## Project Description
Personal learning journey tracker for staff to plan their own learning journey, based on their learning goals, facilitating the progression of their career within the organization while taking their preferred and optimal combination of courses.

## Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
    - Has support for Windows and MacOS
- Clone this repo:
~~~
$ git clone git@github.com:gjegoh/SPM_Official.git
$ cd SPM_Official
~~~

## Steps to Running the Project
- If running the project for the first time, build and start the container:
~~~
$ docker-compose up --build
~~~
- If container is already built:
~~~
$ docker-compose up
~~~
- If trying to wipe the local database:
~~~
$ docker-compose down --volumes
~~~

## How to use the Project
- To login as a user:
    - Username: learner1
    - Password: learner1
- To login as a admin:
    - Username: admin
    - Password: admin
    
# Credits
- Group 4:
    - Goh Jia En
    - Phoenikelly Yong
    - Celine Ng
    - Euodia Tan
    - Wong Ju Da
