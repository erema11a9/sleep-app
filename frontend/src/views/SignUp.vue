<template>
  <div class="viewport">
    <div class="main-content">
      <div class="registration-container">
        <div class="registration-form-container">
          <h2 class="form-title">Создайте аккаунт</h2>
          <p class="form-subtitle">Начните путь к здоровому сну</p>

          <form @submit.prevent="submitForm">
            <!-- Никнейм -->
            <div class="form-group">
              <label for="nickname" class="form-label">Никнейм</label>
              <input type="text" id="nickname" v-model="formData.nickname" @blur="validateField('nickname')"
                :class="{ 'error': errors.nickname }" class="form-input" placeholder="Введите ваш ник" maxlength="16"
                required />
            </div>

            <!-- Дата рождения -->
            <div class="form-group">
              <label for="birthdate" class="form-label">Дата рождения</label>
              <input type="date" id="birthdate" v-model="formData.birthdate" @blur="validateField('birthdate')"
                :class="{ 'error': errors.birthdate }" class="form-input" required />
            </div>

            <!-- Пол -->
            <div class="form-group">
              <label class="form-label">Пол</label>
              <div class="gender-options">
                <label>
                  <input type="radio" name="gender" value="male" v-model="formData.gender" required /> Мужской
                </label>
                <label>
                  <input type="radio" name="gender" value="female" v-model="formData.gender" required /> Женский
                </label>
              </div>
            </div>

            <!-- Пароль -->
            <div class="form-group">
              <label for="password" class="form-label">Пароль</label>
              <div class="password-input-container">
                <input type="password" id="password" v-model="formData.password" @blur="validateField('password')"
                  :class="{ 'error': errors.password }" class="form-input" placeholder="Минимум 8 символов"
                  maxlength="16" required />
                <button type="button" @click="togglePasswordVisibility" class="toggle-password">👁️</button>
              </div>
            </div>

            <!-- Кнопка регистрации -->
            <button type="submit" class="btn" :class="{ 'btn-primary': isFormValid, 'btn-disabled': !isFormValid }"
              :disabled="!isFormValid">
              Создать аккаунт
            </button>

            <!-- Сообщение об ошибке -->
            <p v-if="formHasErrors" class="error-message">
              Пожалуйста, заполните все поля корректно!
            </p>
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
        nickname: '',
        birthdate: '',
        gender: '',
        password: '',
      },
      errors: {
        nickname: false,
        birthdate: false,
        password: false,
      },
      attemptedSubmit: false,
    };
  },
  computed: {
    isFormValid() {
      return (
        this.formData.nickname.length > 0 &&
        this.isValidAge &&
        this.formData.gender.length > 0 &&
        this.formData.password.length >= 8
      );
    },
    formHasErrors() {
      return Object.values(this.errors).some(error => error);
    },
    isValidAge() {
      if (!this.formData.birthdate) return false;
      const birthYear = new Date(this.formData.birthdate).getFullYear();
      const currentYear = new Date().getFullYear();
      const age = currentYear - birthYear;
      return age >= 12 && age <= 112;
    }
  },
  methods: {
    validateField(field) {
      if (field === 'password') {
        this.errors.password = this.formData.password.length < 8;
      } else if (field === 'birthdate') {
        this.errors.birthdate = !this.isValidAge;
      } else {
        this.errors[field] = this.formData[field].trim() === '';
      }
    },
    validateAllFields() {
      this.errors.nickname = this.formData.nickname.trim() === '';
      this.errors.birthdate = !this.isValidAge;
      this.errors.password = this.formData.password.length < 8;
    },
    submitForm() {
      this.attemptedSubmit = true;
      this.validateAllFields();

      if (!this.isFormValid) {
        console.log("Ошибка! Заполните все поля корректно.");
        return;
      }

      console.log("Регистрация успешна!", this.formData);
    },
    togglePasswordVisibility() {
      const passwordField = document.getElementById('password');
      passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
    },
    async sendDataToBackend() {
      const RESPONSE = await fetch("http://localhost:5000/api/users", {
        method: "POST",
        body: {

        }
      })

      if (RESPONSE.ok) {
        // ...
      }
    }
  },

};
</script>

<style scoped>
@import '@/styles/shared_global.css';
@import '@/styles/SignIn-style.css';
</style>
