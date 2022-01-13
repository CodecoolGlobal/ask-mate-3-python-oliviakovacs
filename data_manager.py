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
        SELECT title, message, vote_number, view_number, id
        FROM question
        WHERE id = %(q)s
        '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_question_id(cursor, id):
    query = '''
            SELECT *
            FROM answer
            WHERE question_id = %(q)s
            ORDER BY submission_time
            '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


@connection.connection_handler
def get_question_comment_by_question_id(cursor, id):
    query = '''
            SELECT id, message, submission_time
            FROM comment
            WHERE question_id = %(q)s
            '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


@connection.connection_handler
def get_answer_comment_by_question_id(cursor, id):
    query = '''
        SELECT answer_id,message ,submission_time
        FROM comment c
        WHERE c.answer_id = (SELECT a.id FROM answer a WHERE a.id = %(q_id)s)'''
    cursor.execute(query, {'q_id': id})
    return cursor.fetchall()


@connection.connection_handler
def get_question_headers(cursor):
    cursor.execute("Select * FROM question LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    return colnames


@connection.connection_handler
def get_answer_ids(cursor):
    query = """
        SELECT MAX(id)+1 as maximum
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_ids(cursor):
    query = """
    SELECT MAX(id)+1 as maximum
    FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_question(cursor, new_question_data):
    query = """
       INSERT INTO question
       VALUES (%(id)s,%(s_t)s,%(v_n)s,%(vo_nu)s,%(t_l)s,%(m_e)s,%(pic)s);
    """
    cursor.execute(query, {'id': new_question_data[0], 's_t': new_question_data[1], 'v_n': new_question_data[2],
    'vo_nu': new_question_data[3], 't_l': new_question_data[4], 'm_e': new_question_data[5],'pic': new_question_data[6]})


@connection.connection_handler
def add_new_answer(cursor, new_question_data):
    query = """
       INSERT INTO answer
       VALUES (%(id)s,%(s_t)s,%(v_n)s,%(q_i)s,%(m_a)s,%(pic)s);
    """
    cursor.execute(query, {'id': new_question_data[0], 's_t': new_question_data[1], 'v_n': new_question_data[2],
    'q_i': new_question_data[3], 'm_a': new_question_data[4],'pic': new_question_data[5]})


@connection.connection_handler
def add_new_comment_to_question(cursor, new_comment_data):
    query = """
    INSERT INTO comment (submission_time, question_id, message)
    VALUES (%(s_t)s, %(q_id)s, %(m_a)s)
    """
    cursor.execute(query, {'s_t': new_comment_data[0], 'q_id': new_comment_data[1], 'm_a': new_comment_data[2]})


@connection.connection_handler
def add_new_comment_to_answer(cursor, new_comment_data):
    query = """
    INSERT INTO comment (submission_time, answer_id, message)
    VALUES (%(s_t)s, %(a_id)s, %(m_a)s)
    """
    cursor.execute(query, {'s_t': new_comment_data[0], 'a_id': new_comment_data[1], 'm_a': new_comment_data[2]})

@connection.connection_handler
def delete_question_by_id(cursor, id):
    query = """
    DELETE
    FROM question
    WHERE id = %(q_id)s"""
    cursor.execute(query, {'q_id':id})


@connection.connection_handler
def delete_answer_by_question_id(cursor, id):
    query = """
       DELETE
       FROM answer
       WHERE question_id = %(q_id)s"""
    cursor.execute(query, {'q_id': id})


@connection.connection_handler
def delete_comment_by_question_id(cursor, id):
    query = """
       DELETE
       FROM comment
       WHERE question_id = %(q_id)s"""
    cursor.execute(query, {'q_id': id})


@connection.connection_handler
def delete_comment_by_answer_id(cursor, id):
    query = """
       DELETE
       FROM comment c 
       WHERE c.answer_id = (SELECT a.id FROM answer a WHERE a.id = %(q_id)s)"""
    cursor.execute(query, {'q_id': id})


@connection.connection_handler
def delete_answer_by_id(cursor, answer_id):
    query = """
           DELETE
           FROM answer
           WHERE id = %(q_id)s
           RETURNING question_id"""
    cursor.execute(query, {'q_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def change_vote_by_id(cursor, data):
    if data[2]:
        query = f"""
                UPDATE { data[0] }
                SET vote_number=vote_number+%(c_h)s
                WHERE {data[3]}=%(q_or_a_id)s;
                """
    cursor.execute(query, {'q_or_a_id': data[1], 'c_h': data[2]})


@connection.connection_handler
def get_question_id_by_answer(cursor, id):
    query= '''
        SELECT question_id
        FROM answer
        WHERE id=%(id)s;
         '''
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@connection.connection_handler
def edit_question(cursor, id, question_title, question_message, pic):
    query = """
    UPDATE question
    SET title = %(q_t)s, message = %(q_m)s, image = %(pic)s
    WHERE id = %(q_id)s
    """
    cursor.execute(query, {'q_id': id, 'q_t': question_title, 'q_m': question_message, 'pic': pic})


@connection.connection_handler
def edit_answer(cursor, id, answer_message, pic):
    query = """
        UPDATE answer
        SET message = %(a_m)s, image = %(pic)s
        WHERE id = %(a_id)s
        RETURNING question_id
        """
    cursor.execute(query, {'a_id': id, 'a_m': answer_message, 'pic': pic})
    return cursor.fetchone()


@connection.connection_handler
def get_answer_by_id(cursor, id):
    query = '''
        SELECT *
        FROM answer
        WHERE id = %(q)s
        '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()

@connection.connection_handler
def get_latest_questions(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY submission_time DESC LIMIT 5
    """
    cursor.execute(query)
    return cursor.fetchall()


