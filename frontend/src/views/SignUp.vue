<template>
  <div class="viewport">
    <div class="login-window">
      <div class="login-contents">
        <router-link to="/">
          <img :src="logo" alt="Logo" />
        </router-link>

        <div v-if="errorMessage" class="error-container">
          <p class="error-message">{{ errorMessage }}</p>
        </div>

        <div class="field">
          <label for="reg-nickname">Ваш никнейм</label>
          <input type="text" name="reg-nickname" id="reg-nickname" required v-model="nickname" placeholder="Никнейм" />
        </div>

        <div class="field">
          <label for="birthdate">Дата рождения</label>
          <input type="date" name="birthdate" id="birthdate" required :max="today" v-model="dateString" />
        </div>

        <div class="field">
          <label for="gender">Пол</label>
          <div class="radio-group">
            <label v-for="gender in genders" :key="gender.char">
              <input type="radio" name="gender" :value="gender.char" v-model="selectedGender" required />
              {{ gender.text }}
            </label>
          </div>
        </div>

        <div class="field">
          <label for="reg-password">Ваш пароль</label>
          <input :type="passFieldType" name="reg-password" id="reg-password" required minlength="8" maxlength="20"
            v-model="password" placeholder="Пароль" />
        </div>

        <p>
          <label class="checkbox">
            <input type="checkbox" name="showPassword" id="showPassword" @click="togglePasswordVisibility" />Показать
            пароль
          </label>
        </p>

        <button @click="register"> Регистрация </button>

        <p class="no-account">
          Уже есть аккаунт?
          <router-link to="../sign-in" class="no-account">Войти</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logo from '@/assets/logo_text.svg';
import { ref } from 'vue';
import { useRouter } from 'vue-router';


const router = useRouter();

function isAlphaNumeric(str: string) {
  var code, i, len;

  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);
    if (
      !(code > 47 && code < 58) &&
      !(code > 64 && code < 91) &&
      !(code > 96 && code < 123)
    ) {
      return false;
    }
  }
  return true;
}

const nickname = ref('');

const passFieldType = ref<'password' | 'text'>('password');
function togglePasswordVisibility() {
  passFieldType.value = passFieldType.value === 'password' ? 'text' : 'password';
}
const password = ref('');

const today = new Date().toISOString().substring(0, 10);
const dateString = ref(today);

const genders = ref([
  {
    char: 'm',
    text: 'Мужчина',
  },
  {
    char: 'f',
    text: 'Женщина',
  },
]);
const selectedGender = ref('');

const errorMessage = ref<string | null>(null);

function check(): boolean {
  errorMessage.value = null;

  if (!isAlphaNumeric(nickname.value)) {
    errorMessage.value = 'В никнейме могут быть только латинские буквы и цифры';
  } else if (nickname.value.length < 4) {
    errorMessage.value = 'Никнейм должен быть длиной 4 символа или больше';
  } else if (
    new Date(dateString.value).getFullYear() >
    new Date().getFullYear() - 2
  ) {
    errorMessage.value = 'Недействительная дата рождения';
  } else if (selectedGender.value === '') {
    errorMessage.value = 'Выберите пол';
  } else if (password.value.length < 8) {
    errorMessage.value = 'Пароль должен быть длиной 8 символов или больше';
  }

  if (errorMessage.value) {
    return false;
  }

  return true;
}

async function register() {
  if (!check()) {
    return;
  }

  const stuff = {
    nickname: nickname.value,
    password: password.value,
    birth_date: dateString.value,
    gender: selectedGender.value,
  };

  try {
    const RESPONSE = await fetch('http://localhost:5000/api/reg', {
      method: 'POST',
      body: JSON.stringify(stuff),
      headers: { 'Content-Type': 'application/json' },
    });

    if (RESPONSE.ok) {
      router.push('/app');
    } else {
      const errorData = await RESPONSE.json();
      errorMessage.value = errorData.message || 'Ошибка регистрации';
    }
  } catch (error: any) {
    errorMessage.value = 'Произошла ошибка при регистрации';
    console.error('Ошибка регистрации:', error);
  }
}
</script>

<style scoped>
@import '@/styles/shared_reg_log.css';

.radio-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>