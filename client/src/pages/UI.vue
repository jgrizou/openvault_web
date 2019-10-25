<template>
  <div class="ui" id="ui">

    <Display ref="display" class="display"></Display>

    <Digit ref="digit" class="digit"></Digit>

    <!-- Big Reset Button -->
    <DigitButton ref="digitbutton" :callback="reset">Restart</DigitButton>

    <!-- reset panel appears only when needed -->
    <Reset ref="reset" :callback="reset"></Reset>

    <!-- level components -->
    <div v-if="pad_type == '1x2'">
      <Pad12 ref="pad" class="pad" :callback="discrete_pad_callback"></Pad12>
    </div>
    <div v-else-if="pad_type == '1x2_random'">
      <Pad12Random ref="pad" class="pad" :callback="discrete_pad_callback"></Pad12Random>
    </div>
    <div v-else-if="pad_type == '3x3'">
      <Pad33 ref="pad" class="pad" :callback="discrete_pad_callback"></Pad33>
    </div>
    <div v-else-if="pad_type == 'touch'">
      <PadTouch ref="pad" class="pad" :callback="touch_pad_callback"></PadTouch>
    </div>
    <div v-else-if="pad_type == 'draw'">
      <PadDraw ref="pad" class="pad" :callback="draw_pad_callback"></PadDraw>
    </div>
    <div v-else-if="pad_type == 'audio'">
      <PadAudio ref="pad" class="pad" :callback="audio_pad_callback"></PadAudio>
    </div>
    <div v-else-if="pad_type == 'keyboard'">
      <PadKeyboard ref="pad" class="pad" :callback="keyboard_pad_callback"></PadKeyboard>
    </div>
    <div v-else>
      <!-- <div class="pad">Pad {{ pad_type }} not implemented</div> -->
    </div>

    <!-- check panel appears only when needed -->
    <Check ref="check" :callback="reset"></Check>

    <!-- hood panel appear once pad_type defined -->
    <div v-if="pad_type">
      <Hood ref="hood" :pad_type="pad_type"></Hood>
    </div>

    <!-- Loader Animation for user feedback on top of everything-->
    <Loader ref="loader"></Loader>

  </div>
</template>


<script>
import Check from './../components/Check.vue'
import Display from './../components/Display.vue'
import Digit from './../components/Digit.vue'
import DigitButton from './../components/Digit_Button.vue'
import Reset from './../components/Reset.vue'
import Pad12 from './../components/Pad_1x2.vue'
import Pad12Random from './../components/Pad_1x2_RandomPadColor.vue'
import Pad33 from './../components/Pad_3x3.vue'
import PadTouch from './../components/Pad_Touch.vue'
import PadDraw from './../components/Pad_Draw.vue'
import PadAudio from './../components/Pad_Audio.vue'
import PadKeyboard from './../components/Pad_Keyboard.vue'
import Hood from './../components/Hood.vue'
import Loader from './../components/Loader.vue'

