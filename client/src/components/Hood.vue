<template>

  <div v-show="active">

    <div class='hood'>
      <div v-for="index in n_hypothesis" :key="index">
        <div :class="{
          'hyp': true,
          ['hyp' + index]: true
          }"
        >

          <div class="round hood_digit">{{ index - 1 }}</div>

          <div class="hood_display" :id="'hood_display_' + index"></div>

          <div class="hood_text" :id="'hood_text_' + index"></div>

        </div>
      </div>
    </div>

    <div v-if="show_button">
      <button class="hood_pause_button" v-on:click="on_unpause_click">
        New digit identified
        <br><br>
        Click here to propagate the labels
      </button>
    </div>

  </div>

</template>

<script>

export default {
  name: "Hood",
  props: {
    pad_type: {
      type: String,
      required: true,
      default: undefined
    }
  },
  data() {
    return {
      active: false,
      show_button: false,
      n_hypothesis: 10,
      discrete_pad_list: ['1x2', '1x2_random', '3x3'],
      continuous_pad_list: ['touch', 'draw', 'audio'],
      hood_info: undefined
    }
  },
  methods: {
    apply_pause: function () {
      this.show_button = true
    },
    on_unpause_click: function () {
      this.$socket.emit('hood_pause_end')
      this.show_button = false
    },
    update_hood_info: function(hood_info) {
      this.active = true
      this.show_button = false

      console.log(this.pad_type)
      console.log(hood_info)
      this.hood_info = hood_info
      this.update_hood_text()
      this.update_hood_display()
    },
    update_hood_display: function() {
      for (var i = 0; i < this.n_hypothesis; i++) {

        if (this.discrete_pad_list.includes(this.pad_type)) {
          if (this.pad_type == '3x3') {
            this.hood_display_3x3(i)
          } else {
            console.log(i)
          }
        } else if (this.continuous_pad_list.includes(this.pad_type)) {
          this.hood_display_continuous(i)
        }

      }
    },
    hood_display_3x3: function (i) {
      // get container
      var historyContainer = document.getElementById("hood_display_" + (i+1));
      historyContainer.innerHTML = ''

      var padContainer = document.createElement("div");
      padContainer.className = 'hood_pad_container';
      historyContainer.appendChild(padContainer)

      var pad_display_width = padContainer.offsetWidth
      var pad_display_height = padContainer.offsetHeight

      // create the grid
      for (var col = 0; col < 3; col++) {
        for (var row = 0; row < 3; row++) {


          var pad_position = row*3 + col
          var margin = 2

          var buttonLocator = document.createElement("div");
          buttonLocator.className = 'hood_button_locator';
          buttonLocator.id = 'hood_button_locator_' + i + '_' + pad_position;
          buttonLocator.style.top = row*pad_display_height/3 + margin + 'px';
          buttonLocator.style.left = col*pad_display_width/3 + margin + 'px';
          buttonLocator.style.width = pad_display_width/3 - 2*margin + 'px';
          buttonLocator.style.height = pad_display_height/3 -2*margin + 'px';

          // color per known symbols
          var button_color = getComputedStyle(document.documentElement).getPropertyValue('--neutral_color');
          var color_name =  this.hood_info.known_symbols_colors[''+pad_position]
          if (color_name == 'flash') {
            button_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
          } else if (color_name == 'noflash') {
            button_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
          }
          buttonLocator.style.backgroundColor = button_color

          // add to container
          padContainer.appendChild(buttonLocator)
        }
      }

      //add info in grid

      var n_dot_per_position = new Array(9).fill(0);

      this.hood_info.symbol_history.forEach( (pad_position, index, array) => {

        var gridElem = document.getElementById('hood_button_locator_' + i + '_' + pad_position)

        var pad_width = gridElem.offsetWidth
        var pad_height = gridElem.offsetHeight

        var dotLocator = document.createElement("div");
        dotLocator.className = 'hood_dot_locator';

        var border_width = 1
        var dot_width = Math.floor(pad_width/3) - border_width
        var dot_height = Math.floor(pad_height/3) - border_width

        var row_position = n_dot_per_position[pad_position] %  3
        var column_position = Math.floor(n_dot_per_position[pad_position] / 3)

        dotLocator.style.top = column_position * dot_height + 'px';
        dotLocator.style.left = row_position * dot_width + 'px';
        dotLocator.style.width = dot_width + 'px';
        dotLocator.style.height = dot_height + 'px';
        dotLocator.style.borderRadius = '50%';
        dotLocator.style.borderStyle = 'solid';
        dotLocator.style.borderWidth = border_width + 'px';

        // color per click
        var button_color = getComputedStyle(document.documentElement).getPropertyValue('--neutral_color');
        var color_name =  this.hood_info.hypothesis_colors[i][index]
        if (color_name == 'flash') {
          button_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
        } else if (color_name == 'noflash') {
          button_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
        }
        dotLocator.style.backgroundColor = button_color;

        gridElem.appendChild(dotLocator)

        // increment number of dot in this button
        n_dot_per_position[pad_position] += 1
      })

    },
    hood_display_continuous: function(i) {

      // get container
      var historyContainer = document.getElementById("hood_display_" + (i+1));
      historyContainer.innerHTML = ''

      var hood_display_width = historyContainer.offsetWidth
      var hood_display_height = historyContainer.offsetHeight

      if (this.hood_info.hypothesis_classifier_maps[i]) {
          historyContainer.innerHTML = '<img src="' + this.hood_info.hypothesis_classifier_maps[i] + '") class="map-container" alt=""/>'
      }

      // add points one by one
      this.hood_info.signal_location.forEach( (position, index, array) => {

        var point_center_X = position[0] * hood_display_width
        var point_center_Y = position[1] * hood_display_height
        var point_radius = 6 // in px

        var pointLocator = document.createElement("div");
        pointLocator.className = 'hood_click_locator';
        pointLocator.style.left = point_center_X - point_radius + "px";
        pointLocator.style.top = point_center_Y - point_radius+ "px";
        pointLocator.style.width = point_radius * 2 + "px";
        pointLocator.style.height = point_radius * 2 + "px";

        var point_color = undefined
        var color_name =  this.hood_info.hypothesis_colors[i][index]
        if (color_name == 'flash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color');
        } else if (color_name == 'noflash') {
          point_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color');
        }
        pointLocator.style.backgroundColor = point_color

        // add point to div
        historyContainer.appendChild(pointLocator)
      });
    },
    update_hood_text: function() {

      for (var i = 0; i < this.n_hypothesis; i++) {

        var hood_text_elem = document.getElementById('hood_text_' + (i+1))

        if (this.discrete_pad_list.includes(this.pad_type)) {
          hood_text_elem.innerHTML = this.hood_text_innerHTML_discrete(i)
        } else if (this.continuous_pad_list.includes(this.pad_type)) {
          hood_text_elem.innerHTML = this.hood_text_innerHTML_continuous(i)
        }
      }
    },
    hood_text_innerHTML_discrete: function(i) {
      if (this.hood_info.hypothesis_validity[i]) {
        return 'True'
      } else {
        return 'False'
      }
    },
    hood_text_innerHTML_continuous: function(i) {
      var likelihood = this.hood_info.hypothesis_probability[i]
      var likelihood_with2Decimals_floored = likelihood.toString().match(/^-?\d+(?:\.\d{0,2})?/)[0]
      return likelihood_with2Decimals_floored
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --hood_width: var(--screen_width);
  --hood_height: var(--screen_height);

  --hyp_panel_width: calc( var(--hood_width) / 2 );
  --hyp_panel_height: calc( var(--hood_height) / 5 );

  --hood_pad_margin: 8px;
}

.hood_pause_button {
  position: absolute;
  top: var(--display_height);
  left: 0px;
  width: var(--screen_width);
  height: var(--digit_height);
  outline: none; /* remove contour when clicked */
  border: none;
  text-align: center;
  vertical-align: middle;
  font-size: 30px;
  font-weight: 600;
  color: rgba(0, 0, 0, 1);
  background-color: rgba(230, 230, 230, 1);
}

.hood_pause_button:active {
  background-color: rgba(200, 200, 200, 1);
}


.hood {
  position: absolute;
  top: 0px;
  left: var(--hood_width);
  width: var(--hood_width);
  height: var(--hood_height);
  /* background-color: rgba(255, 0, 0, 1); */
}

.hyp {
  position: absolute;
  width: var(--hyp_panel_width);
  height: var(--hyp_panel_height);
  /* background-color: rgba(0, 255, 0, 0.5); */
}


.hyp1 {
  top: calc( 0 * var(--hyp_panel_height) );
  left: 0px;
}

.hyp2 {
  top: 0px;
  left: var(--hyp_panel_width);
}

.hyp3 {
  top: calc( 1 * var(--hyp_panel_height) );
  left: 0px;
}

.hyp4 {
  top: calc( 1 * var(--hyp_panel_height) );
  left: var(--hyp_panel_width);
}

.hyp5 {
  top: calc( 2 * var(--hyp_panel_height) );
  left: 0px;
}

.hyp6 {
  top: calc( 2 * var(--hyp_panel_height) );
  left: var(--hyp_panel_width);
}

.hyp7 {
  top: calc( 3 * var(--hyp_panel_height) );
  left: 0px;
}

.hyp8 {
  top: calc( 3 * var(--hyp_panel_height) );
  left: var(--hyp_panel_width);
}

.hyp9 {
  top: calc( 4 * var(--hyp_panel_height) );
  left:0px;
}

.hyp10 {
  top: calc( 4 * var(--hyp_panel_height) );
  left: var(--hyp_panel_width);
}

.hood_digit {
  background-color: rgba(255, 0, 0, 0.5);
}

.hood_display {
  position: absolute;
  top: 0px;
  left: var(--digit_spacing);
  width: calc( var(--hyp_panel_width) - var(--digit_spacing));
  height: var(--hyp_panel_height);
  background-color: rgba(100, 100, 100, 0.1);
}

.hood_text {
  position: absolute;
  top: var(--digit_spacing);
  left: 0px;
  width: var(--digit_spacing);
  height: calc( var(--hyp_panel_height) - var(--digit_spacing));
  text-align: center;
  vertical-align: middle;
  font-size: 20px;
  font-weight: 500;
  line-height: calc( var(--hyp_panel_height) - var(--digit_spacing) );
  background-color: rgba(100, 100, 100, 0.5);
}

.hood_click_locator {
    position: absolute;
    border-radius: 50%;
    border-style: solid;
    border-width: 2px;
    border-color: rgba(0, 0, 0, 0.85);
    pointer-events: none;
}

.hood_button_locator {
  position: absolute;
  border-radius: 5px;
}

.hood_pad_container {
  position: absolute;
  top: var(--hood_pad_margin);
  left: var(--hood_pad_margin);
  width: calc( var(--hyp_panel_width) - var(--digit_spacing) - 2*var(--hood_pad_margin));
  height: calc( var(--hyp_panel_height) - 2*var(--hood_pad_margin));
}

.hood_dot_locator {
  position: absolute;
}




</style>

<style scoped>
/* local styles */
</style>
