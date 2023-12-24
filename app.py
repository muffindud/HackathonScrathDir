from flask import Flask, jsonify
from main import *


app = Flask(__name__)


@app.route("/get_groups", methods=["GET"])
def get_groups():
    return jsonify(groups)


@app.route("/group=<int:group_id>", methods=["GET"])
def get_group_schedule(group_id):
    return jsonify([group_schedule[0][group_id], group_schedule[1][group_id]])


def main():
    compute()
    app.run()


if __name__ == "__main__":
    main()
