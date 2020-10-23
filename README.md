## A Very Simple REST API.

### Overview

This simple API was built with Python3.8, the 
[FastAPI framework](https://fastapi.tiangolo.com/), and PostgreSQL, all
running stress-free in Docker.

Why FastAPI? I've heard a lot of talk about this framework and have been
eager to test drive it for a while. It did not disappoint. It has the
best async support of any python library I've ever used--absolutely no
need to think about event loops. The required data validation provides
really smooth error handling and enables very nice auto-generated
documentation. Recommend. 10/10. Would use again.
___

### Run

These instructions assume the host is running MacOS or Linux and Docker 
is installed.

To run,
* Clone repo
* cd into project root, then...

```bash
$ docker-compose up -d --build
```

Test the service is running by navigating to 
[http://localhost:8002/docs](http://localhost:8002/docs).
___

#### Authentication and Credentials

There is currently no authentication. The PostgreSQL credentials are 
hard-coded where needed (and checked into version control). This is
deliberate, as this is only a POC. If this were going to be used in 
production, credentials never would have been checked into version
control.
___

#### API Documentation

When the service is running, __detailed Swagger/OpenAPI documentation
can be found at the `/docs` endpoint__. Please 
[check it out here](http://localhost:8002/docs).

Overview of Available REST Endpoints:

| ENDPOINT | ACTION | REQ. PARAM | OPTIONAL PARAMS | BODY REQUIRED |
|---       |---     |---         | ---             | ---           |
| /person/ | POST   | None       | None            | Yes           |
| /person/ | GET    | person_id  | version         | No            |
| /person/ | PUT    | person_id  | None            | Yes           |
| /person/ | DELETE | person_id  | None            | No            |
| /persons/| GET    | None       | None            | No            |

[The project's Swagger Documentation](http://localhost:8002/docs) 
contains sample request and response objects, as well as the ability to
interactively test the API.
___

### Future Features

* Cache. Caching the latest version of each person with some TTL will  
reduce the need for the most common DB query.
* Testing. This needs integration tests. And more unit tests.
* Logging
___

### Code Convention and Style

This project mostly conforms to PEP-8's style guide. Max line length is 
extended to 88 characters, which is 
[Black's](https://pypi.org/project/black/) default line-length.
