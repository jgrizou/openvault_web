<template>
  <div
    ref="padcontinuous"
    class="padcontinuous"
    v-on:click="on_click"
  >
  </div>
</template>

<script>

export default {
  name: 'PadContinuous',
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      paused: false,
      awaiting_flash: false
    }
  },
  computed: {
    disabled: function () {
      return this.paused || this.awaiting_flash
    }
  },
  methods: {
    on_click: function (event) {
      // do not listen to clicks when pad is disabled
      if (this.disabled) {
          return
      }

      var elem_data = this.$refs.padcontinuous

      var elem_rect = elem_data.getBoundingClientRect()

      var relative_click = {}
      relative_click.x = (event.clientX - elem_rect.x) / elem_rect.width
      relative_click.y = (event.clientY - elem_rect.y) / elem_rect.height

      var click_info = {}
      click_info.relative_click = relative_click
      this.callback(click_info)

      // RIPPLE EFFECT

      // Get necessary variables
      var width           = elem_data.offsetWidth
      var height          = elem_data.offsetHeight
      var ripple_center_X = relative_click.x * width
      var ripple_center_Y = relative_click.y * height
      var radius          = width // in px

      // modified center for the rpi screen that is 90degree rotated
      // var ripple_center_X = (1 - relative_click.y) * width
      // var ripple_center_Y = relative_click.x * height

      //Ripple
      var rippleEffect = document.createElement("div");
      rippleEffect.className = 'ripple-effect';
      rippleEffect.style.left = ripple_center_X + "px";
      rippleEffect.style.top  = ripple_center_Y + "px";

      //rippleContainer
      var rippleContainer = document.createElement("div");
      rippleContainer.className = 'ripple-container';
      rippleContainer.appendChild(rippleEffect);
      rippleContainer.style.width   = width + "px";
      rippleContainer.style.height  = height + "px";

      elem_data.appendChild(rippleContainer);

      // timeout needed to ensure the previous is applied first
      setTimeout(function() {
           rippleEffect.style.left   = ripple_center_X - radius + "px";
           rippleEffect.style.top    = ripple_center_Y - radius + "px";
           rippleEffect.style.width  = radius * 2 + "px";
           rippleEffect.style.height = radius * 2 + "px";
       }, 0);

       setTimeout(function() {
           rippleEffect.style.backgroundColor = "rgba(0, 0, 0, 0)";
       }, 250);

       setTimeout(function() {
           rippleContainer.parentNode.removeChild(rippleContainer);
       }, 1000);
    }
  }
}

</script>

<style>
/* global styles */

.padcontinuous {
  background-color: rgba(255, 255, 255, 1);
}

.ripple-container {
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none;
    overflow: hidden;
}

.ripple-effect {
    position: relative;
    top: 0;
    left: 0;
    width: 0;
    height: 0;
    transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    background-color: rgba(0, 0, 0, 0.35);
}

</style>

<style scoped>
/* local styles */
</style>
