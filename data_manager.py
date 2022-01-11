import connection
import time
from flask import request

@connection.connection_handler
def get_questions(cursor):
    query = '''
    SELECT *
    FROM question
    ORDER BY submission_time;
    '''
    cursor.execute(query)
    return cursor.fetchall()

#
# def get_question_by_id(id, option):
#     questions = get_selected_data(option)
#     for question in questions:
#         if question["id"] == id:
#             return question

@connection.connection_handler
def get_question_by_id(cursor, id):
    query = '''
        SELECT title, message, vote_number, view_number
        FROM question
        WHERE id = %(q)s
        '''
    cursor.execute(query, {'q': id})
    return cursor.fetchall()


def get_selected_data(choice):
    if choice == "question":
        data = connection.get_data(connection.DATA_FILE_PATH_QUESTION)
    elif choice == "answer":
        data = connection.get_data(connection.DATA_FILE_PATH_ANSWER)
    return data


def sort(data, type="submission_time", order="descending"):
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[j][type].isnumeric() and float(data[j][type]) > float(data[j+1][type]):
                data[j], data[j+1] = data[j+1], data[j]
            elif data[j][type] > data[j+1][type]:
                data[j], data[j+1] = data[j+1], data[j]
    if order == "descending":
        return data[::-1]
    return data




def get_answers_by_question_id(question_id, option):
    answers = get_selected_data(option)
    question_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            question_answers.append(answer)
    return question_answers


def create_new_data(headers, file):
    file_list = connection.get_data(file)
    ids = [0]
    for file in file_list:
        ids.append(int(file["id"]))
    new_data = {}
    for header in headers:
        if header == "id":
            new_data.update({"id": max(ids) + 1})
        if header == "submission_time":
            new_data.update({"submission_time": time.time()})
        if header == "vote_number":
            new_data.update({"vote_number": 0})
        if header == "view_number":
            new_data.update({"view_number": 0})
    return new_data


def delete_by_id(filename, index, key):
    final_file = []
    for row in filename:
        if row[key] != index:
            final_file.append(row)
    return final_file


def which_question(filename, id):
    for row in filename:
        if row["id"] == id:
            return row["question_id"]



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