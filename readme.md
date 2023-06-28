test
pip freeze > requirements.txt


## [Migrations Step](https://medium.com/@acer1832a/%E4%BD%BF%E7%94%A8-alembic-%E4%BE%86%E9%80%B2%E8%A1%8C%E8%B3%87%E6%96%99%E5%BA%AB%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86-32d949f7f2c6)
### init env
1. create folder and build basic files
```
alembic init migrations 
```

2. modify config  
- open alembic.ini file
- modify sqlalchemy.url
```
alembic revision -m "migrate init"
```
- then there are history file in migrations/versions
***
### Migrate 
- open  migrations/env.py
- for example model class name = User
- import User
- modify "target_metadata" ex:[User.metadata]

```
alembic revision --autogenerate -m "commit"
```
- then, need to check history file, because that's will not currentful 

```
alembic upgrade head
```
***
## Other command

- upgrade version
```
alembic upgrade +1
```

- downgrade version
```
alembic downgrade -1
```



