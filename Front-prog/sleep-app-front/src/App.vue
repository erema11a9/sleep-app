<template>
  <div id="app">
    <router-view />

  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
 html { 
  background: linear-gradient(100deg, #0F172A, #0c255f);
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
