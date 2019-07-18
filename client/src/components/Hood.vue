<template>

  <div v-show="active">

    <div class='hood'>
      <div v-for="index in n_hypothesis" :key="index">
        <div :class="{
          'hyp': true,
          ['hyp' + index]: true
          }"
          :id="'hyp_' + index"
        >

          <div class="hood_info" :id="'hood_info_' + index"></div>

          <div class="hood_display noselect" :id="'hood_display_' + index">
            <div class="hood_pad_container" :id="'hood_pad_container_' + index"></div>
          </div>

        </div>
      </div>
    </div>

    <div v-if="show_button">
      <div class="hide_digit"></div>
      <button
        class="hood_pause_button noselect"
        v-on:click="on_unpause_click">
        Continue
      </button>
    </div>

  </div>

</template>

<script>
const Interpolator = require('color-interpolate');

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
            this.hood_display_1x2(i)
          }
        } else if (this.continuous_pad_list.includes(this.pad_type)) {
          this.hood_display_continuous(i)
        }

      }
    },
    hood_display_1x2: function (i) {

      var historyContainer = document.getElementById("hood_display_" + (i+1));
      historyContainer.style.backgroundColor = 'rgba(255, 255, 255, 0)'

      // get container
      var padContainer = document.getElementById("hood_pad_container_" + (i+1));
      padContainer.innerHTML = ''

      // create the grid
      for (var col = 0; col < 2; col++) {

        var pad_position = col
        var pad_width_str = "var(--hood_pad_container_width)"
        var pad_height_str = "var(--hood_pad_container_height)"
        var margin_str = "var(--hood_pad_button_margin)"

        var buttonLocator = document.createElement("div");
        buttonLocator.className = 'hood_button_locator';
        buttonLocator.id = 'hood_button_locator_' + i + '_' + pad_position;
        buttonLocator.style.top = margin_str;
        buttonLocator.style.left = "calc(" + col + "*" + pad_width_str + "/2 + " + margin_str + ")"
        buttonLocator.style.width = "calc(" + pad_width_str + "/2 - 2*" + margin_str + ")"
        buttonLocator.style.height = "calc(" + pad_height_str +  " - 2*" + margin_str + ")"
        buttonLocator.style.zIndex = 10;

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

      //add info in grid

      var n_dot_per_position = new Array(9).fill(0);

      this.hood_info.symbol_history.forEach( (pad_position, index, array) => {

        var gridElem = document.getElementById('hood_button_locator_' + i + '_' + pad_position)

        var pad_width = gridElem.offsetWidth
        var pad_height = gridElem.offsetHeight

        var dotLocator = document.createElement("div");
        dotLocator.className = 'hood_dot_locator';

        var margin = 2
        var border_width = 1
        var dot_width = Math.floor(pad_width/2) - border_width - margin
        var dot_height = dot_width

        var row_position = n_dot_per_position[pad_position] %  2
        var column_position = Math.floor(n_dot_per_position[pad_position] / 2)

        dotLocator.style.top = column_position * (dot_height + border_width + margin) + 'px';
        dotLocator.style.left = row_position * (dot_width + margin) + 'px';
        dotLocator.style.width = dot_width + 'px';
        dotLocator.style.height = dot_height + 'px';
        dotLocator.style.borderRadius = '50%';
        dotLocator.style.borderStyle = 'solid';
        dotLocator.style.borderWidth = border_width + 'px';
        buttonLocator.style.zIndex = 20;

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
    hood_display_3x3: function (i) {

      var historyContainer = document.getElementById("hood_display_" + (i+1));
      historyContainer.style.backgroundColor = 'rgba(255, 255, 255, 0)'


      // get container
      var padContainer = document.getElementById("hood_pad_container_" + (i+1));
      padContainer.innerHTML = ''

      // create the grid
      for (var col = 0; col < 3; col++) {
        for (var row = 0; row < 3; row++) {


          var pad_position = row*3 + col
          var pad_width_str = "var(--hood_pad_container_width)"
          var pad_height_str = "var(--hood_pad_container_height)"
          var margin_str = "var(--hood_pad_button_margin)"

          var buttonLocator = document.createElement("div");
          buttonLocator.className = 'hood_button_locator';
          buttonLocator.id = 'hood_button_locator_' + i + '_' + pad_position;
          buttonLocator.style.top = "calc(" + row + "*" + pad_height_str + "/3 + " + margin_str + ")"
          buttonLocator.style.left = "calc(" + col + "*" + pad_width_str +"/3 + " + margin_str + ")"
          buttonLocator.style.width = "calc(" + pad_width_str + "/3 - 2*" + margin_str + ")"
          buttonLocator.style.height = "calc(" + pad_height_str + "/3 - 2*" + margin_str + ")"
          buttonLocator.style.zIndex = 10;


          // color per known symbols
          var button_color = getComputedStyle(document.documentElement).getPropertyValue('--neutral_color')
          var color_name =  this.hood_info.known_symbols_colors[''+pad_position]
          if (color_name == 'flash') {
            button_color = getComputedStyle(document.documentElement).getPropertyValue('--on_color')
          } else if (color_name == 'noflash') {
            button_color = getComputedStyle(document.documentElement).getPropertyValue('--off_color')
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
        var dot_width = Math.floor(pad_width/3)
        var dot_height = Math.floor(pad_height/3)

        var row_position = n_dot_per_position[pad_position] %  3
        var column_position = Math.floor(n_dot_per_position[pad_position] / 3)

        dotLocator.style.top = column_position * dot_height + 'px';
        dotLocator.style.left = row_position * dot_width + 'px';
        dotLocator.style.width = dot_width - 2*border_width + 'px';
        dotLocator.style.height = dot_height - 2*border_width + 'px';
        dotLocator.style.borderRadius = '50%';
        dotLocator.style.borderStyle = 'solid';
        dotLocator.style.borderWidth = border_width + 'px';
        dotLocator.style.zIndex = 20;

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
      historyContainer.style.backgroundColor = 'rgba(240, 240, 240, 1)'

      var hood_display_width = historyContainer.offsetWidth
      var hood_display_height = historyContainer.offsetHeight

      if (this.hood_info.hypothesis_classifier_maps) {
        if (this.hood_info.hypothesis_classifier_maps[i]) {
            historyContainer.innerHTML = '<img src="' + this.hood_info.hypothesis_classifier_maps[i] + '") class="map-container" draggable="false" alt=""/>'
        }
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
        if (this.discrete_pad_list.includes(this.pad_type)) {
          this.populate_hood_text_discrete(i)
        } else if (this.continuous_pad_list.includes(this.pad_type)) {
          this.populate_hood_text_continuous(i)
        }
      }
    },
    populate_hood_text_discrete: function(i) {

      var hyp_elem = document.getElementById('hyp_' + (i+1))
      hyp_elem.classList.remove('valid_hyp', 'equally_valid_hyp', 'invalid_hyp');

      var hood_info_elem = document.getElementById('hood_info_' + (i+1))
      hood_info_elem.innerHTML = ''

      var digitElem = document.createElement("div");
      digitElem.innerHTML = '' + i

      if (this.hood_info.hypothesis_validity[i]) {

        // if (this.hood_info.hypothesis_validity.filter(x => x).length == 1) {
        //   digitElem.className = 'hood_default_digit hood_green_digit';
        //   hyp_elem.classList.add('valid_hyp');
        // } else {
        //   digitElem.className = 'hood_default_digit hood_orange_digit';
        //   hyp_elem.classList.add('equally_valid_hyp');
        // }

        digitElem.className = 'hood_default_digit noselect hood_green_digit';
        hyp_elem.classList.add('valid_hyp');

      } else {
        digitElem.className = 'hood_default_digit noselect hood_red_digit ';
        hyp_elem.classList.add('invalid_hyp');
      }

      hood_info_elem.appendChild(digitElem)

    },
    populate_hood_text_continuous: function(i) {

      var hyp_elem = document.getElementById('hyp_' + (i+1))
      hyp_elem.classList.remove('default_hyp');

      var hood_info_elem = document.getElementById('hood_info_' + (i+1))
      hood_info_elem.innerHTML = ''

      function likelihood_to_multiplier(x) {
        var multiplier = 10
        if (x <= 0.5) {
          return Math.tanh(- multiplier * (0.25-x)) / 4 + 0.25
        } else {
          return Math.tanh(multiplier * (x-0.75)) / 4 + 0.75
        }
      }

      // console.log('#######')
      // for (var x = 0; x < 1; x += 0.05) {
      //   console.log(likelihood_to_multiplier(x).toFixed(2))
      // }

      var likelihood = this.hood_info.hypothesis_probability[i]
      var hyp_multiplier = likelihood_to_multiplier(likelihood)

      var max_digit_diameter = 0.9*72
      var min_digit_diameter = 40
      var diff_digit_diameter = max_digit_diameter - min_digit_diameter
      var digit_diameter_str = diff_digit_diameter * hyp_multiplier + min_digit_diameter + 'px'

      var max_digit_fontsize = 30
      var min_digit_fontsize = 18
      var diff_digit_fontsize = max_digit_fontsize - min_digit_fontsize
      var digit_fontsize_str = diff_digit_fontsize * hyp_multiplier + min_digit_fontsize + 'px'

      var digitElem = document.createElement("div");
      digitElem.innerHTML = '' + i
      digitElem.className = 'hood_default_digit noselect';

      digitElem.style.top =  "calc( (var(--hyp_container_height) - " + digit_diameter_str + ") / 2)";
      digitElem.style.left =  "calc( (var(--hood_text_width) - " + digit_diameter_str + ") / 2)";
      digitElem.style.width = digit_diameter_str
      digitElem.style.height = digit_diameter_str

      digitElem.style.fontSize = digit_fontsize_str
      digitElem.style.lineHeight = digit_diameter_str

      var digit_colormap = Interpolator(['rgba(255, 65, 54, 0.5)', 'rgba(255, 175, 116, 0.5)', 'rgba(46, 204, 64, 0.5)']);
      var digit_color = digit_colormap(hyp_multiplier)
      digitElem.style.backgroundColor = digit_color

      hood_info_elem.appendChild(digitElem)

      // add background color
      hyp_elem.classList.add('default_hyp');
      var hyp_colormap = Interpolator(['rgba(255, 65, 54, 0.1)', 'rgba(255, 175, 116, 0.1)', 'rgba(46, 204, 64, 0.1)']);
      // var hyp_colormap = Interpolator(['rgba(255, 65, 54, 0.5)', 'rgba(255, 175, 116, 0.5)', 'rgba(46, 204, 64, 0.5)']);
      var hyp_color = hyp_colormap(hyp_multiplier)
      hyp_elem.style.backgroundColor = hyp_color

      // scale the all thing
      var max_scale = 0.9
      var min_scale = 0.8
      var diff_scale = max_scale - min_scale
      var hyp_scale = diff_scale * hyp_multiplier + min_scale
      hyp_elem.style.transform = "scale(" + hyp_scale + ")"
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --hood_border_width: 2px;
  --hood_width: calc( var(--screen_width) - var(--hood_border_width));
  --hood_height: var(--screen_height);

  --hyp_panel_width: calc( var(--hood_width) / 2 );
  --hyp_panel_height: calc( var(--hood_height) / 5 );

  --hyp_border_width: 2px;
  --hyp_container_width: calc( var(--hyp_panel_width) - 2*var(--hyp_border_width));
  --hyp_container_height: calc( var(--hyp_panel_height) - 2*var(--hyp_border_width));

  --hood_text_width: var(--digit_diameter);
  --hood_display_width: calc( var(--hyp_container_width) - var(--hood_text_width) );

  --hood_pad_margin: 8px;
  --hood_pad_container_width: calc( var(--hood_display_width) - 2*var(--hood_pad_margin));
  --hood_pad_container_height: calc( var(--hyp_container_height) - 2*var(--hood_pad_margin));
  --hood_pad_button_margin: 2px;

  --hood_pause_btn_margin_top: 15px;
  --hood_pause_btn_margin_side: 60px;
  --hood_pause_top: calc(var(--display_height) - var(--shadow_diff) + var(--hood_pause_btn_margin_top));
  --hood_pause_left: var(--hood_pause_btn_margin_side);
  --hood_pause_btn_width: calc(var(--screen_width) - 2*var(--hood_pause_btn_margin_side));
  --hood_pause_btn_height: calc(var(--digit_height) - 2*var(--hood_pause_btn_margin_top));
}

.hide_digit {
  position: absolute;
  top: var(--display_height);
  left: 0px;
  width: var(--screen_width);
  height: var(--digit_height);
  outline: none; /* remove contour when clicked */
  border: none;
  background-color: rgba(255, 255, 255, 1);
}

.hood_pause_button {
  position: absolute;
  top: var(--hood_pause_top);
  left: var(--hood_pause_left);
  width: var(--hood_pause_btn_width);
  height: var(--hood_pause_btn_height);
  outline: none; /* remove contour when clicked */
  border: none;
  border-radius: 30px;
  text-align: center;
  vertical-align: middle;
  font-size: 50px;
  font-weight: 600;
  color: rgba(50, 50, 50, 1);
  background-color: rgba(230, 230, 230, 1);
  box-shadow: 0 var(--shadow_full) rgba(150, 150, 150, 1);
}

.hood_pause_button:active {
  color: rgba(0, 0, 0, 1);
  background-color: rgba(210, 210, 210, 1);
  box-shadow: 0 var(--shadow_min) rgba(100, 100, 100, 1);
  transform: translateY(var(--shadow_diff));
}

.hood {
  position: absolute;
  top: 0px;
  left: var(--screen_width);
  width: var(--hood_width);
  height: var(--hood_height);
  background-color: rgba(255, 255, 255, 1);
  border-left: var(--hyp_border_width) solid rgba(66, 65, 78, 0.5);
}

.hyp {
  position: absolute;
  width: var(--hyp_container_width);
  height: var(--hyp_container_height);
  border: var(--hyp_border_width) solid rgba(66, 65, 78, 0.1);
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

.hood_info {
  position: absolute;
  top: 0px;
  left: 0px;
  width: var(--hood_text_width);
  height: var(--hyp_container_height);
  text-align: center;
  vertical-align: middle;
  font-size: 20px;
  font-weight: 500;
  line-height: calc( var(--hyp_container_height) / 3 );
  /* z-index: 9999; */
  box-sizing: border-box;
  /* border-right: 2px solid rgba(66, 65, 78, 0.5); */
}

.hood_display {
  position: absolute;
  top: 0px;
  left: var(--hood_text_width);
  width: var(--hood_display_width);
  height: var(--hyp_container_height);
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
  width: var(--hood_pad_container_width);
  height: var(--hood_pad_container_height);
}

.hood_dot_locator {
  position: absolute;
}


:root {
  --green_scale: 0.9;
  --green_digit_fontsize: 30px;
  --green_digit_width: calc( 0.9 * var(--hood_text_width));
  --green_color_icon: rgba(46, 204, 64, 0.5);
  --green_color_background: rgba(46, 204, 64, 0.1);

  --orange_scale: 0.9;
  --orange_digit_fontsize: 24px;
  --orange_digit_width: calc( 0.775 * var(--hood_text_width));
  --orange_color_icon: rgba(255, 175, 116, 0.5);
  --orange_color_background: rgba(255, 175, 116, 0.1);

  --red_scale: 0.8;
  --red_digit_fontsize: 18px;
  --red_digit_width: calc( 0.55 * var(--hood_text_width));
  --red_color_icon: rgba(255, 65, 54, 0.5);
  --red_color_background: rgba(255, 65, 54, 0.1);
}

.hood_default_digit {
  position: absolute;
  border-radius: 50%;
  text-align: center;
  vertical-align: middle;
  font-weight: 600;
  z-index: 10;
}

.hood_green_digit {
  top: calc( (var(--hyp_container_height) - var(--green_digit_width)) / 2);
  left: calc( (var(--hood_text_width) - var(--green_digit_width)) / 2);
  width: var(--green_digit_width);
  height: var(--green_digit_width);
  font-size: var(--green_digit_fontsize);
  line-height: calc( var(--green_digit_width) );
  background-color: var(--green_color_icon);
}

.hood_orange_digit {
  top: calc( (var(--hyp_container_height) - var(--orange_digit_width)) / 2);
  left: calc( (var(--hood_text_width) - var(--orange_digit_width)) / 2);
  width: var(--orange_digit_width);
  height: var(--orange_digit_width);
  font-size: var(--orange_digit_fontsize);
  line-height: calc( var(--orange_digit_width) );
  background-color: var(--orange_color_icon);
}

.hood_red_digit {
  top: calc( (var(--hyp_container_height) - var(--red_digit_width)) / 2);
  left: calc( (var(--hood_text_width) - var(--red_digit_width)) / 2);
  width: var(--red_digit_width);
  height: var(--red_digit_width);
  font-size: var(--red_digit_fontsize);
  line-height: calc( var(--red_digit_width) );
  background-color: var(--red_color_icon);
}


.valid_hyp {
  filter: blur(0px);
  -webkit-filter: blur(0px);
  background-color: var(--green_color_background);
  transform: scale(var(--green_scale));
  transform-origin: 50% 50%;
  z-index: 0;
}

.equally_valid_hyp {
  filter: blur(0px);
  -webkit-filter: blur(0px);
  background-color: var(--orange_color_background);
  transform: scale(var(--orange_scale));
  transform-origin: 50% 50%;
  z-index: 0;
}

.invalid_hyp {
  filter: blur(0px);
  -webkit-filter: blur(0px);
  background-color: var(--red_color_background);
  transform: scale(var(--red_scale));
  transform-origin: 50% 50%;
  z-index: 0;
}

.default_hyp {
  filter: blur(0px);
  -webkit-filter: blur(0px);
  transform-origin: 50% 50%;
  z-index: 0;
}

</style>

<style scoped>
/* local styles */
</style>
