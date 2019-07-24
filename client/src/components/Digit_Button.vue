<template>
  <div>

    <transition name="digit-button-appear">

      <div v-if="show">
        <div class="hide_digit"></div>
        <button
          class="digit_overlay_button noselect"
          v-on:click="on_click">
            <slot></slot>
        </button>
      </div>

    </transition>

  </div>
</template>

<script>

export default {
  name: "DigitButton",
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      show: false
    }
  },
  methods: {
    on_click: function () {
      this.callback()
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --digit_overlay_btn_margin_top: 15px;
  --digit_overlay_btn_margin_side: 60px;
  --digit_overlay_top: calc(var(--display_height) - var(--shadow_diff) + var(--digit_overlay_btn_margin_top));
  --digit_overlay_left: var(--digit_overlay_btn_margin_side);
  --digit_overlay_btn_width: calc(var(--screen_width) - 2*var(--digit_overlay_btn_margin_side));
  --digit_overlay_btn_height: calc(var(--digit_height) - 2*var(--digit_overlay_btn_margin_top));
}

.digit_overlay_button {
  position: absolute;
  top: var(--digit_overlay_top);
  left: var(--digit_overlay_left);
  width: var(--digit_overlay_btn_width);
  height: var(--digit_overlay_btn_height);
  outline: none; /* remove contour when clicked */
  border: none;
  border-radius: 30px;
  text-align: center;
  vertical-align: middle;
  font-size: 50px;
  font-weight: 600;
  color: rgba(50, 50, 50, 1);
  background-color: rgba(230, 230, 230, 1);
  box-shadow: 0 var(--shadow_full) rgba(150, 150, 150, 1);
}

.digit_overlay_button:active {
  color: rgba(0, 0, 0, 1);
  background-color: rgba(210, 210, 210, 1);
  box-shadow: 0 var(--shadow_min) rgba(100, 100, 100, 1);
  transform: translateY(var(--shadow_diff));
}

.hide_digit {
  position: absolute;
  top: var(--display_height);
  left: 0px;
  width: var(--screen_width);
  height: var(--digit_height);
  outline: none;
  border: none;
  background-color: rgba(255, 255, 255, 1);
}

.digit-button-appear-enter-active {
  transition: opacity 1s ease-out;
}

.digit-button-appear-leave-active {
  transition: opacity .5s ease-in-out;
}

.digit-button-appear-enter, .digit-button-appear-leave-to {
  opacity: 0;
}

</style>

<style scoped>
/* local styles */
</style>
