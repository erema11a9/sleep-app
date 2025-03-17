<script lang="ts">
    import { goto } from "$app/navigation";

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

        await fetch("http://localhost:5000/api/login", {
            method: "POST",
            body: JSON.stringify(credentials),
            headers: { "Content-Type": "application/json" },
        });

        goto("/app");
    }
</script>

<a href="../">На главную</a>
<br />
<br />
<label for="nickname">Ваш никнейм</label>
<br />
<input type="text" name="nickname" id="nickname" bind:value={nickname} />
<br />
<br />
<label for="password">Ваш пароль</label>
<br />
<input
    type={passFieldType}
    name="password"
    id="password"
    bind:value={password}
/>
<input
    type="checkbox"
    name="showPassword"
    id="showPassword"
    onclick={togglePasswordVisibility}
/>
<br />
<br />

<button onclick={login}> Войти </button>
<br />
<p>Нет аккаунта? <a href="../sign-up">Зарегистрироваться</a></p>
