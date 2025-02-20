# JOTA test
[![test_Django](https://github.com/dlemos/JOTA_test/actions/workflows/main.yml/badge.svg)](https://github.com/dlemos/JOTA_test/actions/workflows/main.yml)

Essa é uma implementação dos requisitos do teste

# Antes de rodar
É preciso criar os containers usando **docker-compose build** mas **docker-compose up** faz o build se não houver container criados ainda.

```bash
$ docker-compose up -d
$ docker-compose exec jotateste bash

# Cria as tabelas no banco e popula com Categorias e um usuário Administrator
appuser@123$ ./manage.py migrate
appuser@123$ ./manage.py loaddata --app news news/default_categories.json
appuser@123$ ./manage.py loaddata --app news news/default_groups.json
appuser@123$ ./manage.py loaddata --app main main/default_user.json

# para os containers
$ docker-compose stop
```

## Como rodar

```bash
$ docker-compose up
```

Em um nevegador digite http://localhost:8000

A senha do usuário _admin_ é _zyZtxqFVGgRfDdrSknQp_

## Como gerar o schema da API interagir usando o Swagger-UI

```bash
# Gere o arquivo schema.yml usando o commando spectacular
$ ./manage.py spectacular --color --file schema.yml
# Suba um container a vulso
$ docker run -p 8080:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/schema.yml:/schema.yml swaggerapi/swagger-ui
```

Com a aplicação rodando abra a URL no navegador http://localhost:8080

https://github.com/tfranzel/drf-spectacular?tab=readme-ov-file#take-it-for-a-spin

## Documentação dos componentes utilizados
- Django https://docs.djangoproject.com/en/5.1/
- Django REST Framework https://www.django-rest-framework.org/
- Simple JWT https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
- Celery https://docs.celeryq.dev/en/stable/index.html
- django-environ https://django-environ.readthedocs.io/en/latest/index.html
- drf-spectacular https://drf-spectacular.readthedocs.io/en/latest/
- pytest https://docs.pytest.org/en/stable/
- pytest-django https://pytest-django.readthedocs.io/en/latest/
- freezegun https://github.com/spulec/freezegun
- factory_boy https://factoryboy.readthedocs.io/en/stable/