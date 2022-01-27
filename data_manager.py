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
        SELECT title, message, vote_number, view_number, id, user_id
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
            SELECT id, message, submission_time, edited_count, user_id
            FROM comment
            WHERE question_id = %(q)s
            '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


@connection.connection_handler
def get_answer_comment_by_question_id(cursor, id):
    query = '''
        SELECT *
        FROM comment c
        WHERE c.answer_id IN (SELECT a.id FROM answer a WHERE a.question_id = %(q_id)s)'''
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
       VALUES (%(id)s,%(s_t)s,%(v_n)s,%(vo_nu)s,%(t_l)s,%(m_e)s,%(pic)s, %(user_id)s);
    """
    cursor.execute(query, {'id': new_question_data[0], 's_t': new_question_data[1], 'v_n': new_question_data[2],
    'vo_nu': new_question_data[3], 't_l': new_question_data[4], 'm_e': new_question_data[5],'pic': new_question_data[6], 'user_id': new_question_data[7]})


@connection.connection_handler
def add_new_answer(cursor, new_question_data):
    query = """
       INSERT INTO answer
       VALUES (%(id)s,%(s_t)s,%(v_n)s,%(q_i)s,%(m_a)s,%(pic)s, %(user_id)s);
    """
    cursor.execute(query, {'id': new_question_data[0], 's_t': new_question_data[1], 'v_n': new_question_data[2],
    'q_i': new_question_data[3], 'm_a': new_question_data[4],'pic': new_question_data[5], 'user_id': new_question_data[6]})


@connection.connection_handler
def add_new_comment_to_question(cursor, new_comment_data):
    query = """
    INSERT INTO comment (submission_time, question_id, message, edited_count, user_id)
    VALUES (%(s_t)s, %(q_id)s, %(m_a)s, %(e_c)s, %(user_id)s)
    """
    cursor.execute(query, {'e_c': 0, 's_t': new_comment_data[0], 'q_id': new_comment_data[1], 'm_a': new_comment_data[2], 'user_id': new_comment_data[3]})


@connection.connection_handler
def add_new_comment_to_answer(cursor, new_comment_data):
    query = """
    INSERT INTO comment (submission_time, answer_id, message, edited_count, user_id)
    VALUES (%(s_t)s, %(a_id)s, %(m_a)s, %(e_c)s, %(user_id)s)
    """
    cursor.execute(query, {'e_c': 0, 's_t': new_comment_data[0], 'a_id': new_comment_data[1], 'm_a': new_comment_data[2], 'user_id': new_comment_data[3]})

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
def delete_question_by_id(cursor, id):
    query = """
       DELETE
       FROM question
       WHERE question.id = %(q_id)s """
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
def delete_comment_by_id(cursor, comment_id):
    query = """
        DELETE
        FROM comment
        WHERE id = %(c_id)s
        RETURNING question_id, answer_id"""
    cursor.execute(query, {'c_id': comment_id})
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


@connection.connection_handler
def make_new_tag(cursor, tag_title):
    query= '''
    INSERT INTO tag(name)
    VALUES(%(t_t)s) RETURNING id
    '''
    cursor.execute(query, {"t_t": tag_title})
    return cursor.fetchone()


@connection.connection_handler
def pairing_tag_with_question(cursor,data):
    query='''
    INSERT INTO question_tag
    VALUES (%(qid)s, %(tid)s)
    '''
    cursor.execute(query, {"qid": data[0], "tid": data[1]})


@connection.connection_handler
def tags_by_question_id(cursor, id):
    query="""
    SELECT *
    FROM tag
    JOIN question_tag qt on tag.id = qt.tag_id
    WHERE question_id = %(id)s
    ORDER BY name
    """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@connection.connection_handler
def select_tag_id_by_tag_name(cursor, t_name):
    query="""
    SELECT id
    FROM tag
    WHERE name = %(tag_name)s 
    """
    cursor.execute(query, {"tag_name": t_name})
    return cursor.fetchone()


@connection.connection_handler
def tag_in_question_or_not(cursor, t_id, q_id):
    query="""
    SELECT question_id
    FROM question_tag
    WHERE question_id = %(q_id)s and tag_id = %(t_id)s
    """
    cursor.execute(query, {"t_id": t_id, "q_id": q_id})
    return cursor.fetchone()


@connection.connection_handler
def all_tag(cursor):
    query='''
    SELECT name
    FROM tag
    ORDER BY name
    '''
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_tag_from_question(cursor, question_id, tag_id):
    query='''
    DELETE 
    FROM question_tag
    WHERE question_id = %(question_id)s and tag_id = %(tag_id)s
    '''
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


@connection.connection_handler
def get_content_by_search(cursor, search):
    query = """
    SELECT title, answer.message, question.id
    FROM question
    FULL JOIN answer
    ON question.id = answer.question_id
    WHERE answer.message LIKE %(s)s OR question.title LIKE %(s)s
    ORDER BY question.id
    """
    cursor.execute(query, {"s": f"%{search}%"})
    return cursor.fetchall()


@connection.connection_handler
def edit_comment(cursor, id, comment_message, now):
    query = """
        UPDATE comment
        SET message = %(c_m)s, submission_time = %(c_now)s, edited_count = edited_count + 1
        WHERE id = %(c_id)s
        RETURNING question_id, answer_id
        """
    cursor.execute(query, {'c_id': id, 'c_m': comment_message, 'c_now': now})
    return cursor.fetchone()


@connection.connection_handler
def get_comment_by_id(cursor, id):
    query = """
       SELECT message 
       FROM comment
       WHERE id = %(c_id)s
       """
    cursor.execute(query, {'c_id': id})
    return cursor.fetchall()


@connection.connection_handler
def reputation_minus_two(cursor, id):
    query = """
    UPDATE "user"
    SET reputation = reputation -2
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@connection.connection_handler
def add_user(cursor, username, password, now):
    query = """
           INSERT INTO "user" (name, user_password, registration_date, reputation)
           VALUES (%(name)s, %(password)s, %(reg_date)s, %(rep_num)s);
        """
    cursor.execute(query, {'name': username, 'password': password, 'reg_date': now, 'rep_num': 0})


