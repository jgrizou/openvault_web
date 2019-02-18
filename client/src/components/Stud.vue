<template>
  <button
    class="stud"
    v-on:click="onClick"
  >
  </button>
</template>

<script>
export default {
  name: 'Stud',
  props: ['index'],
  methods: {
    onClick: function () {
      // send info to callback in parent
      this.$parent.studCallback({index: this.index})
    }
  }
}
</script>

<style>
/* global styles */

.stud {
  display: inline-block;
  border: none;
  outline: none;
  width: 100px;
  height: 100px;
  margin: 0;
  padding: 0;
  background: url("./../assets/test.png") no-repeat 0 -39px;
}

.stud:active {
  background-position: 0 -100px;
}

</style>

<style scoped>
/* local styles */
</style>
