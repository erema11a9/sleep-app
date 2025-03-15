from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg2.pool import SimpleConnectionPool

from dotenv import load_dotenv
import json
import os

# Загрузить переменные среды из .env файла
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080/"]) # Чтоб можно было подключиться из Vue

# Пока что подключение к локальной БД. Потом будет на сервере
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
)

# АПИ чтоб можно было в Vue получать данные из БД
#
# Пока что работает просто при заходе на http://127.0.0.1:5000/api/sleep_stats,
# потом закроем это и сделаем, чтоб только Vue мог получать данные
@app.route('/api/sleep_stats', methods=['GET'])
def get_data():
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM sleep_stats;")
            data = cur.fetchall()
            return jsonify(json.dumps([
                {
                    'user_id': row[0],
                    'age': row[1],
                    'gender': row[2],
                    'sleep_quality': row[3],
                    'bedtime': row[4],
                    'wakeup_time': row[5],
                    'daily_steps': row[6],
                    'calories_burned': row[7],
                    'physical_activity': row[8],
                    'dietary_habits': row[9]
                }
                for row in data], default=str))
    finally:
        pool.putconn(conn)

# Это чтоб можно было заливать данные в БД
#
# Пока что никак не используется, не защищено и даже может помочь взломать БД
# И выглядит убого. Короче потом переделаю, подключу ORM и всё будет по кайфу
@app.route('/api/sleep_stats', methods=['POST'])
def add_data():
    new_data = request.json
    conn = pool.getconn()
    try:
        # Тут полный треш, но пока так
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sleep_db (
                user_id,
                age,
                gender,
                sleep_quality,
                bedtime,
                wakeup_time,
                daily_steps,
                calories_burned,
                physical_activity,
                dietary_habits
                ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                );
                """,
                new_data['user_id'],
                new_data['age'],
                new_data['gender'],
                new_data['sleep_quality'],
                new_data['bedtime'],
                new_data['wakeup_time'],
                new_data['daily_steps'],
                new_data['calories_burned'],
                new_data['physical_activity'],
                new_data['dietary_habits'],
            )
            conn.commit()
            return jsonify({'message': 'Данные добавлены'}), 201
    finally:
        pool.putconn(conn)

if __name__ == "__main__":
    app.run(debug=True)
