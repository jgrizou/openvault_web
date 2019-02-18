<template>
  <button class="cell" v-bind:class="classObject" v-on:click="click">
    {{ message }}
  </button>
</template>

<script>
export default {
  name: 'Toto',
  props: ['index', 'message'],
  data() {
    return {
      pressed: false
    };
  },
  computed: {
    classObject: function () {
      return {
        pressed: this.pressed
      }
    }
  },
  methods: {
    click: function (event) {
      this.$parent.sayHello(this.index)
    }
  }
}
</script>

<style>
/* global styles */

.cell {
  display: inline-block;
  border: none;
  outline: none;
  width: 100px;
  height: 100px;
  margin: 0;
  padding: 0;
  background: url("./../assets/test.png") no-repeat 0 -39px;
}
.cell:active {background-position: 0 -100px;}

</style>

<style scoped>
/* local styles */
</style>
