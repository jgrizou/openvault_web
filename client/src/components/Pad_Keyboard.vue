<template>
  <div>

    <div
      class="keyboard keyboard-disabled"
      v-show="disabled">
    </div>

    <div
      class="keyboard keyboard-ready"
      v-show="!disabled">
    </div>

  </div>
</template>

<script>

export default {
  name: 'PadKeyboard',
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  mounted() {
    window.addEventListener('keydown', (event) => {

      //disabled if not received updated info from server or if key not been released
      if (this.disabled) {
        return
      }

      // see https://www.fxsitecompat.dev/en-CA/docs/2018/keydown-and-keyup-events-are-now-fired-during-ime-composition/
      if (event.isComposing) {
        return;
      }

      this.awaiting_keyup = true
      this.last_key_pressed = event.key

      var keyboard_info = {}
      keyboard_info.key = this.last_key_pressed
      this.callback(keyboard_info)

      this.key_history.push(this.last_key_pressed)
      this.key_history_color.push('neutral')
    })

    window.addEventListener('keyup', (event) => {
      // if same key that was pressed and sent is released then we can get back to accepting new keypressed
      if (event.key == this.last_key_pressed) {
        this.awaiting_keyup = false
      }
    })
  },
  data() {
    return {
      stopped: false,
      paused: false,
      awaiting_flash: false,
      awaiting_pad: false,
      awaiting_keyup: false,
      last_key_pressed: undefined,
      key_history: [],
      key_history_color: [],
      symbol_color: undefined,
    }
  },
  computed: {
    disabled: function () {
      return this.stopped || this.paused || this.awaiting_flash || this.awaiting_pad || this.awaiting_keyup
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
      this.awaiting_keyup = false
      this.last_key_pressed = undefined
      this.key_history = []
      this.key_history_color = []
      this.symbol_color = undefined
    },
    update_pad_info: function (pad_info) {
      // storing the information of which key is which color/meaning
      this.symbol_color = pad_info['symbol_color']
    }
  }
}

</script>

<style>
/* global styles */
:root {
  --png_width: 920px;
  --png_height: 681px;
}

.keyboard {
  position: absolute;
  width: 100%;
  height: 100%;
  mask-image: url("./../assets/keyboard.png");
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}

.keyboard-ready {
  background-color: rgba(200, 200, 200, 1);
}

.keyboard-disabled {
  background-color: rgba(0, 0, 0, 1);
}


</style>

<style scoped>
/* local styles */
</style>
