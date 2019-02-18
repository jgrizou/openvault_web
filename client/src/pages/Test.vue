<template lang="html">
  <div id="app">

    <h1>Hello Yo Parcel from Vue 📦 🚀 </h1>
    <p>{{ message }}</p>
    <b-button v-on:click="clickButton">Add 1</b-button>

    <b-container fluid>
      <b-row>
        <b-col><tile index="stud1" :callback="this.studCallback"></tile></b-col>
        <b-col><tile index="stud2" :callback="this.studCallback"></tile></b-col>
      </b-row>
    </b-container>

    <b-container fluid>
      <b-row>
        <b-col></b-col>
        <b-col><tile ref="tile1" key="1" message="1" :callback="this.tileCallback"></tile></b-col>
        <b-col><tile ref="tile2" index="2" message="2" :callback="this.tileCallback"></tile></b-col>
        <b-col></b-col>
      </b-row>
    </b-container>

    <b-container fluid>
      <b-row>
        <b-col></b-col>
        <b-col><tile index="pad1" :callback="this.padCallback"></tile></b-col>
        <b-col><tile index="pad2" :callback="this.padCallback"></tile></b-col>
        <b-col></b-col>
      </b-row>
    </b-container>

  </div>
</template>


<script>
import Stud from './../components/Stud.vue'
import Pad from './../components/Pad.vue'
import Tile from './../components/Tile.vue'

export default {
  name: 'Test',
  components: { Stud, Pad, Tile},
  data() {
    return {
      message: 'Connecting...',
      cnt: 0
    };
  },
  sockets: {
    connect: function () {
      console.log('socket connected')
      this.message = 'I\'m connected!'
      this.$socket.emit('receive', { message: this.message, cnt: this.cnt })
    },
    response: function (data) {
      console.log(data)
      this.message = data.message
      this.cnt = data.cnt
    }
  },
  methods: {
    clickButton: function () {
      this.$socket.emit('receive', { message: new Date().getTime(), cnt: this.cnt + 1 })
    },
    studCallback: function (data) {
      console.log(data)
      // this.$socket.emit('emit_hello', data)
      var child = this.$refs.tile1
      child.set_background_image("url(" + require("./../assets/test.png") + ")")
    },
    padCallback: function (data) {
      console.log(data)
      // this.$socket.emit('emit_click', data)
      var child = this.$refs.tile1
      child.set_background_color("rgba(220, 0, 0, 0.5)")
    },
    tileCallback: function (data) {
      console.log(data)
      data.component.set_background_color("rgba(0, 0, 0, 0.5)")
      // this.$socket.emit('emit_click', data)
    }
  },
  mounted() {
    window.addEventListener('keypress', (event) => {
      const key = String.fromCharCode(event.keyCode)
      this.$socket.emit('emit_key', {'key': key})
    });
    // window.addEventListener('click', (event) => {
    //   var click_data = {}
    //   click_data.clientX = event.clientX
    //   click_data.clientY = event.clientY
    //   this.$socket.emit('emit_click', {event: click_data})
    // });
  }
}
</script>


<style>
/* global styles */
</style>

<style scoped>
/* local styles */

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol';
}

#app {
  text-align: center;
}

h1 {
  font-weight: 300;
}

.container {
  border: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.row {
  border: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.col {
  border: none;
  outline: none;
  margin: 0;
  padding: 0;
}

</style>
