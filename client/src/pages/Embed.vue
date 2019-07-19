<template>

  <div class="resp-vault">
    <iframe class="resp-iframe"  src="http://127.0.0.1:1234/#/ui/level_7_visible_nocheck.json" allow="microphone"></iframe>
  </div>

</template>

<script>
export default {
  name: 'Embed',
}
</script>


<style>
/* global styles */

.resp-vault {
    position: relative;
    overflow: hidden;
    padding-top: 166.67%;
}

.resp-vault-hood {
    position: relative;
    overflow: hidden;
    padding-top: 83.34%;
}

.resp-iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 0;
}

</style>

<style scoped>
/* local styles */
</style>
