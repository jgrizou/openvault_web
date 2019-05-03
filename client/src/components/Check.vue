<template>

  <div>

    <transition name="slide-check">

      <div class="check" v-show="active">

        <div :class="{
          'smiley': true,
          ['smiley_' + smiley_state]: true
        }">
        </div>


        <div class="check_text">
          <div class="loader_text" v-if="smiley_state == 'loader'">
            <h1>ANALYSING CODE ...</h1>
          </div>
          <div class="valid_text" v-else-if="smiley_state == 'valid'">
            <h1>CODE IS VALID !</h1>
            <p>Vault is open. Collect your gift.</p>
          </div>
          <div class="invalid_text" v-else-if="smiley_state == 'invalid'">
            <h1>WRONG CODE</h1>
            <p>Maybe next time.</p>
          </div>
          <div class="inconsistent_text" v-else-if="smiley_state == 'inconsistent'">
            <h1>OOPS</h1>
            <p>You got mixed up.</p>
          </div>
        </div>

        <div v-if="show_button">
          <button class="check_button" v-on:click="on_click">
            <div v-if="smiley_state == 'valid'">
              RESTART
            </div>
            <div v-else-if="smiley_state == 'invalid'">
              TRY AGAIN
            </div>
            <div v-else-if="smiley_state == 'inconsistent'">
              TRY AGAIN
            </div>
          </button>
        </div>
      </div>

    </transition>

  </div>
</template>

<script>

export default {
  name: "Check",
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      smiley_state: '',
      active: false,
      show_button: false,
      loader_audio: new Audio("/audio/drum.wav"),
      valid_audio: new Audio("/audio/unlock.wav"),
      invalid_audio: new Audio("/audio/fart.wav"),
      inconsistent_audio: new Audio("/audio/sneeze.wav")
    }
  },
  methods: {
    on_click: function () {
      this.smiley_state = ''
      this.active = false
      this.show_button = false
      this.callback()
    },
    start: function (check_state) {
      this.active = true

      var slide_timeout_ms = 500
      var loader_timeout_ms = 1300 + slide_timeout_ms
      var stop_load_audio_timeout_ms = 300 + loader_timeout_ms
      var reveal_timeout_ms = 1000 + stop_load_audio_timeout_ms
      var button_timeout_ms = 2000 + reveal_timeout_ms

      if (check_state == 'inconsistent') {

        setTimeout( () => {
          this.smiley_state = check_state
          this.inconsistent_audio.currentTime = 0
          this.inconsistent_audio.play()
        }, slide_timeout_ms);

        setTimeout( () => {
          this.show_button = true
        }, slide_timeout_ms + 2000);

      } else {

        this.loader_audio.currentTime = 0
        this.loader_audio.play()

        setTimeout( () => {
          this.smiley_state = 'loader'
        }, slide_timeout_ms);

        setTimeout( () => {
          this.smiley_state = ''
        }, loader_timeout_ms);

        setTimeout( () => {
          this.loader_audio.pause()
        }, stop_load_audio_timeout_ms);

        setTimeout( () => {
          this.smiley_state = check_state

          if (check_state == 'valid') {
            this.valid_audio.currentTime = 0
            this.valid_audio.play()
          } else if (check_state == 'invalid') {
            this.invalid_audio.currentTime = 0
            this.invalid_audio.play()
          }

        }, reveal_timeout_ms);

        setTimeout( () => {
          this.show_button = true
        }, button_timeout_ms);

      }

    }
  }
}

</script>

<style>
/* global styles */


:root {
  --loader_color: rgba(255, 255, 255, 1);
  --valid_color: rgba(0, 255, 126, 1);
  --invalid_color: rgba(255, 37, 70, 1);
  --inconsistent_color: rgba(255, 255, 255, 1);
}

.check {
  position: absolute;
  top: var(--display_height);
  width: var(--screen_width);
  height: calc( var(--screen_height) - var(--display_height) );
  background-color: var(--neutral_color);
}

.slide-check-enter-active, .slide-check-leave-active {
  transition: all .5s ease-in-out;
}

.slide-check-enter, .slide-check-leave-to {
  transform: translateY(calc(var(--screen_height) - var(--display_height)));
}

:root {
  --smiley_width: 250px;
}

.smiley {
  position: absolute;
  top: 50px;
  left: calc( (var(--screen_width) - var(--smiley_width)) / 2 );
  width: var(--smiley_width);
  height: var(--smiley_width);
}

.smiley_loader {
  background-color: var(--loader_color);
  -webkit-mask-box-image: url("./../assets/smileys/loader.gif");
}

.smiley_valid {
  background-color: var(--valid_color);
  -webkit-mask-box-image: url("./../assets/smileys/valid.png");
}

.smiley_invalid {
  background-color: var(--invalid_color);
  -webkit-mask-box-image: url("./../assets/smileys/invalid.png");
}

.smiley_inconsistent {
  background-color: var(--inconsistent_color);
  -webkit-mask-box-image: url("./../assets/smileys/inconsistent.png");
}

.check_text h1 {
  position: absolute;
  top: 300px;
  left: 65px;
  width: 350px;
  text-align: center;
  vertical-align: middle;
  font-size: 40px;
  font-weight: 600;
}

.check_text p {
  position: absolute;
  top: 360px;
  left: 65px;
  width: 350px;
  font-size: 25px;
  font-weight: 500;
  text-align: center;
  vertical-align: middle;
}

.loader_text h1 {
  color: var(--loader_color);
}

.valid_text h1 {
  color: var(--valid_color);
}

.valid_text p {
  color: rgba(230, 230, 230, 1);
}

.invalid_text h1 {
  color: var(--invalid_color);
}

.invalid_text p {
  color: rgba(230, 230, 230, 1);
}

.inconsistent_text {
  color: var(--inconsistent_color);
}

.check_button {
  position: absolute;
  top: 480px;
  left: 140px;
  width: 200px;
  height: 70px;
  outline: none; /* remove contour when clicked */
  border: none;
  text-align: center;
  vertical-align: middle;
  font-size: 30px;
  font-weight: 600;
  color: rgba(0, 0, 0, 1);
  border-radius: 15px;
  background-color: rgba(230, 230, 230, 1);
  box-shadow: 0 10px rgba(150, 150, 150, 1);
}

.check_button:active {
  background-color: rgba(200, 200, 200, 1);
  box-shadow: 0 5px rgba(100, 100, 100, 1);
  transform: translateY(5px);
}



</style>

<style scoped>
/* local styles */
</style>
