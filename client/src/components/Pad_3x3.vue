<template>
  <div>

    <div v-for="(color, index) in button_color">

      <button
        :class="{
          'btn btn-square': true,
          ['btn-square-' + index]: true,
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
  name: 'Pad33',
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      stopped: false,
      paused: false,
      awaiting_flash: false,
      awaiting_pad: false,
      button_color: ['neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral']
    }
  },
  computed: {
    disabled: function () {
      return this.stopped || this.paused || this.awaiting_flash || this.awaiting_pad
    },
    is_clean: function () {
      return true
    }
  },
  methods: {
    clean_pad: function () {
      this.stopped = false
      this.paused = false
      this.awaiting_flash = false
      this.awaiting_pad = false
    },
    on_click: function (button_name, event) {
      var click_info = {}
      click_info.button = button_name
      this.callback(click_info)
    },
    update_pad_info: function (pad_info) {
      if (pad_info.button_color) {
          this.button_color = pad_info.button_color
      }
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --btn_3x3_top_margin: 30px;
  --btn_3x3_grid_witdh: calc( (var(--screen_width) - 2*var(--btn_side_margin) - 2*var(--btn_spacing)) / 3 + var(--btn_spacing));
  --btn_3x3_width: calc( var(--btn_3x3_grid_witdh) - var(--btn_spacing));
  --btn_3x3_height: calc( var(--btn_3x3_width) - var(--shadow_full))
}

.btn-square {
  position: absolute;
  width: var(--btn_3x3_width);
  height: var(--btn_3x3_height);
}

.btn-square-0 {
  top: calc( var(--btn_3x3_top_margin) + 0*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 0*var(--btn_3x3_grid_witdh));
}

.btn-square-1 {
  top: calc( var(--btn_3x3_top_margin) + 0*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 1*var(--btn_3x3_grid_witdh));
}

.btn-square-2 {
  top: calc( var(--btn_3x3_top_margin) + 0*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 2*var(--btn_3x3_grid_witdh));
}

.btn-square-3 {
  top: calc( var(--btn_3x3_top_margin) + 1*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 0*var(--btn_3x3_grid_witdh));
}

.btn-square-4 {
  top: calc( var(--btn_3x3_top_margin) + 1*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 1*var(--btn_3x3_grid_witdh));
}

.btn-square-5 {
  top: calc( var(--btn_3x3_top_margin) + 1*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 2*var(--btn_3x3_grid_witdh));
}

.btn-square-6 {
  top: calc( var(--btn_3x3_top_margin) + 2*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 0*var(--btn_3x3_grid_witdh));
}

.btn-square-7 {
  top: calc( var(--btn_3x3_top_margin) + 2*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 1*var(--btn_3x3_grid_witdh));
}

.btn-square-8 {
  top: calc( var(--btn_3x3_top_margin) + 2*var(--btn_3x3_grid_witdh));
  left: calc( var(--btn_side_margin) + 2*var(--btn_3x3_grid_witdh));
}

</style>

<style scoped>
/* local styles */
</style>
