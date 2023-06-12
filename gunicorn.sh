#!/bin/sh
gunicorn --chdir server app:app -w 2 --threads 2 -b 0.0.0.0:80