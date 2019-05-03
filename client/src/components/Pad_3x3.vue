<template>
  <div>

    <div v-for="(color, index) in pad_color">

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
      paused: false,
      awaiting_flash: false,
      pad_color: ['neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral']
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

:root {
  --top_margin: 30px;
  --side_margin: 40px;
  --btn_grid_witdh: calc( (var(--screen_width) - 2*var(--side_margin) - 2*var(--btn_spacing)) / 3 + var(--btn_spacing));
  --btn_width: calc( var(--btn_grid_witdh) - var(--btn_spacing));
  --btn_height: calc( var(--btn_width) - var(--shadow_full))
}

.btn-square {
  position: absolute;
  width: var(--btn_width);
  height: var(--btn_height);
  outline: none; /* remove contour when clicked */
  border: none;
}

.btn-square-0 {
  top: calc( var(--top_margin) + 0*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 0*var(--btn_grid_witdh));
}

.btn-square-1 {
  top: calc( var(--top_margin) + 0*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 1*var(--btn_grid_witdh));
}

.btn-square-2 {
  top: calc( var(--top_margin) + 0*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 2*var(--btn_grid_witdh));
}

.btn-square-3 {
  top: calc( var(--top_margin) + 1*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 0*var(--btn_grid_witdh));
}

.btn-square-4 {
  top: calc( var(--top_margin) + 1*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 1*var(--btn_grid_witdh));
}

.btn-square-5 {
  top: calc( var(--top_margin) + 1*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 2*var(--btn_grid_witdh));
}

.btn-square-6 {
  top: calc( var(--top_margin) + 2*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 0*var(--btn_grid_witdh));
}

.btn-square-7 {
  top: calc( var(--top_margin) + 2*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 1*var(--btn_grid_witdh));
}

.btn-square-8 {
  top: calc( var(--top_margin) + 2*var(--btn_grid_witdh));
  left: calc( var(--side_margin) + 2*var(--btn_grid_witdh));
}

</style>

<style scoped>
/* local styles */
</style>
