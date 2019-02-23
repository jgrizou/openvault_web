<template>
  <div
    class="square"
    v-bind:ref="reference"
    v-bind:style="styleObject"
    v-on:click="on_click"
  >
    <div class="content">{{ message }}</div>
    <media
      :query="{maxWidth: maxWidthTrigger}"
      @media-enter="mediaEnter"
      @media-leave="mediaLeave"
    ></media>
  </div>
</template>

<script>
import Media from 'vue-media'

export default {
  name: 'Tile',
  components: { Media },
  props: {
    index: {
      type: String,
      required: true
    },
    styleDict: {
      type: Object,
      default : {
        "fontSize": "10vw",
        "maxFontSize": "30px",
        "background": "rgba(200, 200, 200, 1)",
        "isBackgroundImage": false,
        "maxWidthTrigger": 600
      }
    },
    message: {
      type: String,
      default: ""
    },
    callback: {
      type: Function,
      default: undefined
    }
  },
  data: function () {
      return {
        maxWidthTrigger: this.styleDict.maxWidthTrigger,
        greaterThanMaxWidth: window.innerWidth > this.styleDict.maxWidthTrigger
      }
  },
  computed: {
    styleObject: function () {
      var styleDict = {}
      if (this.greaterThanMaxWidth) {
        styleDict.fontSize = this.styleDict.maxFontSize
      } else {
        styleDict.fontSize = this.styleDict.fontSize
      }
      if (this.styleDict.isBackgroundImage) {
        styleDict.backgroundImage = this.styleDict.background
      } else {
        styleDict.background = this.styleDict.background
      }
      return styleDict
    },
    reference: function () {
      return this.index
    }
  },
  methods: {
    mediaEnter(mediaQueryString) {
      this.greaterThanMaxWidth = false
    },
    mediaLeave(mediaQueryString) {
      this.greaterThanMaxWidth = true
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

@media (min-width: 600px) {
  .square {
    font-size: 60px;
  }
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
