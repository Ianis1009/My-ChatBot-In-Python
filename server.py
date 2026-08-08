from flask import Flask, render_template, request, jsonify

import voice # voice.py
import travel as travel_module # travel.py
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/travel")
def travel():
    return render_template("travel.html")


@app.route("/moto")
def moto():
    return render_template("moto.html")

@app.route("/api/voice", methods=["POST"])
def set_voice_state():
    data = request.get_json()
    enabled = data.get("enabled")
    if not isinstance(enabled, bool):
        return jsonify({"error":"enabled must be bool"}), 400
    voice.voice_enabled = enabled
    return jsonify({"voice_enabled" : voice.voice_enabled})



@app.route("/api/travel/route", methods=["POST"])
def travel_route():

    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request."
        }), 400

    origin = data.get("origin", "").strip()
    destination = data.get("destination", "").strip()

    if not origin or not destination:
        return jsonify({
            "success": False,
            "error": "Both origin and destination are required."
        }), 400

    result = travel_module.calculate_route(origin, destination)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result)

@app.route("/api/voice", methods=["GET"])
def get_voice_state():
    return jsonify({"voice_enabled": voice.voice_enabled})


@app.route("/chat", methods=["POST"])
def chat():
    
        # data = request.get_json()
    
        # if data is None:
    
        #     return jsonify({
        #         "response": "[ERROR]: Invalid request."
        #     }), 400
    
    
        # command = data.get("message", "").strip()
    
        # if command == "":
        #     return jsonify({
        #         "response": "[INFO]: Please enter a command."
        #     }), 400
    
        # voice.save_message("User", command)
        # response = voice.process_command(command)
        # voice.save_message("Bot", response)
    
        # voice.speak(response, voice.current_voice)
    
    
        # return jsonify({
        #     "response": response
        # })

    data = request.get_json()
    if data is None:
        return jsonify({"response":"[ERROR]: Invalid request."}), 400

    command = data.get("message", "").strip()

    if command == "":
        return jsonify({"response":"[INFO]: Please enter a command."}), 400

    voice.save_message("User", command)
    response = voice.process_command(command)
    voice.save_message("Bot", response)
    voice.speak(response, voice.current_voice)

    return jsonify({"response":response, "voice_enabled":voice.voice_enabled})
    

if __name__ == "__main__":

    voice.init_history()
    app.run(host="127.0.0.1", port=5000, debug=True)