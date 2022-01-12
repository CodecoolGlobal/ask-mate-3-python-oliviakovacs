from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import datetime



app = Flask(__name__)


@app.route("/")
@app.route("/list", methods=['GET'])
def main_page():
    if request.args:
        order = request.args['order-by']
        direction = request.args['direction']
        data = data_manager.get_questions(order, direction)
        headers = data_manager.get_question_headers()
        return render_template('main.html', questions=data, headers=headers)
    data = data_manager.get_questions('submission_time', 'DESC')
    headers = data_manager.get_question_headers()
    return render_template('main.html', questions=data, headers=headers)


@app.route("/question/<question_id>/new-comment")

#
# # @app.route("/question")
# @app.route("/question/<id>")
# def display_question(id):
#     question = data_manager.get_question_by_id(id, "question")
#     answers = data_manager.get_answers_by_question_id(id, 'answer')
#     return render_template("question.html", question=question, answers=answers)


@app.route("/question/<id>")
def display_question(id):
    question = data_manager.get_question_by_id(id)
    answers = data_manager.get_answers_by_question_id(id)
    return render_template("question_by_id.html", question=question, answers=answers, id=id)


@app.route("/add-question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        max_id = data_manager.get_question_ids()
        now = datetime.datetime.now()
        new_question=[]
        new_question.append(max_id[0]['maximum'])
        new_question.append(now)
        new_question.append(0)
        new_question.append(0)
        new_question.append(request.form.get("title"))
        new_question.append(request.form.get("message"))
        #new_question.append(request.form.get(pics))
        data_manager.add_new_question(new_question)
        # Ide kell majd a Pics!!!

        return redirect('/list')

    question = {'title': '', 'message': ''}
    return render_template("ask_mate_1/form.html", visible_data=question, route="/add-question", is_question=True)


@app.route('/question/<question_id>/new-answer', methods=["POST", "GET"])
def add_answer(question_id):
    if request.method == "POST":
        max_id = data_manager.get_question_ids()
        max_answer_id = data_manager.get_answer_ids()
        now = datetime.datetime.now()
        new_answer = []
        new_answer.append(max_answer_id[0]['maximum'])
        new_answer.append(now)
        new_answer.append(0)
        new_answer.append(question_id)
        new_answer.append(request.form.get("message"))
        #new_question.append(pic)
        data_manager.add_new_answer(new_answer)
        return redirect(f"/question/{question_id}")
    question = {'title': '', 'message': ''}
    return render_template("form.html", visible_data=question, route=f"/question/{question_id}/new-answer", is_question=False)


@app.route('/question/<id>/delete', methods=["GET"])
def delete_question(id):
    data_manager.delete_comment_by_question_id(id)
    data_manager.delete_answer_by_question_id(id)
    data_manager.delete_question_by_id(id)
    return redirect("/list")


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def edit_question(question_id):
    if request.method == "POST":
        question = request.form["question_title"]
        message = request.form["question_message"]
        data_manager.edit_question(question_id, question, message)
        return redirect(url_for("display_question", id=question_id))
    question = data_manager.get_question_by_id(question_id)
    return render_template("edit_question.html", question=question, q_id=question_id)


@app.route('/answer/<answer_id>/delete', methods=["POST", "GET"])
def delete_answer(answer_id):
    data_manager.delete_comment_by_answer_id(answer_id)
    return_question_id = data_manager.delete_answer_by_id(answer_id)
    return redirect("/question/" + str(return_question_id['question_id']))


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    change = 1
    data_manager.change_vote_by_id(["question", question_id,  change, "id"])
    return redirect(url_for("display_question", id=question_id))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    change = -1
    data_manager.change_vote_by_id(["question", question_id,  change, "id"])
    return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<id>/vote_up')
def vote_up_answer(id):
    old_data = data_manager.change_vote_by_id(id, "answer", "increase")
    question_id = data_manager.which_question(old_data, id)
    return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<id>/vote_down')
def vote_down_answer(id):
    old_data = data_manager.change_vote_by_id(id, "answer", "decrease")
    question_id = data_manager.which_question(old_data, id)
    return redirect(url_for("display_question", id=question_id))

@app.route('/question/pics/<link>')
def giv_pics_to_question(link):
    header = connection.DATA_HEADER_QUESTION
    data = data_manager.get_selected_data("question")
    question_with_pics = data_manager.give_pics(link, data)
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, question_with_pics, header)
    default_sort_data = data_manager.sort(data)
    return render_template('ask_mate_1/list.html', questions=default_sort_data)


@app.route('/answer/pics/<link>')
def giv_pics_to_answer(link):
    header = connection.DATA_HEADER_ANSWER
    data = data_manager.get_selected_data("answer")
    answer_with_pics = data_manager.give_pics(link, data)
    connection.write_data(connection.DATA_FILE_PATH_QUESTION, answer_with_pics, header)
    default_sort_data = data_manager.sort(data)
    return render_template('ask_mate_1/list.html', questions=default_sort_data)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5001
    )
