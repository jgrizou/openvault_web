<template>
  <div>
    <div v-for="(color, index) in button_color">

      <button
        :class="{
          'btn btn-elongated': true,
          ['btn-elongated-' + index]: true,
          [color]: true
          }"
        :disabled="disabled"
        v-on:click="on_click(index.toString())">
      </button>

    </div>

  </div>
</template>

<script>

export default {
  name: 'Pad12Random',
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      paused: false,
      awaiting_flash: false,
      button_color: ['noflash', 'flash'],
      button_color_1: ['noflash', 'flash'],
      button_color_2: ['flash', 'noflash'],
    }
  },
  computed: {
    disabled: function () {
      return this.paused || this.awaiting_flash
    }
  },
  methods: {
    on_click: function (button_name, event) {
      var click_info = {}
      click_info.button = button_name
      this.callback(click_info)
      this.toggle_button_color()
    },
    toggle_button_color: function () {
      if (this.button_color === this.button_color_2) {
        this.button_color = this.button_color_1
      } else {
        this.button_color = this.button_color_2
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
