from flask import Flask, render_template, request, jsonify, send_from_directory
from chatbot_model import Chatbot
import os

# Caminhos do frontend
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend')

# Inicialização do Flask com paths personalizados
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
bot = Chatbot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/style.css")
def style():
    return send_from_directory(STATIC_DIR, "style.css")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    response = bot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