@connection.connection_handler
def get_user_id_by_name(cursor,username):
    query = '''
    SELECT id
    FROM "user"
    WHERE name = %(user_name)s
    '''
    cursor.execute(query, {'user_name': username})
    return cursor.fetchone()


@connection.connection_handler
def get_username_by_id(cursor, id):
    query = '''
    SELECT name
    FROM "user"
    WHERE id = %(id)s;
    '''
    cursor.execute(query, {"id": id})
    return cursor.fetchone()


@connection.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    query = '''
    SELECT user_id
    FROM question
    WHERE id = %(question_id)s
    '''
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@connection.connection_handler
def get_user_id_by_answer_id(cursor, answer_id):
    query = '''
        SELECT user_id
        FROM answer
        WHERE id =  CAST(%(answer_id)s AS int)
        '''
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def accepted_answer(cursor, answer_id,true_or_false):
    query = '''
    UPDATE answer
    SET accepted = CAST(%(true_or_false)s AS bit)
    WHERE answer.id = %(answer_id)s;
    '''
    cursor.execute(query, {'answer_id': answer_id, 'true_or_false': true_or_false})


@connection.connection_handler
def plus_15(cursor, user_id):
    query = '''
       UPDATE "user"
       SET reputation = reputation +15
       WHERE id = %(user_id)s
       '''
    cursor.execute(query, {'user_id': user_id})


@connection.connection_handler
def minus_15(cursor, user_id):
    query = '''
       UPDATE "user"
       SET reputation = reputation -15
       WHERE id = %(user_id)s
       '''
    cursor.execute(query, {'user_id': user_id})


@connection.connection_handler
def change_reputation_up(cursor, received_id, num):
    query = f"""
        UPDATE "user"
        SET reputation = reputation+%(num)s
        WHERE id= %(received_id)s;
        """
    cursor.execute(query, {"received_id": received_id, "num": num})


@connection.connection_handler
def get_user_names(cursor):
    query = """
    SELECT name, user_password
    FROM "user"
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_user_id_by_username(cursor, username):
    query = """
    SELECT id
    FROM "user"
    WHERE name =%(username)s"""
    cursor.execute(query, {'username': username })
    return cursor.fetchone()


@connection.connection_handler
def get_user_list(cursor):
    query = """
        SELECT u.id AS id, u.name AS name, u.registration_date AS registration_date, COUNT(a) AS answer_number, COUNT(c) AS comment_number, COUNT(q) AS question_number, reputation
        FROM "user" u
        LEFT JOIN question q ON u.id = q.id
        LEFT JOIN answer a ON u.id = a.user_id
        LEFT JOIN comment c ON u.id = c.user_id
        GROUP BY u.id, u.name, u.registration_date, u.reputation
        ORDER BY u.id"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tags(cursor):
    query = """
        SELECT tag.name, COUNT(question_tag.tag_id) as number_of_questions
        FROM tag
        LEFT JOIN question_tag
        ON tag.id = question_tag.tag_id
        GROUP BY tag.name
        ORDER BY number_of_questions DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_questions_by_user_id(cursor, user_id):
    query = """
        SELECT title, id
        FROM question
        WHERE user_id = %(user_id)s
        ORDER BY submission_time
    """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_user_id(cursor, user_id):
    query = """
            SELECT message, question_id
            FROM answer
            WHERE user_id = %(user_id)s
            ORDER BY submission_time
        """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_user_id(cursor, user_id):
    query = """
            SELECT message, question_id, answer_id
            FROM comment
            WHERE user_id = %(user_id)s
            ORDER BY submission_time
        """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


def get_users(cursor, username):
    query = """
        SELECT EXISTS(SELECT name AS exists FROM "user" WHERE name = %(username)s)
    """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()



