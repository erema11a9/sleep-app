<script lang="ts">
    import kitty404 from "./kitty404.jpg";
</script>

<div class="viewport">
    <div class="window">
        <div class="left-side">
            <h1 class="error-code">404</h1>
            <p>Как Вы тут оказались?</p>
            <a href="/">На главную</a>
        </div>
        <img src={kitty404} alt="404 cat" class="kitty" />
    </div>
</div>

<style>
    @import "../../styles/shared_global.css";

    .viewport {
        display: grid;
        place-items: center;
    }

    .window {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        background: linear-gradient(
            45deg,
            var(--background-dark),
            var(--background-dark-alt)
        );
        border-radius: 1em;
        box-shadow: 0px 0px 30px #00000044;
        overflow: hidden;
        height: 30vh;
    }

    .error-code {
        margin: 0;
        font-size: 5em;
        color: var(--error);
    }

    .left-side {
        display: grid;
        place-items: center;
        margin: 0 5vw;
    }

    p {
        margin: 2vh 0;
    }

    a {
        all: unset;
        background-color: transparent;
        border-width: 2px;
        border-style: solid;
        border-color: var(--foreground-dark);
        border-radius: 1vmax;
        padding: 1vh 1vw;
        font-size: 100%;
        text-align: center;
        cursor: pointer;
        margin: 1vh 0 0 0;
    }

    a:hover {
        background-color: rgba(224, 228, 255, 0.25);
    }

    .kitty {
        height: 30vh;
        width: 30vh;
    }
</style>
