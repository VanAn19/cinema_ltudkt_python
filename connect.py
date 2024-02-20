import pyodbc

server = 'LAPTOP-747FVP6Q\SQLEXPRESS'
database = 'Cinema_N07'
username = 'sa'
password = '123456'

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=LAPTOP-747FVP6Q\SQLEXPRESS;'
                      'Database=Cinema_N07;'
                      'UID=sa;'
                      'PWD=123456;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()