<template>
    <div class="viewport">
        <header>
            <router-link to="/" class="logo">
                <img :src="logoIcon" alt="logo icon" class="logo-img" />
                <span class="logo-text">Sleepy</span>
            </router-link>
            <nav>
                <a href="/about-us" class="active">О нас</a>
            </nav>
            <div class="user-profile">
                <div class="user-avatar">A</div>
            </div>
        </header>

        <div class="main-content">
            <div class="dashboard">
                <div class="overview-section">
                    <h2 class="section-title">Обзор сна</h2>
                    <div class="stats-cards">
                        <div class="stat-card">
                            <div class="stat-title">Среднее время сна</div>
                            <div class="stat-value">{{ sleepStats.avg_hours || '0' }}ч</div>
                            <div class="stat-trend"
                                :class="{ 'trend-up': sleepStats.avg_hours_change > 0, 'trend-down': sleepStats.avg_hours_change < 0 }">
                                {{ sleepStats.avg_hours_change > 0 ? '+' : '' }}{{ sleepStats.avg_hours_change || '0'
                                }}ч
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-title">Качество сна</div>
                            <div class="stat-value">{{ sleepStats.quality || '0' }}%</div>
                            <div class="stat-trend"
                                :class="{ 'trend-up': sleepStats.quality_change > 0, 'trend-down': sleepStats.quality_change < 0 }">
                                {{ sleepStats.quality_change > 0 ? '+' : '' }}{{ sleepStats.quality_change || '0' }}%
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-title">Глубокий сон</div>
                            <div class="stat-value">{{ sleepStats.deep_sleep || '0' }}%</div>
                            <div class="stat-trend"
                                :class="{ 'trend-up': sleepStats.deep_sleep_change > 0, 'trend-down': sleepStats.deep_sleep_change < 0 }">
                                {{ sleepStats.deep_sleep_change > 0 ? '+' : '' }}{{ sleepStats.deep_sleep_change || '0'
                                }}%
                            </div>
                        </div>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-header">
                        <div class="chart-title">Длительность сна за неделю</div>
                        <div class="chart-legend">
                            <div class="legend-item"><span class="legend-color" style="background: #8b5cf6;"></span>
                                Глубокий сон</div>
                            <div class="legend-item"><span class="legend-color" style="background: #3b82f6;"></span>
                                Легкий сон</div>
                        </div>
                    </div>
                    <canvas id="sleepChart"></canvas>
                </div>

                <div class="recommendations">
                    <h2 class="section-title">Рекомендации по сну</h2>
                    <div class="recommendation-item" v-for="(rec, index) in recommendations" :key="index">
                        <div class="recommendation-icon">💡</div>
                        <div class="recommendation-text">
                            <div class="recommendation-title">{{ rec.title }}</div>
                            <div class="recommendation-desc">{{ rec.text }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="sidebar">
                <div class="profile-card">
                    <div class="profile-img">A</div>
                    <div class="profile-name">{{ user.nickname || 'Пользователь' }}</div>
                    <div class="profile-streak">Серия: {{ user.sleep_streak || '0 дней' }}</div>
                </div>

                <div class="chat-container">
                    <div class="chat-header">Консультант по сну</div>
                    <div class="chat-messages">
                        <div v-for="(message, index) in chatMessages" :key="index"
                            :class="['message', message.isUser ? 'message-outgoing' : 'message-incoming']">
                            <div class="message-bubble">{{ message.text }}</div>
                            <div class="message-time">{{ message.timestamp }}</div>
                        </div>
                    </div>
                    <div class="chat-input">
                        <input v-model="chatInput" type="text" placeholder="Задайте вопрос ИИ..."
                            @keyup.enter="sendMessage" />
                        <button @click="sendMessage"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                                xmlns="http://www.w3.org/2000/svg">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM13 10H16L12 14L8 10H11V7H13V10Z"
                                    fill="white" />
                            </svg></button>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <div class="copyright">
                <p>© 2025 Студенты 2ИТб-2: Дудин М., Еремин Д., Филиппов Д., Шевченко А.</p>
            </div>
            <div class="links">
                <a href="https://github.com/erema11a9/sleep-app">
                    <img :src="github" alt="github" class="icon" />
                </a>
                <a href="/">
                    <img :src="tg" alt="tg" class="icon" />
                </a>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
import logoIcon from '@/assets/logo.svg';
import logoText from '@/assets/logo_text.svg';
import github from '@/assets/github.svg';
import tg from '@/assets/tg.svg';

// Определение интерфейсов для типизации
interface User {
    nickname: string;
    sleep_streak: string;
}

interface SleepStats {
    avg_hours: number;
    avg_hours_change: number;
    quality: number;
    quality_change: number;
    deep_sleep: number;
    deep_sleep_change: number;
}

interface SleepDataItem {
    date: string;
    deep_sleep: number;
    light_sleep: number;
}

interface Recommendation {
    title: string;
    text: string;
}

interface ChatMessage {
    text: string;
    isUser: boolean;
    timestamp: string;
}

// Объявление переменных с ref
const user = ref<User>({
    nickname: 'Пользователь',
    sleep_streak: '7 дней',
});
const sleepStats = ref<SleepStats>({
    avg_hours: 7.2,
    avg_hours_change: 0.5,
    quality: 86,
    quality_change: 4,
    deep_sleep: 22,
    deep_sleep_change: -2,
});
const sleepData = ref<SleepDataItem[]>([
    { date: 'Пн', deep_sleep: 20, light_sleep: 80 },
    { date: 'Вт', deep_sleep: 22, light_sleep: 78 },
    { date: 'Ср', deep_sleep: 18, light_sleep: 82 },
    { date: 'Чт', deep_sleep: 25, light_sleep: 75 },
    { date: 'Пт', deep_sleep: 21, light_sleep: 79 },
    { date: 'Сб', deep_sleep: 23, light_sleep: 77 },
    { date: 'Вс', deep_sleep: 19, light_sleep: 81 },
]);
const recommendations = ref<Recommendation[]>([
    { title: 'Оптимальное время отхода ко сну', text: 'Попробуйте ложиться в 22:30, чтобы улучшить качество сна.' },
    { title: 'Напоминание о подготовке', text: 'Установите напоминание за 30 минут до сна.' },
    { title: 'Улучшение глубокого сна', text: 'Избегайте синего света перед сном.' },
]);
const chatMessages = ref<ChatMessage[]>([]);
const chatInput = ref<string>('');

onMounted(async () => {
    try {
        const userResponse = await fetch('http://localhost:5000/api/user', { headers: { 'Content-Type': 'application/json' } });
        if (userResponse.ok) user.value = await userResponse.json() as User;
    } catch (error) {
        console.error('Ошибка загрузки данных пользователя:', error);
    }

    try {
        const statsResponse = await fetch('http://localhost:5000/api/sleep-stats', { headers: { 'Content-Type': 'application/json' } });
        if (statsResponse.ok) sleepStats.value = await statsResponse.json() as SleepStats;
    } catch (error) {
        console.error('Ошибка загрузки статистики сна:', error);
    }

    try {
        const sleepResponse = await fetch('http://localhost:5000/api/sleep-data', { headers: { 'Content-Type': 'application/json' } });
        if (sleepResponse.ok) sleepData.value = await sleepResponse.json() as SleepDataItem[];
    } catch (error) {
        console.error('Ошибка загрузки данных сна:', error);
    }

    try {
        const recResponse = await fetch('http://localhost:5000/api/recommendations', { headers: { 'Content-Type': 'application/json' } });
        if (recResponse.ok) recommendations.value = await recResponse.json() as Recommendation[];
    } catch (error) {
        console.error('Ошибка загрузки рекомендаций:', error);
    }

    renderChart();
});

const renderChart = () => {
    const canvas = document.getElementById('sleepChart') as HTMLCanvasElement | null;
    const ctx = canvas?.getContext('2d');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sleepData.value.map(data => data.date),
                datasets: [
                    { label: 'Глубокий сон', data: sleepData.value.map(data => data.deep_sleep), backgroundColor: '#8b5cf6' },
                    { label: 'Легкий сон', data: sleepData.value.map(data => data.light_sleep), backgroundColor: '#3b82f6' },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } },
                plugins: { legend: { position: 'top' } },
            },
        });
    } else {
        console.error('Не удалось найти элемент canvas с id "sleepChart" или получить контекст 2D');
    }
};

