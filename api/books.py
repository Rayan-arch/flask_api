from psycopg2 import extras
from json import dumps, loads
from flask import Response,request, abort
from db import get_connection


def index():
    return 'index'

def add():
    return 'add'

def delete():
    return 'delete'