export default {
  name: 'UI',
  components: { Check, Display, Digit, DigitButton, Reset, Pad12, Pad12Random, Pad33, PadTouch, PadDraw, PadAudio, PadKeyboard, Hood, Loader},
  data() {
    return {
      app_width: 480, // hardcoded value for screen_width
      app_height: 800, // hardcoded value for screen_height
      pad_type: undefined,
      loading_watchdog_interval: undefined,
      timeout_in_seconds: 10, // by default wait 10 seconds to call a timeout
      reload_on_timeout: true  // by default reload the page on timeout
    };
  },
  mounted: function () {
    // start checking loader is not on for too long
    this.start_loading_watchdog()
    // ask server for a new learner
    this.spawn_learner()
    // setup responsiveness
    window.addEventListener('resize', this.handleResize)
    this.handleResize()
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.handleResize)
  },
  sockets: {
    init_timeout: function (timeout_info) {
      this.timeout_in_seconds = timeout_info.timeout_in_seconds
      this.reload_on_timeout = timeout_info.reload_on_timeout
    },
    init_pad: function (pad_info) {
      this.pad_type = pad_info.type
      this.$refs.reset.force_hide = false
      this.$refs.digitbutton.show = false
    },
    is_pad_ready: function () {
      var pad_ready_state = this.$refs.pad != undefined
      this.$socket.emit('pad_ready', pad_ready_state)
    },
    clean_pad: function () {
      this.$refs.pad.clean_pad()
    },
    is_pad_clean: function () {
      if ( this.$refs.pad.is_clean == undefined ) {
        console.error('Error: is_clean property not present in pad: ' + this.pad_type);
      } else {
        var pad_clean_state = this.$refs.pad.is_clean
        this.$socket.emit('pad_clean', pad_clean_state)
      }
    },
    get_url_info: function () {
      var url_info = {}
      url_info.referrer = document.referrer
      url_info.href = document.location.href
      this.$socket.emit('log_url_info', url_info)
    },
    update_code: function (code_info) {
      if (code_info.apply_pause) {
        this.$refs.digit.show_digit = false
        this.$refs.pad.paused = true // force disable the pad button for the time of this pause effect

        setTimeout( () => {
          this.$refs.display.code = code_info.code_json
        }, 50)

        setTimeout( () => {
          this.$refs.pad.paused = false // allow pad button to be enabled again, which also depends on awaiting_flash and awaiting_pad status

          // check every 10ms if we have received all the info we wanted from the server before showing the digit again
          var timer = setInterval( () => {
            if (!this.$refs.pad.awaiting_flash && !this.$refs.pad.awaiting_pad ) {
              this.$refs.digit.show_digit = true
              clearInterval(timer);
            }
          }, 10)
        }, 900)

      } else {
        this.$refs.display.code = code_info.code_json
      }
    },
    update_flash: function (flash) {
      this.$refs.digit.flash = flash
      this.$refs.pad.awaiting_flash = false // enable the pad button
      this.$refs.loader.hide() // deactivate loading animation
    },
    update_pad: function (pad_info) {
      this.$refs.pad.update_pad_info(pad_info)
      this.$refs.pad.awaiting_pad = false
    },
    update_hood: function (hood_info) {
      // if received hood info, rescale the window
      this.app_width = 480 + 480  // hardcoded for screen_width + hood_width
      this.handleResize()
      // and update hood
      this.$refs.hood.update_hood_info(hood_info)
    },
    pause_hood: function() {
      this.$refs.loader.hide() // deactivate loading animation
      this.$refs.hood.apply_pause()
    },
    check: function (check_info) {
      this.$refs.reset.force_hide = true
      this.$refs.loader.hide() // deactivate loading animation
      this.$refs.check.trigger(check_info)

      // when check panel is shown, we do not update the flashing update_flash_pattern so the update_code function might get stuck into a setInterval
      // to ensure the pad can no more be used, we also force the pad to stop
      this.$refs.pad.stopped = true  // yet another way to stop the pad to respond
      // just to be neat we will force awaiting_flash to true to stop that setInterval in update_code to run in the background
      this.$refs.pad.awaiting_flash = false
    },
    no_check: function () {
      // when there is no check, we do not update the flashing update_flash_pattern so the update_code function might get stuck into a setInterval
      // to ensure the pad can no more be used, we also force the pad to stop
      this.$refs.pad.stopped = true  // yet another way to stop the pad to respond
      // just to be neat we will force awaiting_flash to true to stop that setInterval in update_code to run in the background
      this.$refs.pad.awaiting_flash = false

      // show a big restart button
      this.$refs.loader.hide() // deactivate loading animation
      this.$refs.digitbutton.show = true // show restart button
    }
  },
  methods: {
    start_loading_watchdog: function () {
      this.loading_watchdog_interval = setInterval( () => this.loading_watchdog(), 1000)
    },
    stop_loading_watchdog: function () {
      clearInterval(this.loading_watchdog_interval)
    },
    loading_watchdog: function () {
      if (this.$refs.loader) {
        var server_timeout_ms = this.timeout_in_seconds * 1000
        var current_waiting_time_ms = this.$refs.loader.get_loading_duration_ms()

        if (current_waiting_time_ms > server_timeout_ms) {
          this.stop_loading_watchdog()

          if (this.reload_on_timeout) {
            this.reload()
          } else {
            this.$refs.loader.message = 'Server not responding. Try reloading the page.'
          }

          this.$refs.loader.reset_loading_timer()
          this.start_loading_watchdog()
        }
      }
    },
    reload: function () {
      // see https://stackoverflow.com/questions/41301099/do-we-have-router-reload-in-vue-router
      // this.$router.go()  // reload from the vue router
      window.location.reload(true)  // reload from the browser
    },
    handleResize: function (event) {

      // console.log('#######')
      // console.log(window.location)
      // console.log(window.parent.location)
      // console.log(document.referrer)
      // console.log(document.location.href)
      //
      // // iframe detection
      // if ( window.location !== window.parent.location ) {
      //   // The page is in an iframe
      //   console.log('IFRAME')
      // } else {
      //   // The page is not in an iframe
      //   console.log('DIRECT')
      // }

      var current_width = document.documentElement.clientWidth
      var current_height= document.documentElement.clientHeight

      var scale_factor_width = current_width / this.app_width
      var scale_factor_height= current_height / this.app_height
      var scale_factor = Math.min(scale_factor_width, scale_factor_height)

      var translateX = (current_width - scale_factor * this.app_width ) / (2 * scale_factor)
      var translateY = (current_height - scale_factor * this.app_height ) / (2 * scale_factor)
      var translateY = 0 // on top of the page, looks nicer than in the middle

      var ui_elem = document.getElementById("ui")
      ui_elem.style.transform = "scale(" + scale_factor + ") translateX(" + translateX + "px) translateY(" + translateY + "px)";
      ui_elem.style.transformOrigin = "0px 0px"

    },
    spawn_learner: function () {
      // spawn the learner given link given in url
      this.$socket.emit('spawn_learner', this.$route.params.pathMatch)
    },
    reset: function () {
      this.$refs.loader.show_no_delay() // activate loading animation
      this.$refs.reset.force_hide = true // hide reset panel
      this.$socket.emit('reset')
    },
    disable_pad_while_waiting_from_server_update: function () {
      this.$refs.pad.awaiting_flash = true // disable the pad button
      this.$refs.pad.awaiting_pad = true // disable the pad button
      this.$refs.loader.show_with_delay() // activate loading animation
    },
    discrete_pad_callback: function (click_info) {
      this.disable_pad_while_waiting_from_server_update()

      var feedback_info = {}
      feedback_info.symbol = click_info.button
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)
    },
    touch_pad_callback: function (click_info) {
      this.disable_pad_while_waiting_from_server_update()

      var feedback_info = {}
      var x_click = click_info.relative_click.x
      var y_click = click_info.relative_click.y
      feedback_info.signal = [x_click, y_click]
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)

      // this.$socket.emit('log', feedback_info)
    },
    draw_pad_callback: function (draw_info) {
      this.disable_pad_while_waiting_from_server_update()

      var feedback_info = {}
      feedback_info.drawing = draw_info.drawing
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)

      // this.$socket.emit('log', feedback_info)
    },
    audio_pad_callback: function (audio_info) {
      this.disable_pad_while_waiting_from_server_update()

      var feedback_info = {}
      feedback_info.mp3 = audio_info.mp3
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)
    },
    keyboard_pad_callback: function (keyboard_info) {
      this.disable_pad_while_waiting_from_server_update()

      var feedback_info = {}
      feedback_info.symbol = keyboard_info.key
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)
    }
  }
}
</script>


