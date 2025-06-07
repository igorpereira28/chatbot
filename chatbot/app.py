from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot_model import Chatbot
import os

app = Flask(__name__)
CORS(app)  # Permite CORS para todas as rotas e origens

bot = Chatbot()

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    response = bot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
