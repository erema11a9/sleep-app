<script lang="ts">
    import logo from "$lib/assets/logo_text.svg";
    import { goto } from "$app/navigation";

    import { fade } from "svelte/transition";

    function isAlphaNumeric(str: string) {
        var code, i, len;

        for (i = 0, len = str.length; i < len; i++) {
            code = str.charCodeAt(i);
            if (
                !(code > 47 && code < 58) && // numeric (0-9)
                !(code > 64 && code < 91) && // upper alpha (A-Z)
                !(code > 96 && code < 123)
            ) {
                // lower alpha (a-z)
                return false;
            }
        }
        return true;
    }

    let nickname: string = $state("");

    let passFieldType: "password" | "text" = $state("password");
    function togglePasswordVisibility() {
        passFieldType = passFieldType === "password" ? "text" : "password";
    }
    let password: string = $state("");

    let today: string = new Date().toISOString().substring(0, 10);
    let dateString: string = $state(today);

    let genders = $state([
        {
            char: "m",
            text: "Мужчина",
        },
        {
            char: "f",
            text: "Женщина",
        },
    ]);
    let selectedGender: string = $state("");

    function check(): boolean {
        errorMessage = null;

        if (!isAlphaNumeric(nickname)) {
            errorMessage =
                "В никнейме могут быть только латинские буквы и цифры";
        } else if (nickname.length < 4) {
            errorMessage = "Никнейм должен быть длиной 4 символа или больше";
        } else if (
            new Date(dateString).getFullYear() >
            new Date().getFullYear() - 2
        ) {
            errorMessage = "Недействительная дата рождения";
        } else if (selectedGender === "") {
            errorMessage = "Выберите пол";
        } else if (password.length < 8) {
            errorMessage = "Пароль должен быть длиной 8 символов или больше";
        }

        if (errorMessage) {
            return false;
        }

        return true;
    }

    async function register() {
        if (!check()) {
            return;
        }

        let stuff = {
            nickname,
            password,
            birth_date: dateString,
            gender: selectedGender,
        };

        const RESPONSE = await fetch("http://localhost:5000/api/reg", {
            method: "POST",
            body: JSON.stringify(stuff),
            headers: { "Content-Type": "application/json" },
        });

        if (RESPONSE.ok) {
            goto("/app");
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
                <label for="reg-nickname">Ваш никнейм</label>
                <input
                    type="text"
                    name="reg-nickname"
                    id="reg-nickname"
                    required
                    bind:value={nickname}
                    placeholder="Никнейм"
                />
            </div>

            <div class="field">
                <label for="birthdate">Дата рождения</label>
                <input
                    type="date"
                    name="birthdate"
                    id="birthdate"
                    required
                    max={today}
                    bind:value={dateString}
                />
            </div>

            <div class="field">
                <label for="gender">Пол</label>
                <select
                    name="gender"
                    required
                    id="gender"
                    bind:value={selectedGender}
                >
                    {#each genders as gender}
                        <option value={gender.char}>
                            {gender.text}
                        </option>
                    {/each}
                </select>
            </div>

            <div class="field">
                <label for="reg-password">Ваш пароль</label>
                <input
                    type={passFieldType}
                    name="reg-password"
                    id="reg-password"
                    required
                    minlength="8"
                    maxlength="20"
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
                        onclick={togglePasswordVisibility}
                    />Показать пароль
                </label>
            </p>

            <button onclick={register}> Регистрация </button>

            <p class="no-account">
                Уже есть аккаунт? <a href="../sign-in" class="no-account"
                    >Войти</a
                >
            </p>
        </div>
    </div>
</div>

<style>
    @import "../../styles/shared_reg_log.css";

    select {
        background-color: var(--background-dark);
        border: none;
        width: 20vw;
        height: 4vh;
        font-size: 100%;
        text-align: center;
        border-radius: 1vh;
        box-shadow: inset 0px 0px 20px #00000022;
    }
</style>
