<template>
  <div
    class="square"
    v-bind:style="styleObject"
    v-bind:ref="'tile_' + index"
    v-on:click="on_click('tile_' + index, $event)"
  >
    <div class="content">{{ message }}</div>
  </div>
</template>

<script>
export default {
  name: 'Tile',
  props: {
    index: {
      type: String,
      required: true
    },
    fontSize: {
      type: String,
      default: "50px"
    },
    message: {
      type: String,
      default: ""
    },
    callback: undefined
  },
  data: function () {
      return {
          background: "rgba(220, 0, 0, 0.5)",
          isBackgroundImage: false
      }
  },
  computed: {
    styleObject: function () {
      var styleDict = {}
      styleDict.fontSize = this.fontSize
      if (this.isBackgroundImage) {
        styleDict.backgroundImage = this.background
      } else {
        styleDict.background = this.background
      }
      return styleDict
    }
  },
  methods: {
    set_background_color: function (newColorCSS) {
      this.isBackgroundImage = false
      this.background = newColorCSS
    },
    set_background_image: function (newImageLocation) {
      this.isBackgroundImage = true
      this.background = newImageLocation
    },
    on_click: function (ref, event) {
      if (this.callback) {
        // get position of pad
        var elem_data = this.$refs[ref].getBoundingClientRect()

        // compute relative position of click in pad
        var relative_click = {}
        relative_click.x = (event.clientX - elem_data.x) / elem_data.width
        relative_click.y = (event.clientY - elem_data.y) / elem_data.height

        // send info to callback
        this.callback({tile_component: this, relative_click: relative_click})
      }
    }
  }
}
</script>

<style>
/* global styles */

.square {
  border: 1px solid black;
  width: 100%;
  position: relative;
  background-size: 100% 100%;
}

.square:after {
  content: "";
  display: block;
  padding-bottom: 100%;
}

.content {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  width: 100%;
  height: 100%;
}

</style>

<style scoped>
/* local styles */
</style>