const sendMessage = async () => {
    if (!chatInput.value.trim()) return;
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    chatMessages.value.push({ text: chatInput.value, isUser: true, timestamp });

    try {
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: chatInput.value }),
        });
        if (response.ok) {
            const data = await response.json();
            chatMessages.value.push({ text: data.response, isUser: false, timestamp });
        } else {
            chatMessages.value.push({ text: 'Ошибка: нет ответа от ИИ', isUser: false, timestamp });
        }
    } catch (error) {
        chatMessages.value.push({ text: 'Ошибка соединения', isUser: false, timestamp });
    }
    chatInput.value = '';
};
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Comfortaa', cursive;
}

body {
    background-color: #0f172a;
    color: #f8fafc;
    min-height: 100vh;
}

.viewport {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
    display: flex;
    align-items: center;
    gap: 16px;
}

.logo-img {
    width: 40px;
    height: 40px;
}

.logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(to right, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

nav {
    display: flex;
    gap: 32px;
}

nav a {
    color: #94a3b8;
    text-decoration: none;
    font-size: 16px;
    font-weight: 500;
    transition: color 0.2s;
}

nav a:hover {
    color: #f8fafc;
}

nav a.active {
    color: #8b5cf6;
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #8b5cf6;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 16px;
}

.main-content {
    display: grid;
    grid-template-columns: 1fr 350px;
    gap: 32px;
    margin: 40px 0;
    padding: 0;
    width: 100%;
    flex-grow: 1;
}

.dashboard {
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 0 24px;
}

.section-title {
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: 700;
}

.stats-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}

