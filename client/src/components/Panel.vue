<template>

  <div>
    <b-container fluid>
      <b-row v-for="(row, i) of grid" :key="i">
        <b-col v-for="(data, j) of row" :key="j">

          <tile
            v-if="data.index"
            :ref="data.index"
            :index="data.index"
            :message="data.message"
            :fontSize="data.fontSize"
            :callback="tile_callback"
          >
          </tile>

        </b-col>
      </b-row>
    </b-container>
  </div>

</template>

<script>
import Tile from './Tile.vue'

export default {
  name: 'Panel',
  components: { Tile },
  props: {
    index: {
      type: String,
      required: false
    },
    callback: undefined
  },
  data: function () {
      return {
        grid: undefined
      }
  },
  methods: {
    tile_callback: function (data) {
      if (this.callback) {
        var message = {}
        message.panel_component = this
        message.tile_component = data.tile_component
        message.relative_click = data.relative_click
        this.callback(message)
      }
    },
    set_background_colors: function (colors) {
      if (this.grid) {
        for (var i = 0; i < colors.length; i++) {
          for (var j = 0; j < colors[i].length; j++) {
            if (this.grid[i][j].index) {
              var child = this.$refs[this.grid[i][j].index][0]
              child.set_background_color(colors[i][j])
            }
          }
        }
      }
    },
    set_background_images: function (images) {
      if (this.grid) {
        for (var i = 0; i < images.length; i++) {
          for (var j = 0; j < images[i].length; j++) {
            if (this.grid[i][j].index) {
              var child = this.$refs[this.grid[i][j].index][0]
              child.set_background_image(images[i][j])
            }
          }
        }
      }
    }
  }
}
</script>

<style>
/* global styles */
</style>

<style scoped>
/* local styles */
</style>
