from flask import Flask, render_template, request, jsonify, send_from_directory

import os

import voice # voice.py
import travel as travel_module # travel.py
import moto # moto.py
import blog # blog.py

from models import db, User #models.py

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/history")
def history():
    return send_from_directory(os.path.join(app.root_path, "templates"),"history.txt",mimetype="text/plain")

@app.route("/travel")
def travel():
    return render_template("travel.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:

            flash("Please fill in all fields.", "error")

            return redirect(url_for("register"))


        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()


        if existing_user:

            flash(
                "Username or email already exists.",
                "error"
            )

            return redirect(url_for("register"))


        user = User(
            username=username,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()


        session["user_id"] = user.id
        session["username"] = user.username


        return redirect(url_for("index"))


    return render_template("register.html")

@app.route("/blog")
def blog_page():

    articles = blog.get_all_articles()

    return render_template("blog.html",articles=articles)


@app.route("/blog/<int:article_id>")
def article_page(article_id):

    article = blog.get_article_by_id(article_id)

    if article is None:
        return "Article not found", 404

    return render_template("article.html",article=article)

@app.route("/moto")
def moto_page():
    vehicles = moto.get_all_vehicles()
    return render_template("moto.html", vehicles=vehicles)

@app.route("/moto/<int:vehicle_id>")
def vehicle_page(vehicle_id):

    vehicle = moto.get_vehicle_by_id(vehicle_id)

    if vehicle is None:
        return "Vehicle not found", 404

    vehicle["voice_message"] = moto.build_vehicle_message(vehicle)

    return render_template(
        "vehicle.html",
        vehicle=vehicle
    )


@app.route("/api/moto/speak", methods=["POST"])
def moto_speak():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request."
        }), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "success": False,
            "error": "No text provided."
        }), 400

    if not voice.voice_enabled:
        return jsonify({
            "success": False,
            "error": "Voice is currently muted."
        }), 400

    voice.speak(
        text,
        voice.current_voice
    )

    return jsonify({
        "success": True
    })


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

    result = travel_module.calculate_route(origin,destination)

    if not result["success"]:
        return jsonify(result), 404

    voice_message = travel_module.build_route_message(result)

    result["voice_message"] = voice_message

    return jsonify(result)


@app.route("/api/travel/speak", methods=["POST"])
def travel_speak():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request."
        }), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "success": False,
            "error": "No text provided."
        }), 400

    if not voice.voice_enabled:
        return jsonify({
            "success": False,
            "error": "Voice is currently muted."
        }), 400

    voice.speak(
        text,
        voice.current_voice
    )

    return jsonify({
        "success": True
    })

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
    


@app.route("/api/moto/<int:vehicle_id>/info")
def vehicle_info(vehicle_id):

    vehicle = moto.get_vehicle_by_id(vehicle_id)

    if vehicle is None:
        return jsonify({
            "success": False,
            "error": "Vehicle not found."
        }), 404

    message = moto.build_vehicle_message(vehicle)

    return jsonify({
        "success": True,
        "vehicle": vehicle["name"],
        "message": message
    })


if __name__ == "__main__":

    voice.init_history()
    app.run(host="127.0.0.1", port=5000, debug=True)