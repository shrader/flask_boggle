from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}
game_info = ""


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game


    print({"gameId": game_id, "board": game.board})

    return jsonify({"gameId": game_id, "board": game.board})

@app.route("/api/score-word", methods=["POST"])
def score_words():

    response = request.json
    curr_word = response["word"].upper()
    curr_game = response["gameId"]

    if games[curr_game].is_word_in_word_list(curr_word) and games[curr_game].check_word_on_board(curr_word):
        return jsonify(result="ok")

    if not games[curr_game].is_word_in_word_list(curr_word):
        return jsonify(result="not-word")

    if not games[curr_game].check_word_on_board(curr_word):
        return jsonify(result="not-on-board")
 