<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    let token;
    onMount(() => {
        token = localStorage.getItem("token") || "";
    });

    let message = $state();

    let nickname: string = $state("");

    let passFieldType: "password" | "text" = $state("password");
    function togglePasswordVisibility() {
        passFieldType = passFieldType === "password" ? "text" : "password";
    }
    let password: string = $state("");

    async function login() {
        let credentials = {
            nickname,
            password,
        };

        const RESPONSE = await fetch("http://localhost:5000/api/login", {
            method: "POST",
            body: JSON.stringify(credentials),
            headers: { "Content-Type": "application/json" },
        });

        if (RESPONSE.ok) {
            let data = await RESPONSE.json();
            token = data.access_token;
            localStorage.setItem("token", token);
            goto("/app");
        } else {
            message = "Проверьте логин или пароль.";
        }
    }
</script>

<a href="../">На главную</a>
<br />
<br />
<label for="nickname">Ваш никнейм</label>
<br />
<input
    type="text"
    name="nickname"
    id="nickname"
    bind:value={nickname}
    placeholder="Никнейм"
/>
<br />
<br />
<label for="password">Ваш пароль</label>
<br />
<input
    type={passFieldType}
    name="password"
    id="password"
    bind:value={password}
    placeholder="Пароль"
/>
<input
    type="checkbox"
    name="showPassword"
    id="showPassword"
    onclick={togglePasswordVisibility}
/>
<br />
<br />
{#if message}
    <p>{message}</p>
{/if}
<button onclick={login}> Войти </button>
<br />
<p>Нет аккаунта? <a href="../sign-up">Зарегистрироваться</a></p>
