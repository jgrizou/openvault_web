<template>
  <div>
    <b-container fluid>
      <b-row v-for="(row, i) of grid" :key="i">
        <b-col v-for="(data, j) of row" :key="j">

          <tile
            v-if="data.index"
            v-bind:ref="data.index"
            v-bind:index="data.index"
            v-bind:message="data.message"
            v-bind:styleDict="data.style"
            v-bind:callback="tile_callback"
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
  computed: {
    status: function () {
      return !(this.grid === undefined)
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
