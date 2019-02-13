<template lang="html">
  <div id="app">
    <h1>Hello Yo Parcel from Vue 📦 🚀 </h1>
    <p>{{ message }}</p>
    <span><button v-on:click="clickButton">Add 1</button></span>
  </div>
</template>

<script>
export default {
  name: 'app',
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
    }
  },
  mounted() {
    window.addEventListener('keypress', (event) => {
      const key = String.fromCharCode(event.keyCode)
      this.$socket.emit('emit_key', {'key': key})
    });
    window.addEventListener('click', (event) => {
      var click_data = {}
      click_data.clientX = event.clientX
      click_data.clientY = event.clientY
      this.$socket.emit('emit_click', {event: click_data})
    });
  }
}
</script>

<style lang="css">

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


</style>
