from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, INT, SMALLINT, CHAR, VARCHAR, TIME

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


# АПИ чтоб можно было в Vue получать данные из БД
#
# Пока что работает просто при заходе на http://127.0.0.1:5000/api/sleep_stats,
# потом закроем это и сделаем, чтоб только Vue мог получать данные
@app.route("/api/sleep_stats", methods=["GET"])
def get_data():
    stats = SleepStats.query.all()
    return jsonify(json.dumps(stats, default=str))


# Это чтоб можно было заливать данные в БД
@app.route("/api/sleep_stats", methods=["POST"])
def add_data():
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
    except KeyError as e:
        print("KeyError:", e)
        return jsonify({"message": f"Data has not been added, KeyError: {e}"}), 400
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({"message": "Data has been added"}), 201


if __name__ == "__main__":
    app.run(debug=True)
