
<div align = center>

<img src="./assets/logo_icon.svg" width="120" height="120" alt="Icon">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="./assets/logo_text.svg" width="380" height="120" alt="Logo">

<br>

<p style="font-size: 20px;">Веб-приложение для трекинга сна с интеграцией ИИ.</p>

---

</div>

<h2><img height="20" src="./assets/sparkles.svg">&nbsp;&nbsp;Что такое Sleepy?</h2>

Sleepy – ваш помощник в мире здорового сна

Sleepy анализирует ваш сон и предоставляет персонализированные рекомендации для его улучшения. Мы используем передовые технологии для оценки качества сна, выявления факторов, влияющих на засыпание и пробуждение, а также для оптимизации режима сна. Наш сервис поможет вам сформировать здоровые привычки сна, чтобы каждое утро начиналось с бодрости и энергии.

<h2><img height="20" src="./assets/sparkles.svg">&nbsp;&nbsp;Почему Sleepy?</h2>

Sleepy использует ИИ для предоставления рекомендаций и оценки качества сна. При вводе информации о сегодняшнем сне ИИ использует все Ваши предыдущие записи и на их почве выстраивает ответ.

<h2><img height="20" src="./assets/sparkles.svg">&nbsp;&nbsp;Завершённость</h2>

> [!WARNING]  
> Sleepy находится на самой ранней стадии разработки и совсем не является завершённым продуктом. Используйте на свой страх и риск.  

На данный момент готовы следующие функции приложения:
- [x] Сервер с REST API
- [x] Интерфейс для взаимодействия с приложением
- [ ] Авторизация (пока что готова наполовину)
- [ ] Завершённый интерфейс с функционалом

<h2><img height="20" src="./assets/sparkles.svg">&nbsp;&nbsp;Как использовать</h2>

### Требования
1. Python
2. NodeJS
3. PostgreSQL
4. uv  
    (`pip install uv`)
5. Concurrently  
    (`npm i -g concurrently`)

### Шаги для запуска

1. Клонировать репозиторий.  
    ```console
    git clone https://github.com/erema11a9/sleep-app.git
    ```
2. Перейти в папку с проектом.  
    ```console
    cd sleep-app
    ```
3. Переименовать `.env.example` в папке `backend`, чтоб получилось `.env` и заполнить этот файл.

Для разработки:  
1. Запустить dev-версию.  
    ```console
    npm start_dev
    ```
2. Зайти на https://localhost:5173/

Для продакшна:
1. Запустить prod-версию.
   ```console
    npm start_prod
    ```
2. Зайти на https://localhost:5000

<h2><img height="20" src="./assets/sparkles.svg">&nbsp;&nbsp;Разработчики</h2>

[erema11a9](https://github.com/erema11a9)  
[maxxeddd](https://github.com/maxxeddd)