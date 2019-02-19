<template lang="html">
  <div id="app">

    <panel ref="display" index="display" ></panel>
    <br>
    <panel ref="code" index="code"></panel>
    <br>
    <panel ref="pad" index="pad" :callback="pad_callback"></panel>

  </div>
</template>


<script>
import Panel from './../components/Panel.vue'

export default {
  name: 'V1',
  components: { Panel },
  data() {
    return {
    };
  },
  sockets: {
    connect: function () {
      console.log('## Socket connected')
    },
    disconnect: function () {
      console.log('## Socket disconnected')
    },
    grid: function (data) {
      var child = this.$refs[data.panel_index]
      child.grid = data.grid
    },
    colors: function (data) {
      var child = this.$refs[data.panel_index]
      child.set_background_colors(data.colors)
    }
  },
  methods: {
    pad_callback: function (data) {
      // data.tile_component.set_background_color("rgba(0, 0, 0, 0.5)")
      // data.tile_component.set_background_image("url(" + require('./../assets/sprite.png') + ")")

      var click_info = {}
      click_info.panel_index = data.panel_component.index
      click_info.tile_index = data.tile_component.index
      click_info.relative_click = data.relative_click
      this.$socket.emit('click', click_info)
    }
  },
  mounted() {
    window.addEventListener('keypress', (event) => {
      const key = String.fromCharCode(event.keyCode)
      this.$socket.emit('key', {'key': key})
    });
  }
}
</script>


<style>
/* global styles */

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

<style scoped>
/* local styles */
</style>
