<template lang="html">
  <div id="app">

    <b-container fluid>
      <b-row>
        <b-col></b-col>
        <b-col><tile ref="tile1" index="1" message="1" :callback="tileCallback"></tile></b-col>
        <b-col><tile ref="tile2" index="2" message="2" :callback="tileCallback"></tile></b-col>
        <b-col></b-col>
      </b-row>
    </b-container>

    <numberPanel ref="numberpanel"></numberPanel>

  </div>
</template>


<script>
import Tile from './../components/Tile.vue'
import NumberPanel from './../components/NumberPanel.vue'

export default {
  name: 'V1',
  components: { Tile, NumberPanel },
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
      console.log(data)
      var child = this.$refs.numberpanel
      child.grid = data.grid
    },
    newnumber: function (data) {
      console.log(data)
    }
  },
  methods: {
    tileCallback: function (data) {
      console.log(data)
      data.component.set_background_color("rgba(0, 0, 0, 0.5)")
      var child = this.$refs.tile2
      child.set_background_color("rgba(220, 0, 0, 0.5)")

      var click_info = {}
      click_info.index = data.component.index
      click_info.click = data.click
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
