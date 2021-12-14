from flask import Flask
import data_manager
import connection

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main_page():
    data = data_manager.sort(connection.DATA_FILE_PATH_QUESTION)
    return data[0]["id"]




if __name__ == "__main__":
    app.run()
