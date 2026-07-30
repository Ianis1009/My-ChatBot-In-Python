from flask import Flask, render_template, request, jsonify

import voice


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if data is None:

        return jsonify({
            "response": "[ERROR]: Invalid request."
        }), 400


    command = data.get("message", "").strip()

    if command == "":
        return jsonify({
            "response": "[INFO]: Please enter a command."
        }), 400

    voice.save_message("User", command)
    response = voice.process_command(command)
    voice.save_message("Bot", response)

    voice.speak(response, voice.current_voice)


    return jsonify({
        "response": response
    })


if __name__ == "__main__":

    voice.init_history()
    app.run(host="127.0.0.1", port=5000, debug=True)