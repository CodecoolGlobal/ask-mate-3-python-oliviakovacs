import connection


def sort(filename, type="submission_time", order="descending"):
    data = connection.get_data(filename)
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[i][type].isnumeric() and int(data[i][type]) > int(data[j][type]):
                data[i], data[j] = data[j], data[i]
            elif data[i][type] > data[j][type]:
                data[i], data[j] = data[j], data[i]
    if order == "descending":
        return data
    return data[::-1]


def get_question_by_id(id):
    questions = connection.get_data(connection.DATA_FILE_PATH_QUESTION)
    for question in questions:
        if question["id"] == id:
            return question


def get_answers_by_question_id(question_id):
    answers = connection.get_data(connection.DATA_FILE_PATH_ANSWER)
    question_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            question_answers.append(answer)
    return question_answers
