#!/bin/bash
gunicorn --config ./gunicorn_config.py server:app