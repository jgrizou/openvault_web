<template>
  <div
    id="paddraw"
    ref="paddraw"
    class="paddraw"
  >

    <canvas
      id="drawing-canvas"
      class="drawing-canvas"
      width="1000px"
      height="1000px"
      v-on:mousedown="on_mousedown"
      v-on:mouseup="on_mouseup"
      v-on:mousemove="on_mousemove"
      v-on:mouseleave="on_mouseleave"
    ></canvas>

    <div
      ref="padborder"
      class="padborder"
    ></div>

    <button
      class="btn-show-feedback-panel btn-sketches"
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
          id="sketches-feedback-panel"
          class="sketches-feedback-panel"
        >
        </div>
        <button
          class="btn-show-feedback-panel btn-sketches"
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

export default {
  name: 'PadDraw',
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
      is_recording_drawing: false,
      last_cursor_position_on_pad: undefined,
      current_drawing: [],
      drawing_history: [],
      drawing_history_color: [],
      drawing_history_location: [],
      classifier_map: undefined,
      feedback_show_btn_active: false,
      feedback_panel_soundtracks_active: false,
      feedback_panel_embedding_active: false
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

      this.is_recording_drawing = false
      this.last_cursor_position_on_pad = undefined
      this.current_drawing = []
      this.drawing_history = []
      this.drawing_history_color = []
      this.drawing_history_location = []
      this.classifier_map = undefined

      this.feedback_show_btn_active = false
      this.feedback_panel_soundtracks_active = false
      this.feedback_panel_embedding_active = false
    },
    update_pad_info: function (pad_info) {
      if (pad_info.signal_color) {
          this.drawing_history_color = pad_info.signal_color
      }
      if (pad_info.signal_location) {
          this.drawing_history_location = pad_info.signal_location
      }
      if (pad_info.classifier_map) {
          this.classifier_map = pad_info.classifier_map
      }
      // update feedback panels in background
      setTimeout( () => {
        this.show_sketches_history()
      }, 0)

      // redraw in different color to indicate they can draw again
      // this should listen to this.disabled really
      this.clear_paddraw()
      var canvas = document.getElementById('drawing-canvas');
      this.draw_trajectory_to_canvas(canvas, this.current_drawing, 20, 'rgb(200,200,200)')

      console.log(pad_info)
    },
    clear_paddraw: function () {
      var canvas = document.getElementById('drawing-canvas');
      var context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
    },
    draw_trajectory_to_canvas: function(canvas, trajectory, linewidth=20, color='#000000') {

      var i;
      for (i = 0; i < trajectory.length - 1; i++) {

        var start = {}
        start.x = trajectory[i][0]
        start.y = trajectory[i][1]

        var end = {}
        end.x = trajectory[i+1][0]
        end.y = trajectory[i+1][1]

        this.add_stroke_to_canvas(canvas, start, end, linewidth, color)
      }

    },
    add_stroke_to_canvas: function(canvas, start, end, linewidth=20, color='#000000') {
      var context = canvas.getContext("2d");
      var w = canvas.width;
      var h = canvas.height;

      context.beginPath();
      context.moveTo(start.x * w, start.y * h);
      context.lineTo(end.x * w, end.y * h);
      context.lineWidth = linewidth;
      context.strokeStyle = context.fillStyle = color;
      context.lineJoin = context.lineCap = "round";
      context.stroke();
      context.closePath();
    },
    get_relative_cursor_position: function (event) {
      var pad_elem = this.$refs.paddraw
      var pad_rect = pad_elem.getBoundingClientRect()

      var relative_cursor_position = {}
      relative_cursor_position.x = (event.clientX - pad_rect.x) / pad_rect.width
      relative_cursor_position.y = (event.clientY - pad_rect.y) / pad_rect.height

      return relative_cursor_position
    },
    on_mousemove: function (event) {

      if (this.is_recording_drawing) {

        var relative_cursor_position = this.get_relative_cursor_position(event)

        var canvas = document.getElementById('drawing-canvas');
        this.add_stroke_to_canvas(canvas, this.last_cursor_position_on_pad, relative_cursor_position)

        this.current_drawing.push([relative_cursor_position.x, relative_cursor_position.y])

        this.last_cursor_position_on_pad = relative_cursor_position
      }
    },
    on_mousedown: function (event) {
      // do not listen to clicks when pad is disabled
      if (this.disabled) {
          return
      }

      this.clear_paddraw()
      this.current_drawing = []
      this.last_cursor_position_on_pad = this.get_relative_cursor_position(event)
      this.is_recording_drawing = true
    },
    stop_recording: function (event) {
      if (this.disabled) {
          return
      }

      if (this.is_recording_drawing) {
        this.is_recording_drawing = false
        this.drawing_history.push(this.current_drawing)

        // only if something happened, will be empty if the user just clicks without moving
        if (this.current_drawing.length > 0) {
          var draw_info = {}
          draw_info.drawing = this.current_drawing
          this.callback(draw_info)
        }
      }
    },
    on_mouseup: function (event) {
      this.stop_recording()
    },
    on_mouseleave: function (event) {
      this.stop_recording()
    },
    show_sketches_history: function () {
      this.show_sketches()
      this.show_embedding()

      // enable button to show feedback panel
      if (this.drawing_history.length) {
        this.feedback_show_btn_active = true
      }
    },
    show_sketches: function () {
      var sketchesFeedbackPanel = document.getElementById("sketches-feedback-panel");
      sketchesFeedbackPanel.innerHTML = '<div class="sketch-spacer"></div>'

      // loop over all recorded voice
      this.drawing_history.forEach( (drawing, index, array) => {

        // sketchCanvas.innerHTML = '<div class="audio-index">' + String(index).padStart(2, '0') + '</div>'

        var sketchCanvas = document.createElement("canvas")
        sketchCanvas.className = 'sketch-canvas'
        sketchCanvas.id = 'sketch-canvas-' + index
        sketchCanvas.width = 200
        sketchCanvas.height = 200

        var sketch_color = undefined
        var color_name =  this.drawing_history_color[index]
        if (color_name == 'neutral') {
          sketch_color = "rgba(255, 255, 255, 1)"
        } else if (color_name == 'flash') {
          sketch_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
        } else if (color_name == 'noflash') {
          sketch_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
        }
        sketchCanvas.style.backgroundColor = sketch_color


        var context = sketchCanvas.getContext("2d");
        context.font = "40px arial sans-serif";
        context.fillText(String(index).padStart(2, '0'), 2, 34);


        this.draw_trajectory_to_canvas(sketchCanvas, drawing, 8, '#000000')

        sketchesFeedbackPanel.appendChild(sketchCanvas)
      })
    },
    show_embedding: function () {

      var pad_elem = this.$refs.paddraw
      var pad_width = pad_elem.offsetWidth
      var pad_height = pad_elem.offsetHeight

      var embeddingFeedbackPanel = document.getElementById("embedding-feedback-panel");
      embeddingFeedbackPanel.innerHTML = ''

      if (this.classifier_map) {
          embeddingFeedbackPanel.innerHTML = '<img src="' + this.classifier_map + '") class="embedding-map-container" alt=""/>'
          // as the mapping is changing all the time due to umap, we only plot it for one step
          this.classifier_map = undefined
      }

      this.drawing_history.forEach( (drawing, index, array) => {

        var sketchEmbedding = document.createElement("div")

        var signal_position = this.drawing_history_location[index]

        var point_center_X = signal_position[0] * pad_width
        var point_center_Y = signal_position[1] * pad_height
        var point_radius = 25 // in px

        var sketchCanvas = document.createElement("canvas")
        sketchCanvas.className = 'signal-locator'
        sketchCanvas.width = 100
        sketchCanvas.height = 100

        sketchCanvas.style.left = point_center_X - point_radius + "px";
        sketchCanvas.style.top = point_center_Y - point_radius+ "px";
        sketchCanvas.style.width = point_radius * 2 + "px";
        sketchCanvas.style.height = point_radius * 2 + "px";

        var point_color = undefined
        var color_name =  this.drawing_history_color[index]
        if (color_name == 'neutral') {
          point_color = "rgba(255, 255, 255, 0)"
        } else if (color_name == 'flash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
        } else if (color_name == 'noflash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
        }
        sketchCanvas.style.backgroundColor = point_color

        this.draw_trajectory_to_canvas(sketchCanvas, drawing, 4, '#000000')

        embeddingFeedbackPanel.appendChild(sketchCanvas)

      })
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --feedback_sketch_canvas_width: 150px;
}

