<script lang="ts">
    import { goto } from "$app/navigation";

    let nickname: string = $state("");

    let passFieldType: "password" | "text" = $state("password");
    function togglePasswordVisibility() {
        passFieldType = passFieldType === "password" ? "text" : "password";
    }
    let password: string = $state("");

    let dateString: string = $state("");

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
    let selectedGender: string = $state("m");

    async function register() {
        let stuff = {
            nickname,
            password,
            birth_date: dateString,
            gender: selectedGender,
        };

        await fetch("http://localhost:5000/api/reg", {
            method: "POST",
            body: JSON.stringify(stuff),
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
<label for="birthdate">Дата рождения</label>
<br />
<input type="date" name="birthdate" id="birthdate" bind:value={dateString} />
{dateString}
<br />
<br />
<label for="gender">Пол</label>
<br />
<select name="gender" id="gender" bind:value={selectedGender}>
    {#each genders as gender}
        <option value={gender.char}>
            {gender.text}
        </option>
    {/each}
</select>
{selectedGender}
<br />
<br />
<button onclick={register}> Зарегистрироваться </button>
<br />
<p>Уже есть аккаунт? <a href="../sign-in">Войти</a></p>
