<template>
  <div>

    <panel ref="display" index="display" ></panel>
    <br>
    <panel ref="code" index="code"></panel>
    <br>
    <panel ref="pad" index="pad" :callback="pad_callback"></panel>
    <br>

    <b-container class="text-center" fluid>
      <b-row>
        <b-col>
            <b-button v-on:click="reset">Reset</b-button>
            <router-link :to="{ name: 'LevelSelection'}">
              <b-button>Back to selection</b-button>
            </router-link>
        </b-col>
      </b-row>
    </b-container>

  </div>
</template>

<script>
import Panel from './../components/Panel.vue'

export default {
  name: 'PasswordUI',
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
    },
    status: function () {
      var status = true
      status = this.$refs.display.status
      status = this.$refs.code.status
      status = this.$refs.pad.status
      this.$socket.emit('status', status)
    }
  },
  methods: {
    reset: function () {
      this.$socket.emit('reset')
    },
    pad_callback: function (data) {
      // data.tile_component.set_background_color("rgba(0, 0, 0, 0.5)")
      // data.tile_component.set_background_image("url(" + require('./../assets/sprite.png') + ")")

      var click_info = {}
      click_info.panel_index = data.panel_component.index
      click_info.tile_index = data.tile_component.index
      click_info.relative_click = data.relative_click
      click_info.display_colors = this.$refs.display.colors
      this.$socket.emit('click', click_info)
    }
  },
  mounted() {
    window.addEventListener('keypress', (event) => {
      var key_info = {}
      key_info.key = String.fromCharCode(event.keyCode)
      key_info.display_colors = this.$refs.display.colors
      this.$socket.emit('key', key_info)
    });
    // spawn the learner given link given in url
    this.$socket.emit('spawn_learner', this.$route.params.pathMatch)
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
