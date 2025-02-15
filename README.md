# JOTA test

Essa é uma implementação dos requisitos do teste

# Antes de rodar
É preciso criar os containers usando **docker-compose build** mas **docker-compose up** faz o build se não houver container criados ainda.

```bash
$ docker-compose up -d
$ docker-compose exec jotateste bash

# Cria as tabelas no banco e popula com Categorias e um usuário Administrator
appuser@123$ ./manage.py migrate
appuser@123$ ./manage.py loaddata --app news news/default_categories.json
appuser@123$ ./manage.py loaddata --app main main/default_user.json

# para os containers
$ docker-compose stop
```

# Como rodar

```bash
$ docker-compose up
```

Em um nevegador digite http://localhost:8000

A senha do usuário _admin_ é _zyZtxqFVGgRfDdrSknQp_
