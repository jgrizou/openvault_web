<template>

  <div>
    <b-container fluid>
      <b-row v-for="(row, i) of grid" :key="i">
        <b-col v-for="(data, j) of row" :key="j">

          <tile
            v-if="data.index"
            :ref="data.ref"
            :index="data.index"
            :message="data.message"
            :callback="tileCallback"
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
  name: 'NumberPanel',
  components: { Tile },
  data: function () {
      return {
        grid: [],
        colors: undefined
      }
  },
  computed: {
  },
  watch: {

  },
  methods: {
    tileCallback: function (data) {
      console.log(data.component.index)
      console.log(data.click)

      // this.grid = [
      //   [{}, {index: "4", ref: "4"}, {}],
      //   [{index: "1", ref: "1"}]
      // ],

      // this.colors = [
      //   [undefined, "red", undefined],
      //   ["black"]
      // ]

      console.log(this.grid)

    },
    setColors: function (colors) {
      this.colors = colors
      for (var i = 0; i < this.colors.length; i++) {
        for (var j = 0; j < this.colors[i].length; j++) {
          if (this.grid[i][j].ref) {
            var child = this.$refs[this.grid[i][j].ref][0]
            child.set_background_color(this.colors[i][j])
          }
        }
      }
    }
  },
  mounted() {
    console.log('mounted')
    this.colors = [
      [undefined, "red", "red", undefined],
      ["black", "black"]
    ]
  }
}
</script>

<style>
/* global styles */
</style>

<style scoped>
/* local styles */
</style>
