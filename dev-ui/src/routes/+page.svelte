<script lang="ts">
    import logo_icon from "$lib/assets/logo_icon.svg";
    import logo_text from "$lib/assets/logo_text.svg";
    import github from "$lib/assets/github.svg";
    import tg from "$lib/assets/tg.svg";
    import { onMount } from "svelte";

    import { fade } from "svelte/transition";

    import { goto } from "$app/navigation";

    onMount(() => {
        animPlay = true;
    });
    let animPlay: boolean = false;
</script>

<div class="viewport">
    <div class="header">
        <a href="/" class="logo-link">
            <div class="logo-container">
                <img src={logo_icon} alt="logo icon" class="logo" />
                <img src={logo_text} alt="logo text" class="logo logo-text" />
            </div>
        </a>

        <div class="right-container">
            <a href="/about-us" class="about">О нас</a>
            <button
                onclick={() => {
                    goto("/sign-in");
                }}
                class="login"
            >
                Вход
            </button>
            <button
                onclick={() => {
                    goto("/sign-up");
                }}
                class="register"
            >
                Регистрация
            </button>
        </div>
    </div>
    {#if animPlay}
        <div class="main-container">
            <div class="main">
                <h1 in:fade={{ duration: 1000 }}>
                    Sleepy – ваш помощник в мире здорового сна
                </h1>
                <p
                    class="description"
                    in:fade={{ duration: 1000, delay: 1000 }}
                >
                    Sleepy анализирует ваш сон и предоставляет
                    персонализированные рекомендации для его улучшения. Мы
                    используем передовые технологии для оценки качества отдыха,
                    выявления факторов, влияющих на засыпание и пробуждение, а
                    также для оптимизации режима сна. Наш сервис поможет вам
                    сформировать здоровые привычки сна, чтобы каждое утро
                    начиналось с бодрости и энергии.
                </p>

                <button
                    in:fade={{ duration: 1000, delay: 3000 }}
                    onclick={() => {
                        goto("/sign-up");
                    }}
                    class="start"
                >
                    Начать
                </button>
            </div>

            <div class="footer">
                <div class="copyright">
                    <p>
                        © 2025 Студенты 2ИТб-2: Дудин М., Еремин Д., Филиппов
                        Д., Шевченко А.
                    </p>
                </div>
                <div class="links">
                    <a href="https://github.com/erema11a9/sleep-app">
                        <img
                            src={github}
                            alt="github"
                            class="icon"
                            height="10"
                        /></a
                    >
                    <a href="/">
                        <img src={tg} alt="tg" class="icon" height="10" /></a
                    >
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    @import "../styles/shared_global.css";

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

    .right-container > button {
        border-radius: 1em;
        padding: 0 1em;
        height: 4vh;
        cursor: pointer;
        font-size: 200%;
        text-align: center;
    }

    .right-container > button.register {
        border: none;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
    }
    .right-container > button.register:hover {
        background: linear-gradient(
            90deg,
            var(--primary-alt),
            var(--secondary-alt)
        );
    }

    .right-container > button.login {
        background-color: transparent;
        border-style: solid;
        border-color: var(--foreground-dark);
        margin: 0 0.5vw 0 0;
    }
    .right-container > button.login:hover {
        background-color: rgba(224, 228, 255, 0.25);
    }

    a {
        all: unset;
        cursor: pointer;
    }

    .about {
        margin: 0 3vw 0 0;
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
        background-image: linear-gradient(
            90deg,
            var(--primary-alt),
            var(--secondary-alt)
        );
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
        background: linear-gradient(
            90deg,
            var(--primary-alt),
            var(--secondary-alt)
        );
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
    .copyright > * {
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
