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
                        <button @click="sendMessage">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                                xmlns="http://www.w3.org/2000/svg">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM13 10H16L12 14L8 10H11V7H13V10Z"
                                    fill="white" />
                            </svg>
                        </button>
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

.viewport {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    width: 100%;
    background: #0f172a;
    overflow-x: hidden;
}

header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-wrap: wrap;
    gap: 1rem;
    width: 100%;
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    margin-left: 2rem;
}

.logo-img {
    width: 2.5rem;
    height: 2.5rem;
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
    gap: 1.5rem;
    align-items: center;
}

nav a {
    color: #94a3b8;
    text-decoration: none;
    font-size: 1rem;
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
    gap: 0.75rem;
    margin-right: 2rem;
}

.user-avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: #8b5cf6;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1rem;
    color: #fff;
}

.main-content {
    display: grid;
    grid-template-columns: 1fr minmax(18rem, 22rem);
    gap: 2rem;
    margin: 2rem auto;
    flex-grow: 1;
    max-width: 1200px;
    width: 100%;
}

.dashboard {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #f8fafc;
}

.stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
    gap: 1.5rem;
}

.stat-card {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-title {
    color: #94a3b8;
    font-size: 1rem;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
}

.stat-trend {
    font-size: 1rem;
}

.trend-up {
    color: #10b981;
}

.trend-down {
    color: #f59e0b;
}

.chart-container {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 1rem;
    padding: 1.5rem;
    height: 18rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.chart-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
}

.chart-legend {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #94a3b8;
}

.legend-color {
    width: 0.875rem;
    height: 0.875rem;
    border-radius: 0.25rem;
}

.recommendations {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.recommendation-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.recommendation-item:last-child {
    border-bottom: none;
}

.recommendation-icon {
    background: rgba(139, 92, 246, 0.2);
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8b5cf6;
    font-size: 1.25rem;
}

.recommendation-text {
    flex: 1;
}

.recommendation-title {
    font-weight: 700;
    font-size: 1.125rem;
    margin-bottom: 0.375rem;
    color: #f8fafc;
}

.recommendation-desc {
    font-size: 1rem;
    color: #94a3b8;
}

.sidebar {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
}

.profile-card {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.profile-img {
    width: 25%;
    aspect-ratio: 1/1;
    border-radius: 50%;
    background: linear-gradient(to right bottom, #8b5cf6, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: #fff;
}

.profile-name {
    font-size: 1.375rem;
    font-weight: 700;
    color: #f8fafc;
}

.profile-streak {
    background: rgba(139, 92, 246, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 1.5rem;
    font-size: 1rem;
    color: #8b5cf6;
}

.chat-container {
    background: linear-gradient(45deg, #1e293b, #1e293b);
    border-radius: 1rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    max-height: 25rem;
}

.chat-header {
    padding: 1.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: 700;
    font-size: 1.25rem;
    color: #f8fafc;
}

.chat-messages {
    flex: 1;
    padding: 1.25rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
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
    padding: 1rem 1.25rem;
    border-radius: 1.25rem;
    font-size: 1rem;
}

.message-incoming .message-bubble {
    background: rgba(255, 255, 255, 0.1);
    color: #f8fafc;
}

.message-outgoing .message-bubble {
    background: linear-gradient(to right, #8b5cf6, #3b82f6);
    color: #fff;
}

.message-time {
    font-size: 0.875rem;
    color: #94a3b8;
    margin-top: 0.375rem;
    display: flex;
    justify-content: flex-end;
}

.chat-input {
    display: flex;
    padding: 1rem;
    gap: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-input input {
    flex: 1;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.75rem 1.25rem;
    border-radius: 1.5rem;
    color: #f8fafc;
    outline: none;
    font-size: 1rem;
}

.chat-input button {
    background: linear-gradient(to right, #8b5cf6, #3b82f6);
    border: none;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.chat-input button:hover {
    opacity: 0.9;
}

footer {
    display: flex;
    justify-content: space-between;
    padding: 1rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    flex-wrap: wrap;
    gap: 1rem;
    width: 100%;
}

.copyright {
    font-size: 1rem;
    color: #94a3b8;
    margin-left: 2rem;
}

.links {
    font-size: 1rem;
    color: #94a3b8;
    margin-right: 2rem;
}

.links a img {
    width: 1.75rem;
    height: 1.75rem;
    margin-left: 1rem;
}

/* Адаптивность */
@media (max-width: 1024px) {
    .main-content {
        grid-template-columns: 1fr;
    }

    .sidebar {
        padding: 0;
    }
}

@media (max-width: 768px) {
    header {
        padding: 0.75rem 0;
    }

    .logo {
        margin-left: 1rem;
    }

    .logo-img {
        width: 2rem;
        height: 2rem;
    }

    .logo-text {
        font-size: 1.25rem;
    }

    nav {
        gap: 1rem;
    }

    nav a {
        font-size: 0.9rem;
    }

    .user-profile {
        margin-right: 1rem;
    }

    .user-avatar {
        width: 2rem;
        height: 2rem;
        font-size: 0.9rem;
    }

    .main-content {
        margin: 1rem 0;
        padding: 0;
    }

    .stats-cards {
        grid-template-columns: 1fr;
    }

    .section-title {
        font-size: 1.25rem;
    }

    .stat-card {
        padding: 1rem;
    }

    .stat-value {
        font-size: 1.5rem;
    }

    .chart-container {
        height: 15rem;
    }

    .chart-title {
        font-size: 1.1rem;
    }

    .legend-item {
        font-size: 0.8rem;
    }

    .profile-img {
        width: 20%;
        font-size: 2rem;
    }

    .profile-name {
        font-size: 1.2rem;
    }

    .profile-streak {
        font-size: 0.9rem;
    }

    .chat-container {
        max-height: 20rem;
    }

    .chat-header {
        font-size: 1.1rem;
    }

    .copyright {
        margin-left: 1rem;
    }

    .links {
        margin-right: 1rem;
    }

    footer {
        padding: 0.75rem 0;
    }
}

@media (max-width: 480px) {
    .logo {
        margin-left: 0.5rem;
    }

    .logo-text {
        font-size: 1rem;
    }

    nav a {
        font-size: 0.8rem;
    }

    .user-profile {
        margin-right: 0.5rem;
    }

    .section-title {
        font-size: 1.1rem;
    }

    .stat-card {
        padding: 0.75rem;
    }

    .stat-title {
        font-size: 0.9rem;
    }

    .stat-value {
        font-size: 1.25rem;
    }

    .stat-trend {
        font-size: 0.9rem;
    }

    .recommendation-title {
        font-size: 1rem;
    }

    .recommendation-desc {
        font-size: 0.9rem;
    }

    .recommendation-icon {
        width: 2rem;
        height: 2rem;
        font-size: 1rem;
    }

    .chat-input input {
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
    }

    .chat-input button {
        width: 2rem;
        height: 2rem;
    }

    .chat-input button svg {
        width: 1rem;
        height: 1rem;
    }

    .copyright {
        margin-left: 0.5rem;
    }

    .links {
        margin-right: 0.5rem;
    }

    .copyright,
    .links {
        font-size: 0.9rem;
    }

    .links a img {
        width: 1.5rem;
        height: 1.5rem;
    }
}
</style>