<style>
/* global styles */

:root {
  --screen_width: 480px;
  --screen_height: 800px;
  --display_height: 200px;
  --digit_height: 150px;
  --pad_height: calc( var(--screen_height) - var(--display_height) - var(--digit_height));

  --on_color: rgba(160, 160, 160, 0.85);
  --on_color_active: rgba(110, 110, 110, 0.85);
  --on_shadow_color: rgba(110, 110, 110, 0.85);
  --on_shadow_color_active: rgba(60, 60, 60, 0.85);

  --off_color: rgba(255, 200, 0, 0.85);
  --off_color_active: rgba(200, 150, 0, 0.85);
  --off_shadow_color: rgba(200, 150, 0, 0.85);
  --off_shadow_color_active: rgba(150, 100, 0, 0.85);

  --neutral_color: rgba(66, 65, 78, 1);
  --neutral_color_active: rgba(47, 46, 57, 1);
  --neutral_color_shadow: rgba(20, 20, 20, 1);
  --neutral_color_shadow_active: rgba(0, 0, 0, 1);

  --shadow_full: 12px;
  --shadow_min: 3px;
  --shadow_diff: calc( var(--shadow_full) - var(--shadow_min) );
}

/* fix for firefox mobile, see https://stackoverflow.com/questions/71074/how-to-remove-firefoxs-dotted-outline-on-buttons-as-well-as-links */
button::-moz-focus-inner {
  border: 0;
}

/* no outline or borders by default on buttons */
button {
  outline: none;
  border: none;
}

/* used to force specific element not to be draggable for neat UI*/
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
}

.ui {
  position: fixed;
  left: 0px;
  top: 0px;
  width: var(--screen_width);
  height: var(--screen_height);
  font-family: "Avenir";
}

.noflash {
  background-color: var(--off_color);
  box-shadow: 0 var(--shadow_full) var(--off_shadow_color);
}

.noflash:active {
  background-color: var(--off_color_active);
  box-shadow: 0 var(--shadow_min) var(--off_shadow_color_active);
}

.flash {
  background-color: var(--on_color);
  box-shadow: 0 var(--shadow_full) var(--on_shadow_color);
}

.flash:active {
  background-color: var(--on_color_active);
  box-shadow: 0 var(--shadow_min) var(--on_shadow_color_active);
}

.neutral {
  background-color: var(--neutral_color);
  box-shadow: 0 var(--shadow_full) var(--neutral_color_shadow);
}

.neutral:active {
  background-color: var(--neutral_color_active);
  box-shadow: 0 var(--shadow_min) var(--neutral_color_shadow_active);
}

.btn {
  border-radius: 15px;
}

.btn:active {
  transform: translateY(var(--shadow_diff));
}

.fullscreen {
  position: absolute;
  top: 0px;
  width: var(--screen_width);
  height: var(--screen_height);
  background-color: rgba(255, 255, 255, 1);
}

.display {
  position: absolute;
  top: 0px;
  width: var(--screen_width);
  height: var(--display_height);
  background-color: rgba(255, 255, 255, 1);
}

.digit {
  position: absolute;
  top: var(--display_height);
  width: var(--screen_width);
  height: var(--digit_height);
  background-color: rgba(255, 255, 255, 1);
}

.pad {
  position: absolute;
  top: calc( var(--display_height) + var(--digit_height) );
  width: var(--screen_width);
  height: var(--pad_height);
  background-color: rgba(255, 255, 255, 1);
}

</style>

<style scoped>
/* local styles */
</style>
