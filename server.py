from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main_page():
    data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    return render_template('list.html', questions=data)


# @app.route("/question")
@app.route("/question/<id>")
def display_question(id):
    question = data_manager.get_question_by_id(id)
    answers = data_manager.get_answers_by_question_id(id)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        data_manager.add_new_content(connection.DATA_FILE_PATH_QUESTION, connection.DATA_HEADER_QUESTION)
        return redirect("/list")
    question = {'title': '', 'message': ''}
    return render_template("form.html", visible_data=question, route="/add-question", is_question=True)


@app.route('/question/<question_id>/new-answer', methods=["POST", "GET"])
def add_answer(question_id):
    if request.method == "POST":
        data_manager.add_new_content(connection.DATA_FILE_PATH_ANSWER, connection.DATA_HEADER_ANSWER, question_id)
        return redirect(f"/question/{question_id}")
    question = data_manager.get_question_by_id(question_id)
    return render_template("form.html", visible_data=question, route=f"/question/{question_id}/new-answer", is_question=False )


@app.route('/question/<id>/delete', methods=["GET"])
def delete_question(id):
    old_data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    data = data_manager.delete_by_id(old_data, id, "id")
    header = connection.DATA_HEADER_QUESTION
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, data, header)
    old_answers = data_manager.sort(connection.DATA_FILE_PATH_ANSWER)
    answer = data_manager.delete_by_id(old_answers, id, "question_id")
    answer_header = connection.DATA_HEADER_ANSWER
    connection.write_data(connection.DATA_FILE_PATH_ANSWER, answer, answer_header)
    return redirect("/list")


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def edit_question(question_id):
    if request.method == "POST":
        header = connection.DATA_HEADER_QUESTION
        old_data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION, type="submission_time", order="None")
        question_title = request.form['title']
        question_message = request.form['message']
        edited_question = data_manager.edit_question(old_data, question_title, question_message, question_id)
        connection.write_data(connection.DATA_FILE_PATH_QUESTION, edited_question, header)
        return redirect(url_for("display_question", id=question_id))
    question = {'title': '', 'message': ''}
    return render_template("form.html", visible_data=question, route=url_for('edit_question', question_id=question_id), is_question=True)


@app.route('/answer/<answer_id>/delete', methods=["POST", "GET"])
def delete_answer(answer_id):
    old_answers = data_manager.sort(connection.DATA_FILE_PATH_ANSWER)
    answer = data_manager.delete_by_id(old_answers, answer_id, "id")
    header = connection.DATA_HEADER_ANSWER
    connection.write_data(connection.DATA_FILE_PATH_ANSWER, answer, header)
    question_id = data_manager.which_question(old_answers, answer_id, "id")
    return redirect(url_for("display_question", id=question_id))


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    old_data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    data = data_manager.incrase_vote(old_data, question_id)
    header = connection.DATA_HEADER_QUESTION
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, data, header)
    return redirect(url_for("display_question", id=question_id))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    old_data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    data = data_manager.decrease_vote(old_data, question_id)
    header = connection.DATA_HEADER_QUESTION
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, data, header)
    return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<id>/vote_up')
def vote_up_answer(id):
    old_data = data_manager.sort(connection.DATA_FILE_PATH_ANSWER, order="None")
    data = data_manager.incrase_vote(old_data, id)
    header = connection.DATA_HEADER_ANSWER
    connection.write_data(connection.DATA_FILE_PATH_ANSWER, data, header)
    question_id = data_manager.which_question(old_data, id)
    return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<id>/vote_down')
def vote_down_answer(id):
    old_data = data_manager.sort(connection.DATA_FILE_PATH_ANSWER, order="None")
    data = data_manager.decrease_vote(old_data, id)
    header = connection.DATA_HEADER_ANSWER
    connection.write_data(connection.DATA_FILE_PATH_ANSWER, data, header)
    question_id = data_manager.which_question(old_data, id)
    return redirect(url_for("display_question", id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000
    )
