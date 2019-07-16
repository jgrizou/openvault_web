<template>
  <div
    ref="padtouch"
    class="padtouch"
    v-on:click="on_click"
  >

    <div
      ref="padborder"
      class="padborder"
    ></div>

  </div>
</template>

<script>

export default {
  name: 'PadTouch',
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
      click_history_location: [],
      click_history_color: [],
      click_history_container: undefined,
      classifier_map: undefined
    }
  },
  computed: {
    disabled: function () {
      return this.stopped || this.paused || this.awaiting_flash || this.awaiting_pad
    },
    is_clean: function () {
      return this.click_history_location.length == 0
    }
  },
  methods: {
    clean_pad: function () {
      this.stopped = false
      this.paused = false
      this.awaiting_flash = false
      this.awaiting_pad = false

      this.click_history_location = []
      this.click_history_color = []

      var pad_elem = this.$refs.padtouch
      if (this.click_history_container) {
        pad_elem.removeChild(this.click_history_container);
      }
      this.click_history_container = undefined
      this.classifier_map = undefined
    },
    on_click: function (event) {
      // do not listen to clicks when pad is disabled
      if (this.disabled) {
          return
      }

      var pad_elem = this.$refs.padtouch

      var pad_rect = pad_elem.getBoundingClientRect()

      var relative_click = {}
      relative_click.x = (event.clientX - pad_rect.x) / pad_rect.width
      relative_click.y = (event.clientY - pad_rect.y) / pad_rect.height

      var click_info = {}
      click_info.relative_click = relative_click
      this.callback(click_info)

      // save location
      this.click_history_location.push(relative_click)
      this.click_history_color.push('neutral')

      this.show_click_history()

      // RIPPLE EFFECT
      this.trigger_ripple(relative_click)

    },
    update_pad_info: function (pad_info) {
      if (pad_info.signal_color) {
          this.click_history_color = pad_info.signal_color
      }
      if (pad_info.classifier_map) {
          this.classifier_map = pad_info.classifier_map
      }
      this.show_click_history()
    },
    show_click_history: function () {
      var pad_elem = this.$refs.padtouch
      var pad_width = pad_elem.offsetWidth
      var pad_height = pad_elem.offsetHeight

      // new container
      var historyContainer = document.createElement("div");
      historyContainer.className = 'history-container';
      historyContainer.style.width   = pad_width + "px";
      historyContainer.style.height  = pad_height + "px";

      if (this.classifier_map) {
          historyContainer.innerHTML = '<img src="' + this.classifier_map + '") class="map-container" alt=""/>'
      }

      // add points one by one
      this.click_history_location.forEach( (click, index, array) => {
        var point_center_X = click.x * pad_width
        var point_center_Y = click.y * pad_height
        var point_radius = 10 // in px

        var clickLocator = document.createElement("div");
        clickLocator.className = 'click-locator';
        clickLocator.style.left = point_center_X - point_radius + "px";
        clickLocator.style.top = point_center_Y - point_radius+ "px";
        clickLocator.style.width = point_radius * 2 + "px";
        clickLocator.style.height = point_radius * 2 + "px";

        var point_color = undefined
        var color_name =  this.click_history_color[index]
        if (color_name == 'neutral') {
          clickLocator.style.borderWidth = '0px'
          point_color = "rgba(50, 50, 50, 1)"
        } else if (color_name == 'flash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
        } else if (color_name == 'noflash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
        }
        clickLocator.style.backgroundColor = point_color

        historyContainer.appendChild(clickLocator)
      });

      // update view
      if (this.click_history_container) {
        pad_elem.removeChild(this.click_history_container);
      }
      this.click_history_container = historyContainer
      pad_elem.appendChild(this.click_history_container);
    },
    trigger_ripple: function (relative_click) {
      var pad_elem = this.$refs.padtouch

      // Set necessary variables
      var pad_width = pad_elem.offsetWidth
      var pad_height = pad_elem.offsetHeight
      var ripple_center_X = relative_click.x * pad_width
      var ripple_center_Y = relative_click.y * pad_height
      var start_radius = 10 // in px
      var end_radius = pad_width // in px

      // modified center for the rpi screen that is 90degree rotated
      // var ripple_center_X = (1 - relative_click.y) * pad_width
      // var ripple_center_Y = relative_click.x * pad_height

      //Ripple
      var rippleEffect = document.createElement("div");
      rippleEffect.className = 'ripple-effect';
      rippleEffect.style.left = ripple_center_X - start_radius+ "px";
      rippleEffect.style.top  = ripple_center_Y - start_radius+ "px";
      rippleEffect.style.width  = start_radius * 2 + "px";
      rippleEffect.style.height = start_radius * 2 + "px";

      //rippleContainer
      var rippleContainer = document.createElement("div");
      rippleContainer.className = 'ripple-container';
      rippleContainer.appendChild(rippleEffect);
      rippleContainer.style.width   = pad_width + "px";
      rippleContainer.style.height  = pad_height + "px";
      pad_elem.appendChild(rippleContainer);

      // timeout needed to ensure the previous is applied first
      setTimeout(function() {
           rippleEffect.style.left   = ripple_center_X - end_radius + "px";
           rippleEffect.style.top    = ripple_center_Y - end_radius + "px";
           rippleEffect.style.width  = end_radius * 2 + "px";
           rippleEffect.style.height = end_radius * 2 + "px";
       }, 0);

       setTimeout(function() {
           rippleEffect.style.backgroundColor = "rgba(0, 0, 0, 0)";
       }, 250);

       setTimeout(function() {
           pad_elem.removeChild(rippleContainer);
       }, 1000);
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --pad_height_shrink: 30px;
  --pad_border_width: 2px;
}

.padtouch {
  position: absolute;
  top: calc( var(--display_height) + var(--digit_height) + var(--pad_height_shrink) );
  height: calc( var(--pad_height) - var(--pad_height_shrink) );
  background-color: rgba(66, 65, 78, 0.1);
  cursor: crosshair;
}

.padborder {
  position: absolute;
  top: 0;
  width: calc( var(--screen_width));
  height: var(--pad_border_width);
  background-color: rgba(66, 65, 78, 0.5);
  z-index: 1;
}

.history-container {
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none;
    overflow: hidden;
    background-size: cover;
    z-index: 0;
}

.map-container {
  width: 100%;
  height: 100%;
}

.click-locator {
    position: absolute;
    border-radius: 50%;
    border-style: solid;
    border-width: 2px;
    border-color: rgba(0, 0, 0, 0.85);
    pointer-events: none;
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
    background-color: rgba(66, 65, 78, 0.35);
}

</style>

<style scoped>
/* local styles */
</style>
