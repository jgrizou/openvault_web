<template>

  <div
    ref="padaudio"
    class="padaudio"
  >

    <button
      id="audio-btn-micro"
      class="btn-micro-ready"
      v-on:mousedown="on_mousedown"
    ></button>

    <button
      class="btn-show-feedback-panel btn-soundtracks"
      v-show="feedback_show_btn_active"
      v-on:click="feedback_panel_soundtracks_active = true"
    >Show history</button>

    <button
      class="btn-show-feedback-panel btn-embedding"
      v-show="feedback_show_btn_active"
      v-on:click="feedback_panel_embedding_active = true"
    >Show map</button>

    <transition name="slide-feedback">

      <div v-show="feedback_panel_soundtracks_active">
        <div
          ref="padborder"
          class="padborder"
        ></div>
        <div
          id="soundtracks-feedback-panel"
          class="soundtracks-feedback-panel"
        >
        </div>
        <button
          class="btn-show-feedback-panel btn-soundtracks"
          v-on:click="feedback_panel_soundtracks_active = false"
        >Hide history</button>
      </div>

    </transition>

    <transition name="slide-feedback">

      <div v-show="feedback_panel_embedding_active">
        <div
          ref="padborder"
          class="padborder"
        ></div>
        <div
          id="embedding-feedback-panel"
          class="embedding-feedback-panel"
        >
        </div>
        <button
          class="btn-show-feedback-panel btn-embedding"
          v-on:click="feedback_panel_embedding_active = false"
        >Hide map</button>
      </div>

    </transition>


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
      feedback_panel_soundtracks_active: false,
      feedback_panel_embedding_active: false,
      feedback_show_btn_active: false,
      audio_history_file: [],
      audio_history_fileurl: [],
      audio_history_color: [],
      audio_history_location: [],
      classifier_map: undefined
    }
  },
  computed: {
    disabled: function () {
      return this.stopped || this.paused || this.awaiting_flash || this.awaiting_pad || this.awaiting_self
    },
    is_clean: function () {
      return this.audio_history_file.length == 0
    }
  },
  methods: {
    clean_pad: function () {
      this.stopped = false
      this.paused = false
      this.awaiting_flash = false
      this.awaiting_pad = false
      this.awaiting_self = false
      this.feedback_panel_soundtracks_active = false
      this.feedback_panel_embedding_active = false
      this.feedback_show_btn_active = false
      this.audio_history_file = []
      this.audio_history_fileurl = []
      this.audio_history_color = []
      this.audio_history_location = []
      this.classifier_map = undefined

      var audioFeedbackPanel = document.getElementById("soundtracks-feedback-panel");
      audioFeedbackPanel.innerHTML = ''

      // // just starting and stopping a recroding to initiate the MicRecorder/// otherwise the first recorded sound is a bit truncated
      // this.recorder.start().then(() => {
      //   this.recorder.stop().getMp3().then(([buffer, blob]) => {
      //   }).catch((e) => {
      //     alert('Sound recording not allowed or disfunctioning, you need to activate it to try this level');
      //     console.error(e);
      //   });
      // }).catch((e) => {
      //   alert('Sound recording not allowed or disfunctioning, you need to activate it to try this level');
      //   console.error(e);
      // });
    },
    update_pad_info: function (pad_info) {
      console.log(pad_info)
      if (pad_info.signal_color) {
          this.audio_history_color = pad_info.signal_color
      }
      if (pad_info.signal_location) {
          this.audio_history_location = pad_info.signal_location
      }
      if (pad_info.classifier_map) {
          this.classifier_map = pad_info.classifier_map
      }
      // update feedback panels in background
      setTimeout( () => {
        this.show_audio_history()
      }, 0)
    },
    show_audio_history: function () {

      this.show_soundtracks()
      this.show_embedding()

      // enable button to show feedback panel
      if (this.audio_history_fileurl.length) {
        this.feedback_show_btn_active = true
      }
    },
    show_embedding: function () {

      var pad_elem = this.$refs.padaudio
      var pad_width = pad_elem.offsetWidth
      var pad_height = pad_elem.offsetHeight

      var embeddingFeedbackPanel = document.getElementById("embedding-feedback-panel");
      embeddingFeedbackPanel.innerHTML = ''

      if (this.classifier_map) {
          embeddingFeedbackPanel.innerHTML = '<img src="' + this.classifier_map + '") class="embedding-map-container" alt=""/>'
          // as the mapping is changing all the time due to umap, we only plot it for one step
          this.classifier_map = undefined
      }

      this.audio_history_fileurl.forEach( (fileurl, index, array) => {

        var audioEmbedding = document.createElement("div")

        var signal_position = this.audio_history_location[index]

        var point_center_X = signal_position[0] * pad_width
        var point_center_Y = signal_position[1] * pad_height
        var point_radius = 14 // in px

        var signalLocator = document.createElement("div");
        signalLocator.className = 'signal-locator'
        signalLocator.style.left = point_center_X - point_radius + "px";
        signalLocator.style.top = point_center_Y - point_radius+ "px";
        signalLocator.style.width = point_radius * 2 + "px";
        signalLocator.style.height = point_radius * 2 + "px";

        var point_color = undefined
        var color_name =  this.audio_history_color[index]
        if (color_name == 'neutral') {
          point_color = "rgba(255, 255, 255, 1)"
          // point_color = getComputedStyle(document.documentElement).getPropertyValue('--neutral_color');
        } else if (color_name == 'flash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
        } else if (color_name == 'noflash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
        }
        signalLocator.style.backgroundColor = point_color

        embeddingFeedbackPanel.appendChild(signalLocator)

        // overlay sound
        var signalLocatorAudio = document.createElement("div");
        signalLocatorAudio.className = 'audio-dot-player-' + index
        signalLocatorAudio.style.position = 'absolute';
        signalLocatorAudio.style.left = point_center_X - 30.75 + "px";
        signalLocatorAudio.style.top = point_center_Y + 1.75 + "px";
        signalLocatorAudio.innerHTML = '<audio><source src="' + fileurl + '" type="audio/mp3"></audio>'

        embeddingFeedbackPanel.appendChild(signalLocatorAudio)

        // initiate audio player instance
        var audio_player = new GreenAudioPlayer('.' + signalLocatorAudio.className, { stopOthersOnPlay: false });
      })
    },
    show_soundtracks: function () {

      var audioFeedbackPanel = document.getElementById("soundtracks-feedback-panel");
      audioFeedbackPanel.innerHTML = '<div class="audio-spacer"></div>'

      // loop over all recorded voice
      this.audio_history_fileurl.forEach( (fileurl, index, array) => {

        var audioPlayer = document.createElement("div")
        audioPlayer.className = 'audio-player-' + index
        audioPlayer.innerHTML = '<div class="audio-index">' + String(index).padStart(2, '0') + '</div><audio><source src="' + fileurl + '" type="audio/mp3"></audio>'

        var audio_color = undefined
        var color_name =  this.audio_history_color[index]
        if (color_name == 'neutral') {
          audio_color = "rgba(255, 255, 255, 1)"
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
    on_mousedown: function () {

      // do not listen to clicks when pad is disabled
      if (this.disabled) {
          return
      }

      this.start_recording()

      // awaiting that the sound is recorded to renable the pad
      this.awaiting_self = true

      var microphoneElement = document.getElementById("audio-btn-micro");

      setTimeout( () => {
        microphoneElement.classList.add("btn-micro-ready-active")
      }, 250)

      setTimeout( () => {
        microphoneElement.classList.remove("btn-micro-ready-active")
      }, 1750)

      setTimeout( () => {
        this.stop_recording()
        this.awaiting_self = false
      }, 2000)

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

/* Recording button css */

:root {
  --pad_height_shrink: 30px;
  --pad_border_width: 2px;

  --pad_top_with_shrink: calc( var(--display_height) + var(--digit_height) + var(--pad_height_shrink) );
  --pad_height_with_shrink: calc( var(--pad_height) - var(--pad_height_shrink) );

  --micro_diameter: 150px;
  --micro_logo_size: calc( var(--micro_diameter) / 3 );
  --micro_top: calc( (var(--pad_height_with_shrink) - var(--micro_diameter)) / 2);
  --micro_left: calc( (var(--screen_width) - var(--micro_diameter)) / 2);

}

.padaudio {
  position: absolute;
  top: var(--pad_top_with_shrink);
  height: var(--pad_height_with_shrink);
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
  background-color: rgba(109, 220, 111, 0.8);
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

/* Feedback sounds css */


.soundtracks-feedback-panel span.controls__current-time {
  display: none
}

.soundtracks-feedback-panel span.controls__total-time {
  display: none
}

.soundtracks-feedback-panel .volume {
  display: none
}

.soundtracks-feedback-panel .green-audio-player .controls .controls__slider {
  margin-left: 0px;
  margin-right: 0px;
}

.soundtracks-feedback-panel .green-audio-player .controls {
  margin-left: 20px;
  margin-right: -10px;
}

.soundtracks-feedback-panel .green-audio-player .play-pause-btn {
  margin-left: 15px;
  margin-right: 0px;
}

.soundtracks-feedback-panel .green-audio-player {
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
}

.soundtracks-feedback-panel .audio-index {
  position: absolute;
  left: 5px;
  font-weight: 600;
  font-size: 20px;
}


/* Feedback panel animation css */

.slide-feedback-enter-active, .slide-feedback-leave-active {
  transition: all .5s ease-in-out;
}

.slide-feedback-enter, .slide-feedback-leave-to {
  transform: translateY(var(--pad_height_with_shrink));
}

.btn-show-feedback-panel {
  position: absolute;
  top: 370px;
  width: 60px;
  height: 40px;
  border-radius: 20px;
  text-align: center;
  vertical-align: middle;
  font-size: 12px;
  font-weight: 400;
  outline: none; /* remove contour when clicked */
  box-shadow: none;
  border-style: solid;
  border-width: 1px;
  border-color: rgba(66, 65, 78, 0.35);
}

.btn-show-feedback-panel:active {
  background-color: rgba(150, 150, 150, 1);
}

/* soundtrack panel */

.soundtracks-feedback-panel {
  position: absolute;
  overflow:auto;
  top: 0px;
  left: 0px;
  width: var(--screen_width);
  height: var(--pad_height_with_shrink);
  background-color: rgba(240, 240, 240, 1);
}

.btn-soundtracks {
  left: 390px;
}


/* embedding panel */

.embedding-feedback-panel {
  position: absolute;
  top: 0px;
  left: 0px;
  width: var(--screen_width);
  height: var(--pad_height_with_shrink);
  background-color: rgba(240, 240, 240, 1);
}

.btn-embedding {
  left: 10px;
}

.embedding-map-container {
  width: 100%;
  height: 100%;
}


/* embedding css */

.embedding-feedback-panel span.controls__current-time {
  display: none
}

.embedding-feedback-panel span.controls__total-time {
  display: none
}

.embedding-feedback-panel .volume {
  display: none
}

.embedding-feedback-panel .green-audio-player .controls {
  display: none
}

.embedding-feedback-panel .green-audio-player .play-pause-btn {
  margin-left: 0px;
  margin-right: 0px;
}

.embedding-feedback-panel .green-audio-player {
  width: 0px;
  height: 0px;
  margin-top: 0px;
  margin-bottom: 0px;
  box-shadow: none;
}

.embedding-feedback-panel .audio-index {
  position: absolute;
  left: 5px;
  font-weight: 600;
  font-size: 20px;
}

.signal-locator {
    position: absolute;
    border-radius: 10%;
    border-style: solid;
    border-width: 2px;
    border-color: rgba(0, 0, 0, 0.85);
    pointer-events: none;
}


.padborder {
  position: absolute;
  top: 0;
  width: calc( var(--screen_width));
  height: var(--pad_border_width);
  background-color: rgba(66, 65, 78, 0.5);
  z-index: 1;
}


.audio-spacer {
  height: 20px;
}

</style>

<style scoped>
/* local styles */
</style>
