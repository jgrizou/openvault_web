<template>
  <div
    class="square"
    v-bind:style="styleObject"
    v-bind:ref="reference"
    v-on:click="on_click"
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
      default: "10vw"
    },
    message: {
      type: String,
      default: ""
    },
    callback: {
      type: Function,
      default: undefined
    },
    background: {
      type: String,
      default: "rgba(200, 200, 200, 1)"
    },
    isBackgroundImage: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
      return {
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
    },
    reference: function () {
      return this.index
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
    on_click: function (event) {
      if (this.callback) {
        // get position of pad
        var elem_data = this.$refs[this.reference].getBoundingClientRect()

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
  display: flex;
}

.square:after {
  content: "";
  display: flex;
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
