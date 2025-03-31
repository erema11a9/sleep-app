<template>
    <div class="viewport">
        <div class="header">
            <a href="/" class="logo-link">
                <div class="logo-container">
                    <img :src="logoIcon" alt="logo icon" class="logo" />
                    <img :src="logoText" alt="logo text" class="logo logo-text" />
                </div>
            </a>

            <div class="right-container">
                <a href="/about-us" class="about">О нас</a>
                <button @click="goto('/sign-in')" class="login">Вход</button>
                <button @click="goto('/sign-up')" class="register">Регистрация</button>
            </div>
        </div>

        <div class="main-container">
            <div class="main">
                <h1 class="section-name">О нас</h1>
                <p class="description">
                    Мы — группа студентов КнАГУ, разрабатывающая проект Sleepy для
                    оценки и улучшения сна. Наша команда из четырёх человек создаёт
                    систему, которая с помощью искусственного интеллекта анализирует
                    качество сна, предоставляет персональные рекомендации и помогает
                    оптимизировать режим отдыха. Мы стремимся сделать Sleepy
                    удобным, точным и полезным инструментом для всех, кто заботится
                    о своём здоровье и самочувствии.
                </p>

                <div class="cards">
                    <div class="card">
                        <img :src="erema" alt="Human" class="photograph" />
                        <h1>Еремин Дмитрий</h1>
                        <p>Вот он крутой конечно вообще он всё знает прям супер-программист</p>
                    </div>
                    <div class="card">
                        <img :src="MAX" alt="Human" class="photograph" />
                        <h1>Дудин Максим</h1>
                        <p>Вот он крутой конечно вообще он всё знает прям супер-программист</p>
                    </div>
                    <div class="card">
                        <img :src="Fil" alt="Human" class="photograph" />
                        <h1>Филиппов Дмитрий</h1>
                        <p>Вот он крутой конечно вообще он всё знает прям супер-программист</p>
                    </div>
                    <div class="card">
                        <img :src="Alex" alt="Human" class="photograph" />
                        <h1>Шевченко Алексей</h1>
                        <p>Вот он крутой конечно вообще он всё знает прям супер-программист</p>
                    </div>
                </div>
            </div>

            <div class="footer">
                <div class="copyright">
                    <p>
                        © 2025 Студенты 2ИТб-2: Дудин М., Еремин Д., Филиппов Д.,
                        Шевченко А.
                    </p>
                </div>
                <div class="links">
                    <a href="https://github.com/erema11a9/sleep-app">
                        <img :src="github" alt="github" class="icon" height="10" />
                    </a>
                    <a href="/">
                        <img :src="tg" alt="tg" class="icon" height="10" />
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import logoIcon from "@/assets/logo.svg";
import logoText from "@/assets/logo_text.svg";
import github from "@/assets/github.svg";
import tg from "@/assets/tg.svg";
import erema from "@/assets/photo/erema.png";
import MAX from "@/assets/photo/MAX.jpg";
import Fil from "@/assets/photo/Fil.jpg";
import Alex from "@/assets/photo/Alex.jpg";

const router = useRouter();
const goto = (path) => router.push(path);
</script>

<style scoped>
@import "@/styles/shared_global.css";

* {
    font-weight: 500;
    font-size: 90%;
}

.header {
    height: 15vh;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.logo {
    height: 5vh;
}

.logo-text {
    margin: 0 0 0 0.5vw;
}

.logo-container {
    margin: 0 0 0 5vw;
}

.right-container {
    margin: 0 5vw 0 0;
}

.right-container>button {
    border-radius: 1em;
    padding: 0 1em;
    height: 4vh;
    cursor: pointer;
    font-size: 200%;
    text-align: center;
}

.right-container>button.register {
    border: none;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
}

.right-container>button.register:hover {
    background: linear-gradient(90deg,
            var(--primary-alt),
            var(--secondary-alt));
}

.right-container>button.login {
    background-color: transparent;
    border-style: solid;
    border-color: var(--foreground-dark);
    margin: 0 0.5vw 0 0;
}

.right-container>button.login:hover {
    background-color: rgba(224, 228, 255, 0.25);
}

a {
    all: unset;
    cursor: pointer;
}

.about {
    margin: 0 3vw 0 0;
    font-size: 1.5em;
    color: rgb(224, 228, 255);
    text-shadow: 0 0 5px rgba(224, 228, 255, 0.5);
}

.main-container {
    width: 100vw;
    height: 85vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 80%;
}

.section-name {
    font-size: 4em;
    width: 100%;
    margin: 2vh 0;
}

.description {
    font-size: 2em;
    margin: 1vh 0;
}

.cards {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2vh 0;
}

.card {
    height: 96%;
    width: 24%;
    background: linear-gradient(45deg,
            var(--background-dark),
            var(--background-dark-alt));
    border-radius: 2vmax;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 0 20px #00000033;
}

.photograph {
    aspect-ratio: 1 / 1;
    width: 50%;
    border-radius: 100vmax;
}

.card>p {
    font-size: 2em;
    text-align: center;
    padding: 0 4vw;
}


.card>h1 {
    font-size: 4em;
    text-align: center;
    padding: 0 8vw;
}

.footer {
    display: flex;
    justify-content: space-between;
    align-content: center;
    height: 5vh;
    width: 80vw;
}

.copyright {
    flex-grow: 0;
    flex-shrink: 0;

    margin: auto 0;
}

.copyright>* {
    all: unset;
    font-size: 1.1em;
    color: rgba(224, 228, 255, 0.25);
}

.links {
    max-width: 10vh;
    opacity: 0.25;
}

.icon {
    height: 80%;
}
</style>