.stat-card {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-title {
    color: #94a3b8;
    font-size: 16px;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #f8fafc;
}

.stat-trend {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
}

.trend-up {
    color: #10b981;
}

.trend-down {
    color: #f59e0b;
}

.chart-container {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 16px;
    padding: 24px;
    height: 300px;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.chart-title {
    font-size: 20px;
    font-weight: 700;
}

.chart-legend {
    display: flex;
    gap: 20px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    color: #94a3b8;
}

.legend-color {
    width: 14px;
    height: 14px;
    border-radius: 4px;
}

.sidebar {
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 0 24px;
}

.profile-card {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.profile-img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(to right bottom, #8b5cf6, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    font-weight: 700;
}

.profile-name {
    font-size: 22px;
    font-weight: 700;
}

.profile-streak {
    background: rgba(139, 92, 246, 0.2);
    padding: 8px 16px;
    border-radius: 24px;
    font-size: 16px;
    color: #8b5cf6;
    display: flex;
    align-items: center;
    gap: 8px;
}

.chat-container {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    height: 400px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.chat-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: 700;
    font-size: 20px;
}

.chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.message {
    max-width: 85%;
}

.message-incoming {
    align-self: flex-start;
}

.message-outgoing {
    align-self: flex-end;
}

.message-bubble {
    padding: 16px 20px;
    border-radius: 20px;
    font-size: 16px;
}

.message-incoming .message-bubble {
    background-color: rgba(255, 255, 255, 0.1);
}

.message-outgoing .message-bubble {
    background: linear-gradient(to right, #8b5cf6, #3b82f6);
}

.message-time {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 6px;
    display: flex;
    justify-content: flex-end;
}

.chat-input {
    display: flex;
    padding: 16px;
    gap: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-input input {
    flex: 1;
    background-color: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 12px 20px;
    border-radius: 24px;
    color: #f8fafc;
    outline: none;
    font-size: 16px;
}

.chat-input button {
    background: linear-gradient(to right, #8b5cf6, #3b82f6);
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.chat-input button:hover {
    opacity: 0.9;
}

.recommendations {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.recommendation-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.recommendation-item:last-child {
    border-bottom: none;
}

.recommendation-icon {
    background-color: rgba(139, 92, 246, 0.2);
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8b5cf6;
    font-size: 20px;
}

.recommendation-text {
    flex: 1;
}

.recommendation-title {
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 6px;
}

.recommendation-desc {
    font-size: 16px;
    color: #94a3b8;
}

footer {
    display: flex;
    justify-content: space-between;
    padding: 16px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.copyright,
.links {
    font-size: 16px;
    color: #94a3b8;
}

.links a img {
    width: 28px;
    height: 28px;
    margin-left: 16px;
}

@media (max-width: 768px) {
    .main-content {
        grid-template-columns: 1fr;
    }

    .stats-cards {
        grid-template-columns: 1fr;
    }

    .dashboard,
    .sidebar {
        padding: 0 16px;
    }
}
</style>
