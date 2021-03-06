## A Very Simple REST API.

### Overview

This minimal REST API stores `person` records. Each `person` is uniquely
identifiable by their associated `person_id` (UUID) and `version`. Once
a unique `person` is created, updates to the `person`'s attributes
result in the creation of a new record with the same `person_id`, but
with a new `version` attribute. Only the most current `version` of a
`person` can be updated. When a `person` is updated, the API enforces
that there are changes compared to the current `version`. It does not,
however, verify that the new `version` is unique across all versions for
the associated `person_id`. The most current `version` of a `person` can
be deleted.

Bulk queries are not supported at this time.

This project was built using __Python3.8__, the
[__FastAPI__](https://fastapi.tiangolo.com/) framework, and
__PostgreSQL__, all running stress-free in __Docker__.

__Why FastAPI?__ There's been
[a lot](https://talkpython.fm/episodes/show/284/modern-and-fast-apis-with-fastapi)
[of talk](https://pythonbytes.fm/episodes/show/192/calculations-by-hand-but-in-the-compter-with-handcalcs)
about this framework and I've been eager to test drive it. It did not
disappoint. It has superior async support--there's absolutely no need
to think about event loops. FastAPI uses mandatory data validation via
[pydantic](https://pydantic-docs.helpmanual.io/), which provides smooth
error handling and enables very nice auto-generated documentation.
Recommend. 10/10. Would use again.
___

### Run

These instructions assume the host is running MacOS or Linux and
[Docker](https://www.docker.com/) is installed.

__To run__,
* clone repo
* cd into project root, then...

```bash
$ docker-compose up -d --build
```

Test the service is running by navigating to
[http://localhost:8002/docs](http://localhost:8002/docs).

To run the __unit tests__...

```bash
$ tox --
```
___

#### Authentication and Credentials

There is currently no authentication. The PostgreSQL credentials are
hard-coded where needed (and checked into version control). This is
deliberate, as this is only a POC. If this were going to be used in
production, credentials never would have been checked into version
control.

__Remove the hardcoded DB credentials and change the login and password
prior to public use.__
___

#### API Documentation

When the service is running, __detailed Swagger/OpenAPI documentation
can be found at the `/docs` endpoint__.
[check it out here](http://localhost:8002/docs). Or the ReDoc version
[here](http://localhost:8002/redoc).

__Overview of Available REST Endpoints:__

| ENDPOINT | ACTION | REQ. PARAM | OPTIONAL PARAMS | BODY REQUIRED |
|---       |---     |---         | ---             | ---           |
| /person/ | POST   | None       | None            | Yes           |
| /person/ | GET    | person_id  | version         | No            |
| /person/ | PUT    | person_id  | None            | Yes           |
| /person/ | DELETE | person_id  | None            | No            |
| /persons/| GET    | None       | None            | No            |

__Sample curls:__

POST /person/
```bash
$ curl -X POST "http://localhost:8002/person/" -H  "accept: application/json" -H  "Content-Type: application/json" -d '{"first_name":"guido","last_name":"van rossum","email":"guidovr@python.com","age":64}' -i
```

GET /person/{person_id}
```bash
$ curl -X GET "http://localhost:8002/person/843651c0-4e05-4960-a274-95578912bfe1" -H "accept: application/json" -i
```

PUT /person/
```bash
$ curl -X PUT "http://localhost:8002/person/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{'person_id':'843651c0-4e05-4960-a274-95578912bfe1','email':'guidovr@python3.com'}" -i
```

DELETE /person/{person_id}
```bash
curl -X DELETE "http://localhost:8002/person/843651c0-4e05-4960-a274-95578912bfe1" -H  "accept: application/json" -i
```

GET /persons/
```bash
$ curl -X GET "http://localhost:8002/persons/" -H "accept: application/json" -i
```

[The project's Swagger Documentation](http://localhost:8002/docs)
contains sample request and response objects, as well as the ability to
interactively test the API.

__A note on mandatory trailing `/`'s in requests__. In an effort to keep
the swagger clean since this is just a POC, I chose not to go with
either of the two inelegant options
[discussed here](https://github.com/tiangolo/fastapi/issues/1127).
TL;DR: changes to a FastAPI dependency broke standard regex in routes.
___

### Considerations
* __DB Transactions__. Currently no DB queries are transactional/atomic.
The downside to this is obvious. In addition to increasing data
integrity, using transactional, atomic queries would reduce the
complexity of the handler code.
* __Relational vs Non-Relational__. Lots of thoughts here.
* __Delete returns success even if no target record was found__. There
are varying opinions on this behavior. From a security standpoint it
could be considered a feature, from a usability standpoint it could be
viewed as a bug.
___

### Future Features

* __Cache__. Caching the latest version of each person with some TTL
will reduce the need for the most common DB query.
* __Testing__. This needs integration tests. And more unit tests!!
* __Logging__
___

### Code Convention and Style

This project mostly conforms to the standards in
[PEP-8](https://www.python.org/dev/peps/pep-0008/). Max line length is
extended to 88 characters, which is
[Black's](https://pypi.org/project/black/) default line-length.
