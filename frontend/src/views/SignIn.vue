<template>
    <div class="viewport">
        <Transition name="fade">
            <div v-if="true" class="login-window">
                <div class="login-contents">
                    <a href="/"><img :src="logo" alt="Logo" /></a>

                    <div v-if="errorMessage" class="error-container">
                        <p class="error-message">{{ errorMessage }}</p>
                    </div>

                    <div class="field">
                        <label for="nickname">Ваш никнейм</label>
                        <input v-model="nickname" type="text" name="nickname" id="nickname" placeholder="Никнейм" />
                    </div>

                    <div class="field">
                        <label for="password">Ваш пароль</label>
                        <input v-model="password" :type="passFieldType" name="password" id="password"
                            placeholder="Пароль" />
                    </div>

                    <p>
                        <label class="checkbox">
                            <input v-model="showPassword" type="checkbox" name="showPassword" id="showPassword" />
                            Показать пароль
                        </label>
                    </p>

                    <button @click="login"> Войти </button>

                    <p class="no-account">
                        Нет аккаунта? <a href="../sign-up" class="no-account">Зарегистрироваться</a>
                    </p>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import logo from "@/assets/logo_text.svg";

const router = useRouter();

const token = ref("");
onMounted(() => {
    token.value = localStorage.getItem("token") || "";
});

const nickname = ref("");
const password = ref("");
const showPassword = ref(false);
const errorMessage = ref("");

const passFieldType = computed(() => (showPassword.value ? "text" : "password"));

async function login() {
    try {
        const response = await fetch("http://localhost:5000/api/login", {
            method: "POST",
            body: JSON.stringify({ nickname: nickname.value, password: password.value }),
            headers: { "Content-Type": "application/json" },
        });

        if (response.ok) {
            const data = await response.json();
            token.value = data.access_token;
            localStorage.setItem("token", token.value);
            router.push("/account");
        } else {
            errorMessage.value = "Проверьте логин или пароль.";
        }
    } catch (error) {
        errorMessage.value = "Ошибка соединения.";
    }
}
</script>

<style scoped>
@import "@/styles/shared_reg_log.css";

.fade-enter-active,
.fade-leave-active {
    transition: opacity 1s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>