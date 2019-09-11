<template>
  <div>

    <div v-if="is_mobile">
      <input
        id="input"
        class="pad hidden-input"
        type="text"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false">
      </input>
      <button
        class="show_keyboard"
        v-on:click="show_keyboard">
        Click to show keyboard
      </button>
    </div>
    <div v-else>
      <div
        class="keyboard keyboard-disabled"
        v-show="disabled">
      </div>

      <div
        class="keyboard keyboard-ready"
        v-show="!disabled">
      </div>
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

    // special hack for mobile: see https://www.outsystems.com/blog/javascript-events-unmasked-how-to-create-input-mask-for-mobile.html
    // we add a listener on the input element (that is hidden but nonetheless existing)
    if (this.is_client_mobile_or_tablet()){

      input.addEventListener('input', (event) => {

        //disabled if not received updated info from server or if key not been released
        if (this.disabled) {
          return
        }

        var text_entered_so_far = event.target.value
        var last_char_entered = text_entered_so_far[text_entered_so_far.length - 1]

        var keyboard_info = {}
        keyboard_info.key = last_char_entered
        this.callback(keyboard_info)

        this.key_history.push(this.last_key_pressed)
        this.key_history_color.push('neutral')
      })

    } else {
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
    }
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
    is_mobile: function () {
      return this.is_client_mobile_or_tablet()
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
      this.check_focus_timer = undefined
      this.key_history = []
      this.key_history_color = []
      this.symbol_color = undefined
    },
    update_pad_info: function (pad_info) {
      // storing the information of which key is which color/meaning
      this.symbol_color = pad_info['symbol_color']
    },
    show_keyboard: function (event) {
      // to show the keyboard on mobile, we bring focus on a hidden input element
      var input_elem = document.getElementById("input");
      input_elem.focus();

      // check every 100ms if focus is on the input, meaning the keyboard is shown
      clearInterval(this.check_focus_timer);
      this.check_focus_timer = setInterval( () => {
        this.check_keyboard_state()
      }, 100)
    },
    check_keyboard_state: function () {

      var input_elem = document.getElementById("input");

      var previous_app_height = this.$parent.app_height

      if (document.activeElement === input_elem) {
        this.$parent.app_height = 400
      } else {
        this.$parent.app_height = 800
      }

      //only call resize if needed
      if (this.$parent.app_height != previous_app_height) {
        this.$parent.handleResize()
      }

    },
    // from https://stackoverflow.com/questions/11381673/detecting-a-mobile-browser
    is_client_mobile_or_tablet: function() {
      var check = false;
      (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
      return check;
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


.hidden-input {
  position: absolute;
  width: 0px;
  height: 0px;
  outline: none;
  border: none;
  color: white;
}

.show_keyboard {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -100%);
  /* width: 60px; */
  /* height: 50px; */
  text-align: center;
  vertical-align: middle;
  font-size: 30px;
  font-weight: 600;
  border-style: solid;
  border-radius: 10px;
  color: rgba(0, 0, 0, 1);
  background-color: rgba(255, 255, 255, 1);
}

</style>

<style scoped>
/* local styles */
</style>
