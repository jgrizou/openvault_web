<template>

  <div
    ref="padaudio"
    class="padaudio"
  >

    <div id="audio-feedback-panel" class="audio-feedback-panel">
    </div>

    <button
      id="audio-btn-micro"
      class="btn-micro-ready"
      v-on:mousedown="on_mousedown"
    ></button>

  </div>

</template>

<script>
const MicRecorder = require('mic-recorder-to-mp3');
const GreenAudioPlayer = require('green-audio-player');
require('green-audio-player/dist/css/green-audio-player.min.css')

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
      stopped: false,
      paused: false,
      awaiting_flash: false,
      awaiting_pad: false,
      awaiting_self: false,
      recorder: new MicRecorder(),
      audio_history_file: [],
      audio_history_fileurl: [],
      audio_history_color: []
    }
  },
  computed: {
    disabled: function () {
      return this.stopped || this.paused || this.awaiting_flash || this.awaiting_pad || this.awaiting_self
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
      this.awaiting_self = false
      this.audio_history_file = []
      this.audio_history_fileurl = []
      this.audio_history_color = []

      var audioFeedbackPanel = document.getElementById("audio-feedback-panel");
      audioFeedbackPanel.innerHTML = ''
    },
    show_audio_history: function () {

      var audioFeedbackPanel = document.getElementById("audio-feedback-panel");
      audioFeedbackPanel.innerHTML = ''

      // loop over all recorded voice
      this.audio_history_fileurl.forEach( (fileurl, index, array) => {

        var audioPlayer = document.createElement("div")
        audioPlayer.className = 'audio-player-' + index
        audioPlayer.innerHTML = '<div class="audio-index">' + String(index).padStart(2, '0') + '</div><audio><source src="' + fileurl + '" type="audio/mp3"></audio>'

        var audio_color = undefined
        var color_name =  this.audio_history_color[index]
        if (color_name == 'neutral') {
          // keep default
        } else if (color_name == 'flash') {
          audio_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
          audioPlayer.style.borderColor = audio_color
        } else if (color_name == 'noflash') {
          audio_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
          audioPlayer.style.borderColor = audio_color
        }
        audioPlayer.style.backgroundColor = audio_color

        // add to the feebdack panel
        audioFeedbackPanel.appendChild(audioPlayer)

        // initiate audio player instance
        var audio_player = new GreenAudioPlayer('.' + audioPlayer.className, { stopOthersOnPlay: true });

      })
    },
    update_pad_info: function (pad_info) {
      if (pad_info.signal_color) {
          this.audio_history_color = pad_info.signal_color
      }
      this.show_audio_history()
    },
    on_mousedown: function () {

      if (! this.disabled) {
        // awaiting that the sound is recorded to renable the pad
        this.awaiting_self = true

        var microphoneElement = document.getElementById("audio-btn-micro");
        microphoneElement.classList.add("btn-micro-ready-active")

        this.start_recording()

        setTimeout( () => {
          this.stop_recording()
          microphoneElement.classList.remove("btn-micro-ready-active")
          this.awaiting_self = false
        }, 1500)

      }

    },
    start_recording: function () {
      //start recording
      this.recorder.start().then(() => {
      }).catch((e) => {
        alert('Voice recording is not working.');
        console.error(e);
      });
    },
    stop_recording: function () {
      // stop recording
      this.recorder.stop().getMp3().then(([buffer, blob]) => {
        // create mp3 file and push date to it
        const file = new File(buffer, 'user_recording.mp3', {
          type: blob.type,
          lastModified: Date.now()
        });
        // save it in history
        this.audio_history_file.push(file)
        this.audio_history_fileurl.push(URL.createObjectURL(file))
        this.audio_history_color.push('neutral')
        // send back to server
        var audio_info = {}
        audio_info.mp3 = file
        this.callback(audio_info)

      }).catch((e) => {
        alert('We could not retrieve your voice recording.');
        console.error(e);
      });
    }
  }
}

</script>

<style>
/* global styles */

span.controls__current-time {
  display: none
}

span.controls__total-time {
  display: none
}

.volume {
  display: none
}

.green-audio-player .controls .controls__slider {
  margin-left: 0px;
  margin-right: 0px;
}

.green-audio-player .controls {
  margin-left: 20px;
  margin-right: -10px;
}

.green-audio-player .play-pause-btn {
  margin-left: 15px;
  margin-right: 0px;
}

.green-audio-player {
  position: relative;
  left: 120px;
  width: 200px;
  min-width: 100px;
  height: 35px;
  margin-top:2px;
  margin-bottom:2px;
  box-shadow: none;
  border-style: solid;
  border-width: 1px;
  border-color: rgba(66, 65, 78, 0.35);
  background-color: rgba(255, 255, 255, 1);
}

.audio-index {
  position: absolute;
  left: 5px;
  font-weight: 600;
  font-size: 20px;
}

.audio-feedback-panel {
  overflow:auto;
  top: 0px;
  left: 0px;
  width: var(--screen_width);
  height: var(--pad_height);
}

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

.btn-micro-ready {
  position: absolute;
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

.btn-micro-ready:hover {
  /* top: var(--micro_top_hover);
  left: var(--micro_left_hover);
  width: var(--micro_diameter_hover);
  height: var(--micro_diameter_hover);
  height: var(--micro_diameter_hover); */
  background-color: rgba(109, 220, 111, 0.8);
  /* background-size: var(--micro_logo_size_hover);
  border-radius: calc(var(--micro_diameter_hover) / 2); */
}

.btn-micro-ready-active {
  background-color: rgba(226, 73, 73, 1);
  animation: recording 1.5s;
  -webkit-animation:recording 1.5s infinite;
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
