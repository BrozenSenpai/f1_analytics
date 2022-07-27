#!/bin/bash
sleep 70
gunicorn --config ./gunicorn_config.py index:server