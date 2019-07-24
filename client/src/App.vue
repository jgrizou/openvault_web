<template>
  <div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>

/* for mobile disabling the refresh on drawing down the screen, see https://w3bits.com/prevent-chrome-pull-to-refresh-css/*/

.body,
.wrapper {
  /* Break the flow */
  position: absolute;
  top: 0px;

  /* Give them all the available space */
  width: 100%;
  height: 100%;

  /* Remove the margins if any */
  margin: 0;

  /* Allow them to scroll down the document */
  overflow-y: hidden;
}

.body {
  /* Sending body at the bottom of the stack */
  z-index: -2;
}

.wrapper {
  /* Making the wrapper stack above the body */
  z-index: -1;
}

</style>
