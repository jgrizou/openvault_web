<template>
  <div>

    <div
      ref="padkeyboard"
      class="keyboard keyflash"
      v-show="disabled">
    </div>

    <div
      ref="padkeyboard"
      class="keyboard"
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
    window.addEventListener('keypress', (event) => {
      this.key_history.push(event.key)
      this.key_history_color.push('neutral')

      var keyboard_info = {}
      keyboard_info.key = event.key
      this.callback(keyboard_info)

      console.log(event)
      console.log(event.key)
      console.log(this.key_history)
      console.log(this.key_history_color)

      var pad_elem = this.$refs.padkeyboard
      pad_elem.classList.add("keyflash");
      setTimeout(function(){ pad_elem.classList.remove("keyflash"); }, 500);
    })
  },
  data() {
    return {
      stopped: false,
      paused: false,
      awaiting_flash: false,
      awaiting_pad: false,

      key_history: [],
      key_history_color: [],
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
    update_pad_info: function (pad_info) {
      console.log(pad_info)
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
  position: relative;
  width: 100%;
  height: 100%;
  background-color: var(--invalid_color);
  mask-image: url("./../assets/keyboard.png");
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}

.keyflash {
  background-color: var(--valid_color);
}

</style>

<style scoped>
/* local styles */
</style>
