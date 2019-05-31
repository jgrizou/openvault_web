<template>
  <div>

    <Digit ref="digit" class="digit"></Digit>

    <Display ref="display" class="display"></Display>

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
      <PadTouch ref="pad" class="pad" :callback="continuous_pad_callback"></PadTouch>
    </div>
    <div v-else-if="pad_type == 'audio'">
      <PadAudio ref="pad" class="pad" :callback="audio_pad_callback"></PadAudio>
    </div>
    <div v-else>
      <!-- <div class="pad">Pad {{ pad_type }} not implemented</div> -->
    </div>

    <!-- check panel appears only when needed -->
    <Check ref="check" :callback="hide_check_panel"></Check>


  </div>
</template>


<script>
import Check from './../components/Check.vue'
import Display from './../components/Display.vue'
import Digit from './../components/Digit.vue'
import Reset from './../components/Reset.vue'
import Pad12 from './../components/Pad_1x2.vue'
import Pad12Random from './../components/Pad_1x2_RandomPadColor.vue'
import Pad33 from './../components/Pad_3x3.vue'
import PadTouch from './../components/Pad_Touch.vue'
import PadAudio from './../components/Pad_Audio.vue'

export default {
  name: 'SPA',
  components: { Check, Display, Digit, Reset, Pad12, Pad12Random, Pad33, PadTouch, PadAudio },
  data() {
    return {
      pad_type: undefined
    };
  },
  mounted: function () {
    this.spawn_learner()
  },
  sockets: {
    init_pad: function (pad_info) {
      this.pad_type = pad_info.type
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
    update_code: function (code_info) {
      if (code_info.apply_pause) {
        this.$refs.digit.show_digit = false
        this.$refs.pad.paused = true // disable the pad button

        setTimeout( () => {
          this.$refs.display.code = code_info.code_json
        }, 50);

        setTimeout( () => {
          this.$refs.digit.show_digit = true
          this.$refs.pad.paused = false // enable the pad button
        }, 900);

      } else {
        this.$refs.display.code = code_info.code_json
      }
    },
    update_flash: function (flash) {
      this.$refs.digit.flash = flash
      this.$refs.pad.awaiting_flash = false // enable the pad button
    },
    update_pad: function (pad_info) {
      this.$refs.pad.update_pad_info(pad_info)
      console.log(pad_info)
    },
    check: function (check_state) {
      this.show_check_panel(check_state)
    }
  },
  methods: {
    spawn_learner: function () {
      // spawn the learner given link given in url
      this.$socket.emit('spawn_learner', this.$route.params.pathMatch)
    },
    reset: function () {
      this.$socket.emit('reset')
    },
    discrete_pad_callback: function (click_info) {
      this.$refs.pad.awaiting_flash = true // disable the pad button

      var feedback_info = {}
      feedback_info.symbol = click_info.button
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)
    },
    continuous_pad_callback: function (click_info) {
      this.$refs.pad.awaiting_flash = true // disable the pad

      var feedback_info = {}
      var x_click = click_info.relative_click.x
      var y_click = click_info.relative_click.y
      feedback_info.signal = [x_click, y_click]
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)

      this.$socket.emit('log', feedback_info)
    },
    audio_pad_callback: function (audio_info) {
      var feedback_info = {}
      feedback_info.mp3 = audio_info.mp3
      feedback_info.flash = this.$refs.digit.flash
      this.$socket.emit('feedback_info', feedback_info)
    },
    show_check_panel: function (check_state) {
      this.$refs.reset.force_hide = true
      this.$refs.check.start(check_state)
    },
    hide_check_panel: function () {
      this.$refs.reset.force_hide = false
      this.reset()
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
