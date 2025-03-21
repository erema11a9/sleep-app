<template>
    <div class="container">
  
      <div class="main-content">
        <div class="registration-container">
          <div class="registration-form-container">
            <h2 class="form-title">Создайте аккаунт</h2>
            <p class="form-subtitle">Начните путь к здоровому сну</p>
  
            <form @submit.prevent="submitForm">
              <div class="form-group">
                <label for="full-name" class="form-label">Полное имя</label>
                <input
                  type="text"
                  id="full-name"
                  v-model="formData.fullName"
                  class="form-input"
                  placeholder="Введите ваше имя"
                  required
                />
              </div>
  
              <div class="form-group">
                <label for="email" class="form-label">Email адрес</label>
                <input
                  type="email"
                  id="email"
                  v-model="formData.email"
                  class="form-input"
                  placeholder="example@mail.com"
                  required
                />
              </div>
  
              <div class="form-group">
                <label for="password" class="form-label">Пароль</label>
                <div class="password-input-container">
                  <input
                    type="password"
                    id="password"
                    v-model="formData.password"
                    class="form-input"
                    placeholder="Минимум 8 символов"
                    required
                  />
                  <button type="button" @click="togglePasswordVisibility" class="toggle-password">👁️</button>
                </div>
              </div>
  
              <div class="checkbox-container">
                <input
                  type="checkbox"
                  id="terms"
                  v-model="formData.acceptTerms"
                  class="form-checkbox"
                  required
                />
                <label for="terms" class="checkbox-label">
                  Я принимаю <a href="#">Условия использования</a> и <a href="#">Политику конфиденциальности</a>
                </label>
              </div>
  
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="!isFormValid"
              >
                Создать аккаунт
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formData: {
          fullName: '',
          email: '',
          password: '',
          acceptTerms: false,
        },
      };
    },
    computed: {
      isFormValid() {
        return (
          this.formData.fullName &&
          this.formData.email &&
          this.formData.password.length >= 8 &&
          this.formData.acceptTerms
        );
      },
    },
    methods: {
      submitForm() {
        console.log(this.formData);
      },
      togglePasswordVisibility() {
        const passwordField = document.getElementById('password');
        passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
      },
    },
  };
  </script>
  
  <style scoped>
    @import '@/assets/SignIn-style.css';
  </style>
  