<template lang="html">
  <div id="app">
    <h1>Hello Yo Parcel from Vue 📦 🚀 {{ message }}</h1>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      message: 'custom message'
    };
  },
  sockets: {
    connect: function () {
      console.log('socket connected')
      this.message = 'I\'m connected!'
      this.$socket.emit('receive', { message: this.message, cnt: 0 })
    },
    response: function (data) {
      console.log(data)
      this.message = data.message
      this.$socket.emit('receive', { message: new Date().getTime(), cnt: data.cnt + 1 })
    }
  },
  methods: {
    clickButton: function (data) {
      this.$socket.emit('emit_method', data)
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
      click_data.screenX = event.screenX
      click_data.screenY = event.screenY
      this.$socket.emit('emit_click', {event: click_data})
    });
  }
}
</script>

<style lang="css">
html,
body {
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol';
}

#app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

h1 {
  font-weight: 300;
}
</style>
