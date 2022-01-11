import connection
import time
from flask import request
from psycopg2 import sql


@connection.connection_handler
def get_questions(cursor, order="submission_time", direction="DESC"):
    query = sql.SQL("SELECT * FROM question ORDER BY {order} {direction}")
    cursor.execute(query.format(order=sql.Identifier(order), direction=sql.SQL(direction)))
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor, id):
    query = '''
        SELECT title, message, vote_number, view_number
        FROM question
        WHERE id = %(q)s
        '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_question_id(cursor, id):
    query = '''
            SELECT message, vote_number
            FROM answer
            WHERE question_id = %(q)s
            '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


@connection.connection_handler
def get_question_headers(cursor):
    cursor.execute("Select * FROM question LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    return colnames


@connection.connection_handler
def get_applicant_ids(cursor):
    query = """
    SELECT MAX(id)+1
    FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_content(cursor,new_question_data):
    query = """
       INSERT INTO question
       VALUES (%(id)s,%(s_t)s,%(v_n)s,%(vo_nu)s,%(t_l)s,%(m_e)s);
    """
    cursor.execute(query, {'id': new_question_data[0], 's_t': new_question_data[1], 'v_n': new_question_data[2],
    'vo_nu': new_question_data[3], 't_l': new_question_data[4], 'm_e': new_question_data[5]})


def change_vote(filename, id, direction):
    for row in filename:
        if row["id"] == id and direction == "increase":
            row['vote_number'] = str(int(row['vote_number']) + 1)
        elif row["id"] == id and direction == "decrease":
            row['vote_number'] = str(int(row['vote_number']) - 1)
    return filename


def edit_question(old, new_title, new_message, id,):
    for row in old:
        if row["id"] == id:
            row["title"] = new_title
            row["message"] = new_message
            return old


def delete_content_by_id(content_id, content_type):
    if content_type == "question":
        file_path = connection.DATA_FILE_PATH_QUESTION
        header = connection.DATA_HEADER_QUESTION
    elif content_type == "answer":
        file_path = connection.DATA_FILE_PATH_ANSWER
        header = connection.DATA_HEADER_ANSWER
    old_data = get_selected_data(content_type)
    data = delete_by_id(old_data, content_id, "id")
    connection.write_data(file_path, data, header)
    return old_data


def change_vote_by_id(content_id, content_type, direction):
    if content_type == "question":
        file_path = connection.DATA_FILE_PATH_QUESTION
        header = connection.DATA_HEADER_QUESTION
    elif content_type == "answer":
        file_path = connection.DATA_FILE_PATH_ANSWER
        header = connection.DATA_HEADER_ANSWER
    old_data = get_selected_data(content_type)
    data = change_vote(old_data, content_id, direction)
    connection.write_data(file_path, data, header)
    return old_data


def give_pics(link, datas):
    datas = sort(datas)
    for data in datas:
        data["image"] = link
        return datas


def give_pics_by_id(question_id, image, datas):
    for data in datas:
        if data["id"] == question_id:
            data["image"] = image
            return datas


