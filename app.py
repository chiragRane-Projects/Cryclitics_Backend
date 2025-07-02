from flask import Flask, request, jsonify
from analysis import get_players, analyze_player
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/players", methods=["GET"])
def players():
    players_list = get_players()
    return jsonify({"players": players_list})

@app.route("/analyze", methods=["GET"])
def analyze():
    player = request.args.get("player")
    if not player:
        return jsonify({"error": "Player name is required"}), 400
    
    result = analyze_player(player)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)