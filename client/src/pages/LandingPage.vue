<template>
  <iframe
    class="iframe-fullpage"
    src="https://jgrizou.com/projects/vault/quickaccess/"
  >
  </iframe>
</template>


<script>
export default {
  name: 'LandingPage',
}
</script>


<style>
/* global styles */

.iframe-fullpage{
  position: fixed;
  top: 0px;
  bottom: 0px;
  right: 0px;
  width: 100%;
  border: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  z-index: 999999;
  height: 100%;
}

</style>

<style scoped>
/* local styles */
</style>
