# # db.py
# import os
# import pymysql
# from dotenv import load_dotenv
# from pymysql.cursors import DictCursor

# load_dotenv()

# POOL = None


# def query(sql, params=None):
#     conn = get_conn()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(sql, params or ())
#             return cur.fetchall()
#     finally:
#         conn.close()

# from app.config import MYSQL_CONFIG

# def get_conn():
#     return pymysql.connect(
#         host=MYSQL_CONFIG["host"],
#         user=MYSQL_CONFIG["user"],
#         password=MYSQL_CONFIG["password"],
#         database=MYSQL_CONFIG["database"],
#         cursorclass=pymysql.cursors.DictCursor
#     )

# def query_one(sql, params=None):
#     conn = get_conn()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(sql, params)
#             return cur.fetchone()
#     finally:
#         conn.close()

# def query_all(sql, params=None):
#     conn = get_conn()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(sql, params)
#             return cur.fetchall()
#     finally:
#         conn.close()

# def execute(sql, params=None):
#     conn = get_conn()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(sql, params)
#             conn.commit()
#             return cur.lastrowid
#     finally:
#         conn.close()
        
# def insert_one(query, params=None):
#     """Insert one row and return the inserted ID."""
#     conn = get_conn()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(query, params)
#             conn.commit()
#             return cur.lastrowid
#     except Exception as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()        

import pymysql
from app.config import MYSQL_CONFIG

def get_conn():
    return pymysql.connect(**MYSQL_CONFIG)

def query_one(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()
    finally:
        conn.close()

def query_all(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def execute(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()

def insert_one(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
