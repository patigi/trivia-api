#!/bin/bash

dropdb trivia_test

createdb trivia_test

psql trivia_test < trivia.psql

python3 test_flaskr.py
