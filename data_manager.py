import connection
import time
from flask import request


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


def get_question_by_id(id, option):
    questions = get_selected_data(option)
    for question in questions:
        if question["id"] == id:
            return question


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
    for row in file_list:
        ids.append(int(row["id"]))
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
    finale_file = []
    for row in filename:
        if row[key] != index:
            finale_file.append(row)
    return finale_file


def which_question(filename, id):
    for row in filename:
        if row["id"] == id:
            return row["question_id"]


def add_new_content(which, id=0):
    if which == "question":
        file_name = connection.DATA_FILE_PATH_QUESTION
        headers = connection.DATA_HEADER_QUESTION
    elif which == "answer":
        file_name = connection.DATA_FILE_PATH_ANSWER
        headers = connection.DATA_HEADER_ANSWER
    existing_content = get_selected_data(which)
    new_content = create_new_data(headers, file_name)
    for header in headers:
        if header == "title":
            new_content.update({header: request.form["title"]})
        if header == "message":
            new_content.update({header: request.form["message"]})
        if header == "question_id":
            new_content.update({header: id})
        # if header == "image":
        # new_question.update({header: request.form["image"]})
    existing_content.append(new_content)
    connection.write_data(file_name, existing_content, headers)


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
