# Testing

## Coverage Report:

docker-compose exec -T backend /bin/sh -c "pytest --cov=app app/tests"

## Setup

In order to not conflict with the actual main database, the tests are performed within an in-memory async sqlite
database.
The database path for this database is defined in `config.py` and can be reached with `settings.TEST_DATABASE_URI_ASYNC`
.

During the test case, the database for the main application is set in `session.py` depending on the the
variable `settings.TESTING`.
This variable is set to True while performing the pytest with the package `pytest-env` in the `pytest.ini` file.

It was crucial to have **all** database connections changed during the pytest since otherwise multiple database
connections might exist next to each other.
Prior tests where the database is fully defined in `conftest.py` and injected into the test setup via a dependency
override ended up in some database accesses of the main database from the test setup.
I haven't found out why this is the case but apparently the dependency override does not work as I expected it to do.

## Updates of models in tests

All update tests are currently performed by dictionaries and not by the usually used UpdateModel.
The issue is that otherwise all unset parameters are delivered as None and not ommitted since SQLModel does not detect
the unset values outside of FastAPI yet.
https://github.com/tiangolo/sqlmodel/issues/87
I have no clue why this issue is not apparent in the actual software and only in the tests.