<script setup lang>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import logoIcon from "@/assets/logo.svg";
import logoText from "@/assets/logo_text.svg";
import github from "@/assets/github.svg";
import tg from "@/assets/tg.svg";

const router = useRouter();
const animPlay = ref(false);

onMounted(() => {
  animPlay.value = true;
});

const navigate = (path) => {
  router.push(path);
};
</script>

<template>
  <div class="viewport">
    <div class="header">
      <router-link to="/" class="logo-link">
        <div class="logo-container">
          <img :src="logoIcon" alt="logo_icon" class="logo" />
          <img :src="logoText" alt="logo_text" class="logo logo-text" />
        </div>
      </router-link>

      <div class="right-container">
        <a href="/about-us" class="about">О нас</a>
        <button @click="navigate('/sign-in')" class="login">Вход</button>
        <button @click="navigate('/sign-up')" class="register">Регистрация</button>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="animPlay" class="main-container">
        <div class="main">
          <h1 class="fade-in">Sleepy – ваш помощник в мире здорового сна</h1>
          <p class="description fade-in delay-1s">
            Sleepy анализирует ваш сон и предоставляет персонализированные рекомендации для его
            улучшения. Мы используем передовые технологии для оценки качества отдыха, выявления
            факторов, влияющих на засыпание и пробуждение, а также для оптимизации режима сна.
          </p>
          <button @click="navigate('/sign-up')" class="start fade-in delay-2s">Начать</button>
        </div>

        <div class="footer">
          <div class="copyright">
            <p>© Студенты 2ИТб-2: Дудин М., Еремин Д., Филиппов Д., Шевченко А., 2025</p>
          </div>
          <div class="links">
            <a href="https://github.com/erema11a9/sleep-app">
              <img :src="github" alt="github" class="icon" />
            </a>
            <a href="/">
              <img :src="tg" alt="tg" class="icon" />
            </a>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style>
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
  margin-left: 0.5vw;
}

.logo-container {
  margin-left: 5vw;
}

.right-container {
  margin-right: 5vw;
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
  background: linear-gradient(90deg, var(--primary-alt), var(--secondary-alt));
}

.right-container>button.login {
  background-color: transparent;
  border-style: solid;
  border-color: var(--foreground-dark);
  margin-right: 0.5vw;
}

.right-container>button.login:hover {
  background-color: rgba(224, 228, 255, 0.25);
}

a {
  all: unset;
  cursor: pointer;
}

.about {
  margin-right: 3vw;
  font-size: 1.5em;
  color: rgba(224, 228, 255, 0.75);
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

h1 {
  font-size: 5em;
  text-align: center;
  background-image: linear-gradient(90deg, var(--primary-alt), var(--secondary-alt));
  color: transparent;
  background-clip: text;
}

.description {
  font-size: 3em;
  text-align: center;
}

button.start {
  border: none;
  margin-top: 5vh;
  border-radius: 1vmax;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  width: 30vw;
  height: 10vh;
  font-size: 5em;
  font-weight: 700;
  text-align: center;
  cursor: pointer;
}

button.start:hover {
  background: linear-gradient(90deg, var(--primary-alt), var(--secondary-alt));
}

.footer {
  display: flex;
  justify-content: space-between;
  align-content: center;
  height: 5vh;
  width: 80vw;
}

.copyright {
  margin: auto 0;
}

.copyright>* {
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

/* Анимации */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 1s forwards;
}

.fade-in.delay-1s {
  animation-delay: 1s;
}

.fade-in.delay-2s {
  animation-delay: 2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>
