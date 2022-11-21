# CRUD Query Design

Relationship Queries don't work like they are described in the FastAPI Documentation.
This is a open issue for async and can currently be tackled by explicit relationship queries.

https://github.com/tiangolo/sqlmodel/issues/37

https://github.com/tiangolo/sqlmodel/issues/74

Furthermore SQLAlchemy Version 1.4.35 breaks the relationships as defined in sqlmodel and is therefor set to Version
1.4.34 in the requirements.txt.

https://github.com/tiangolo/sqlmodel/issues/315