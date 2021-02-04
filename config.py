from os import environ
import psycopg2




# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

#Development
# from os.path import join, dirname
# from dotenv import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)
# DATABASE_URL = 'postgres+psycopg2://postgres:76541@localhost:5432/classes'
# conn = DATABASE_URL

#Production
DATABASE_URL = environ.get('DATABASE_URL')
conn = DATABASE_URL
