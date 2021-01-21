from os import environ
import psycopg2

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

# DATABASE_URI = 'postgres+psycopg2://postgres:76541@localhost:5432/classes'
DATABASE_URL = environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