.paddraw {
  position: absolute;
  top: calc( var(--display_height) + var(--digit_height) + var(--pad_height_shrink) );
  height: calc( var(--pad_height) - var(--pad_height_shrink) );
  background-color: rgba(240, 240, 240, 1);
}

.drawing-canvas {
  position: absolute;
  width: var(--screen_width);
  height: calc( var(--pad_height) - var(--pad_height_shrink) );
}

/* feedback sketeches panel */

.sketches-feedback-panel {
  position: absolute;
  overflow:auto;
  top: 0px;
  left: 0px;
  width: var(--screen_width);
  height: calc( var(--pad_height) - var(--pad_height_shrink) );
  background-color: rgba(240, 240, 240, 1);
}

.btn-show-feedback-panel.btn-sketches {
  left: 390px;
}

.sketch-spacer {
  height: 20px;
}

.sketch-canvas {
  position: relative;
  display: block;
  left: calc( ( var(--screen_width) - var(--feedback_sketch_canvas_width) ) / 2 );
  width: var(--feedback_sketch_canvas_width);
  height: var(--feedback_sketch_canvas_width);
  margin-top:2px;
  margin-bottom:2px;
  box-shadow: none;
  border-style: solid;
  border-width: 1px;
  border-color: rgba(66, 65, 78, 0.35);
  background-color: rgba(255, 255, 255, 1);
}

.sketch-canvas-embedding {
  position: absolute;
}

</style>

<style scoped>
/* local styles */
</style>
