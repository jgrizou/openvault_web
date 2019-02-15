<template lang="html">
  <div id="container">

    <div v-for="(result, index) in data" :key="index">

        <input type="text" v-model="result.name">

        <b-button v-on:click="clickButton(result)">Send</b-button>

        <div class="square" :ref="'element' + result.id" v-on:click="clickEvent('element' + result.id, result, $event)">
            <h1>This is a Square</h1>
        </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      data: [{id: 1, name: ''}, {id: 2, name: ''}, {id: 3, name: ''}]
    };
  },
  methods: {
    clickButton: function (result) {
      console.log(result)
      console.log('The value of input is:', result.name)
      this.$socket.emit('input_value', result)
    },
    clickEvent: function (ref, result, event) {
      var elem_data = this.$refs[ref][0].getBoundingClientRect()

      var click_data = {}
      click_data.x = event.clientX
      click_data.y = event.clientY

      var rel_data = {}
      rel_data.x = (click_data.x - elem_data.x) / elem_data.width
      rel_data.y = (click_data.y - elem_data.y) / elem_data.height

      this.$socket.emit('emit_click', {event: rel_data, data: result})
    }
  },
  mounted() {
    console.log(this.$refs);
  }
}
</script>

<style>
/* global styles */
</style>

<style scoped>
/* local styles */

.square {
    background: url("./../assets/test.png");
    width: 50vw;
    height: 50vw;
}

</style>
