#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:8000 JOTA_test.wsgi