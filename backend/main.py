from dataclasses import dataclass

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, INT, SMALLINT, CHAR, VARCHAR, TIME, DATE

from dotenv import load_dotenv
import os
from pathlib import Path

# Загрузить переменные среды из .env файла
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

app = Flask(
    __name__,
    static_folder="../frontend/build",
)
CORS(app, origins=["http://localhost:5173"])  # Чтоб можно было подключиться из фронта

app.config["JWT_SECRET_KEY"] = "qweqweqweqwe123123"
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@dataclass
class SleepStats(db.Model):
    """Модель таблицы со статами"""

    __tablename__ = "sleep_stats"

    user_id: int = Column(INT)
    age: int = Column(SMALLINT)
    gender: str = Column(CHAR(1))
    sleep_quality: int = Column(SMALLINT)
    bedtime: str = Column(TIME)
    wakeup_time: str = Column(TIME)
    daily_steps: int = Column(INT)
    calories_burned: int = Column(INT)
    physical_activity: str = Column(VARCHAR(7))
    dietary_habits: str = Column(VARCHAR(10))
    stat_id: int = Column(INT, primary_key=True)

    def serialise(self):
        return {
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender,
            "sleep_quality": self.sleep_quality,
            "bedtime": str(self.bedtime),
            "wakeup_time": str(self.wakeup_time),
            "daily_steps": self.daily_steps,
            "calories_burned": self.calories_burned,
            "physical_activity": self.physical_activity,
            "dietary_habits": self.dietary_habits,
            "stat_id": self.stat_id,
        }


@dataclass
class Users(db.Model):
    """Модель таблицы пользователей"""

    __tablename__ = "users"

    nickname: str = Column(VARCHAR(16))
    password: str = Column(VARCHAR(20))
    birth_date: str = Column(DATE)
    gender: str = Column(CHAR(1))
    id: int = Column(INT, primary_key=True)

    def serialise(self):
        return {
            "nickname": self.nickname,
            "password": self.password,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "id": self.id,
        }


# Получать и добавлять статы. Запихнул всё в одну функцию, не знал, что так можно.
# Не очень нравится, но посмотрим как будет работать.
@app.route("/api/sleep_stats", methods=["POST", "GET"])
def handle_stats():
    match request.method:
        case "POST":
            received_data = request.json
            try:
                new_stat = SleepStats(
                    user_id=received_data["user_id"],
                    age=received_data["age"],
                    gender=received_data["gender"],
                    sleep_quality=received_data["sleep_quality"],
                    bedtime=received_data["bedtime"],
                    wakeup_time=received_data["wakeup_time"],
                    daily_steps=received_data["daily_steps"],
                    calories_burned=received_data["calories_burned"],
                    physical_activity=received_data["physical_activity"],
                    dietary_habits=received_data["dietary_habits"],
                )
                db.session.add(new_stat)
                db.session.commit()
                return jsonify({"message": "Data has been added"}), 201
            except KeyError as e:
                print("KeyError:", e)
                return jsonify(
                    {"message": f"Data has not been added, KeyError: {e}"}
                ), 400

        case "GET":
            stats = SleepStats.query.all()
            return jsonify([stat.serialise() for stat in stats])


# Логин (теперь работает)
@app.route("/api/login", methods=["POST"])
def get_users():
    received_data = request.json
    print(received_data)
    nickname = received_data.get("nickname")
    password = received_data.get("password")
    user = Users.query.filter(Users.nickname == nickname).first()

    if user and user.password == password:
        print("logged in successfully")
        access_token = create_access_token(identity=nickname)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


# Чтоб добавлять новых пользователей
@app.route("/api/reg", methods=["POST"])
def add_user():
    received_data = request.json
    try:
        new_user = Users(
            nickname=received_data["nickname"],
            password=received_data["password"],
            birth_date=received_data["birth_date"],
            gender=received_data["gender"],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Data has been added"}), 201
    except KeyError as e:
        print("KeyError:", e)
        return jsonify({"error": f"Data has not been added, KeyError: {e}"}), 400


@app.route("/app")
@jwt_required
def main_app_page():
    print(get_jwt_identity())
    return send_from_directory(app.static_folder, "app.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path == "":
        return send_from_directory(app.static_folder, "index.html")

    static_path = Path(app.static_folder) / path
    print(static_path)
    if static_path.exists():
        return send_from_directory(app.static_folder, path)

    html_path = Path(app.static_folder) / f"{path}.html"
    if html_path.exists():
        return send_from_directory(app.static_folder, f"{path}.html")

    return send_from_directory(app.static_folder, "404.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
