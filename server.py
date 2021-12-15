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


@app.route("/add-question", methods=["POST"])
def add_question():
    if request.method == "POST":
        all_questions = connection.get_data(connection.DATA_FILE_PATH_QUESTION)
        new_question = data_manager.create_new_data(connection.DATA_HEADER_QUESTION, all_questions)
        for header in connection.DATA_HEADER_QUESTION:
            if header == "title":
                new_question.update({header: request.form["title"]})
            if header == "message":
                new_question.update({header: request.form["message"]})
            if header == "image":
                new_question.update({header: request.form["image"]})
        return redirect("/list")
    question_id = None
    return render_template("form.html", id=question_id)


@app.route('/question/<question_id>/new-answer')
def add_answer():
    pass


@app.route('/question/<question_id>/delete')
def delete_question():
    pass


@app.route('/question/<question_id>/edit')
def edit_question():
    pass


@app.route('/answer/<answer_id>/delete')
def delete_answer():
    pass


@app.route('/question/<question_id>/vote_up')
def vote_up_question():
    pass


@app.route('/question/<question_id>/vote_down')
def vote_down_question():
    pass


@app.route('/answer/<question_id>/vote_up')
def vote_up_answer():
    pass


@app.route('/answer/<question_id>/vote_down')
def vote_down_answer():
    pass


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
