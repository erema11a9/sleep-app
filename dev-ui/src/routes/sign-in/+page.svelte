<script lang="ts">
    import logo from "$lib/assets/logo_text.svg";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    import { fade } from "svelte/transition";

    let token;
    onMount(() => {
        token = localStorage.getItem("token") || "";
    });

    let nickname: string = $state("");

    let showPassword: boolean = $state(false);
    let passFieldType: "password" | "text" = $derived(
        showPassword ? "text" : "password"
    );
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
            errorMessage = "Проверьте логин или пароль.";
        }
    }

    let errorMessage = $state();
</script>

<div class="viewport">
    <div in:fade={{ duration: 1000 }} class="login-window">
        <div class="login-contents">
            <a href="/"><img src={logo} alt="Logo" /></a>

            {#if errorMessage}
                <div class="error-container">
                    <p class="error-message">{errorMessage}</p>
                </div>
            {/if}

            <div class="field">
                <label for="nickname">Ваш никнейм</label>
                <input
                    type="text"
                    name="nickname"
                    id="nickname"
                    bind:value={nickname}
                    placeholder="Никнейм"
                />
            </div>

            <div class="field">
                <label for="password">Ваш пароль</label>
                <input
                    type={passFieldType}
                    name="password"
                    id="password"
                    bind:value={password}
                    placeholder="Пароль"
                />
            </div>

            <p>
                <label class="checkbox">
                    <input
                        type="checkbox"
                        name="showPassword"
                        id="showPassword"
                        bind:checked={showPassword}
                    />Показать пароль
                </label>
            </p>

            <button onclick={login}> Войти </button>

            <p class="no-account">
                Нет аккаунта? <a href="../sign-up" class="no-account"
                    >Зарегистрироваться</a
                >
            </p>
        </div>
    </div>
</div>

<style>
    @import "../../styles/shared_reg_log.css";
</style>
