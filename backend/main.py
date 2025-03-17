from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, INT, SMALLINT, CHAR, VARCHAR, TIME, DATE

from dotenv import load_dotenv
import json
import os

# Загрузить переменные среды из .env файла
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080/"])  # Чтоб можно было подключиться из Vue
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@dataclass
class SleepStats(db.Model):
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


@dataclass
class Users(db.Model):
    __tablename__ = "users"

    nickname: str = Column(VARCHAR(16))
    password: str = Column(VARCHAR(20))
    birth_date: str = Column(DATE)
    age: int = Column(SMALLINT)
    gender: str = Column(CHAR(1))
    id: int = Column(INT, primary_key=True)


# АПИ чтоб можно было в Vue получать статы сна из БД
@app.route("/api/sleep_stats", methods=["GET"])
def get_stats():
    stats = SleepStats.query.all()
    return jsonify(json.dumps(stats, default=str))


# Это чтоб можно было заливать статы сна в БД
@app.route("/api/sleep_stats", methods=["POST"])
def add_stat():
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
        return jsonify({"message": f"Data has not been added, KeyError: {e}"}), 400


# Чтоб добавлять новых пользователей
@app.route("/api/users", methods=["POST"])
def add_user():
    received_data = request.json
    try:
        new_user = Users(
            nickname=received_data["nickname"],
            password=received_data["password"],
            birth_date=received_data["birth_date"],
            age=received_data["age"],
            gender=received_data["gender"],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Data has been added"}), 201
    except KeyError as e:
        print("KeyError:", e)
        return jsonify({"message": f"Data has not been added, KeyError: {e}"}), 400


if __name__ == "__main__":
    app.run(debug=True)
