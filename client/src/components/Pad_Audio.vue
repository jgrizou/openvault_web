<template>
  <div
    ref="padaudio"
    class="padaudio"
  >

    <button
      class="btn_micro_ready"
      v-on:click="on_click"
      v-on:mousedown="on_mousedown"
      v-on:mouseup="on_mouseup"
    ></button>

    <div> <div>

  </div>
</template>

<script>
const MicRecorder = require('mic-recorder-to-mp3');

export default {
  name: 'PadAudio',
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
      recorder: new MicRecorder()
    }
  },
  computed: {
    disabled: function () {
      return this.paused || this.awaiting_flash
    },
    is_clean: function () {
      return true
    }
  },
  methods: {
    clean_pad: function () {
    },
    update_pad_info: function (pad_info) {
      console.log(pad_info)
    },
    on_click: function () {
    },
    on_mousedown: function () {
      this.recorder.start().then(() => {
        // something else
        // console.log("RECORDING")
        // this.buffer_check = setInterval( () => {
        //   var info = this.recorder.lameEncoder.dataBuffer
        //   console.log(info)
        // }, 1000);

      }).catch((e) => {
        console.error(e);
      });
    },
    on_mouseup: function () {

      // clearInterval(this.buffer_check)

      // Once you are done singing your best song, stop and get the mp3.
      this.recorder.stop().getMp3().then(([buffer, blob]) => {

        // console.log("RECORDING STOPPED")

        // do what ever you want with buffer and blob
        // Example: Create a mp3 file and play
        const file = new File(buffer, 'recording.mp3', {
          type: blob.type,
          lastModified: Date.now()
        });

        var audio_info = {}
        audio_info.mp3 = file

        this.callback(audio_info)

        // const player = new Audio(URL.createObjectURL(file));
        // player.play();

      }).catch((e) => {
        alert('We could not retrieve your message');
        console.log(e);
      });
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --micro_diameter: 150px;
  --micro_logo_size: calc( var(--micro_diameter) / 3 );
  --micro_top: calc( (var(--pad_height) - var(--micro_diameter)) / 2);
  --micro_left: calc( (var(--screen_width) - var(--micro_diameter)) / 2);

  --micro_diameter_hover: 200px;
  --micro_logo_size_hover: calc( var(--micro_diameter_hover) / 3 );
  --micro_top_hover: calc( (var(--pad_height) - var(--micro_diameter_hover)) / 2);
  --micro_left_hover: calc( (var(--screen_width) - var(--micro_diameter_hover)) / 2);

}

.btn_micro_ready {
  position: relative;
  top: var(--micro_top);
  left: var(--micro_left);
  width: var(--micro_diameter);
  height: var(--micro_diameter);
  background-color: rgba(109, 220, 111, 1);
  background-image: url(../assets/microphone-solid.svg);
  background-repeat: no-repeat;
  background-position: center center;
  background-size: var(--micro_logo_size);
  border-radius: calc(var(--micro_diameter) / 2);
  outline: none;
  border: none;
}

.btn_micro_ready:hover {
  top: var(--micro_top_hover);
  left: var(--micro_left_hover);
  width: var(--micro_diameter_hover);
  height: var(--micro_diameter_hover);
  height: var(--micro_diameter_hover);
  background-color: rgba(109, 220, 111, 0.8);
  background-size: var(--micro_logo_size_hover);
  border-radius: calc(var(--micro_diameter_hover) / 2);
}

.btn_micro_ready:active {
  background-color: rgba(226, 73, 73, 1);
  animation: recording 1.8s;
  -webkit-animation:recording 1.8s infinite;
}

@-webkit-keyframes recording {
0%   {background-color: rgba(226, 73, 73, 1);}
55%  {background-color: rgba(226, 73, 73, 0.2);}
100%   {background-color: rgba(226, 73, 73, 1);}
}





</style>

<style scoped>
/* local styles */
</style>
