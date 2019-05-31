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
  name: 'Pad12',
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
      button_color: ['noflash', 'flash']
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
    }
  }
}

</script>

<style>
/* global styles */

.btn-elongated {
  position: absolute;
  top: 50px;
  width: 195px;
  height: 350px;
  outline: none;
  border: none;
}

.btn-elongated-0 {
  left: 40px;
}

.btn-elongated-1 {
  right: 40px;
}

</style>

<style scoped>
/* local styles */
</style>
