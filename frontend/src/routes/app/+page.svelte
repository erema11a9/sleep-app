<script lang="ts">
    let sleepStats = $state();

    let exampleStatsStuff = {
        user_id: 1,
        age: 20,
        gender: "m",
        sleep_quality: 10,
        bedtime: "22:00:00",
        wakeup_time: "06:30:00",
        daily_steps: "10000",
        calories_burned: "3000",
        physical_activity: "medium",
        dietary_habits: "healthy",
    };

    async function getStats() {
        const RESPONSE = await fetch("http://localhost:5000/api/sleep_stats", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        sleepStats = await RESPONSE.text();
    }

    let test: string = $state("");
    async function postStat() {
        const RESPONSE = await fetch("http://localhost:5000/api/sleep_stats", {
            method: "POST",
            body: JSON.stringify(exampleStatsStuff),
            headers: { "Content-Type": "application/json" },
        });

        if (RESPONSE) {
            test = "ok";
        }
    }
</script>

<p>
    хай. это само приложение, которое доступно только после регистрации или
    входа
</p>
<br />
<br />
<p>V жми чтоб добавить стату V</p>
<button onclick={postStat}>Добавить</button>
<br />
{test}
<p>V жми кнопку чтоб получить статы V</p>
<button onclick={getStats}>Получить</button>
<br />
<br />
{#if sleepStats}
    {sleepStats}
{/if}
