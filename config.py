from os import environ
import psycopg2

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

# DATABASE_URI = 'postgres+psycopg2://postgres:76541@localhost:5432/classes'
DATABASE_URI = environ.get('DATABASE_URI')

conn = psycopg2.connect(DATABASE_URI, sslmode='require')
