<template>
    <div class="container">
      <header>
        <a href="#" class="logo">
          <img src="@/assets/Logo.png" alt="Logo" class="logo-img" />
          <div class="logo-text">Sleep APP</div>
        </a>
  
        <nav>
          <a href="#">Главная</a>
          <a href="#">Возможности</a>
          <a href="#">Цены</a>
          <a href="#">Контакты</a>
        </nav>
      </header>
  
      <div class="main-content">
        <div class="registration-container">
          <div class="registration-ram">
  
            <div class="registration-content">
              <h2 class="registration-image-title">Улучшите качество своего сна уже сегодня</h2>
              <p class="registration-image-desc">Присоединяйтесь к тысячам пользователей, которые уже улучшили свой сон с помощью Sleep APP</p>
  
              <div class="registration-benefits">
                <div class="benefit-item" v-for="benefit in benefits" :key="benefit.text">
                  <div class="benefit-icon">
                    <span class="check-icon">✔</span>
                  </div>
                  <div class="benefit-text">{{ benefit.text }}</div>
                </div>
              </div>
            </div>
          </div>
  
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
                  :class="{'input-invalid': !isValidEmail}"
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
                    :class="{'input-invalid': !isValidPassword}"
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
        benefits: [
          { text: 'Персонализированные рекомендации для улучшения сна' },
          { text: 'Детальная аналитика циклов сна' },
          { text: 'Консультации со специалистами по сну' },
        ],
      };
    },
    computed: {
      isValidEmail() {
        const emailPattern = /^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$/;
        return emailPattern.test(this.formData.email);
      },
      isValidPassword() {
        return this.formData.password.length >= 8;
      },
      isFormValid() {
        return (
          this.formData.fullName &&
          this.isValidEmail &&
          this.isValidPassword &&
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
  @import './Style.css';
  </style>
  