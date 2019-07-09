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

          <div class="hood_display" :id="'hood_display_' + index">
            <div class="hood_pad_container" :id="'hood_pad_container_' + index"></div>
          </div>


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
            this.hood_display_1x2(i)
          }
        } else if (this.continuous_pad_list.includes(this.pad_type)) {
          this.hood_display_continuous(i)
        }

      }
    },
    get_padContainer: function (i) {
      // get container
      var padContainer = document.getElementById("hood_pad_container_" + (i+1));
      padContainer.innerHTML = ''

      var pad_display_width = padContainer.offsetWidth
      var pad_display_height = padContainer.offsetHeight

      // hack needed somehow for the first display as it seems the pad_display_width using the calc() in css has not yet been computed from the browser, workaround possible but not worth the time for now
      if (pad_display_width == 0) {
        pad_display_width = 147
      }
      if (pad_display_height == 0) {
        pad_display_height = 140
      }

      return [padContainer, pad_display_width, pad_display_height]
    },
    hood_display_1x2: function (i) {

      // get container
      var [padContainer, pad_display_width, pad_display_height] = this.get_padContainer(i)

      // create the grid
      for (var col = 0; col < 2; col++) {

        var pad_position = col
        var margin = 2

        var buttonLocator = document.createElement("div");
        buttonLocator.className = 'hood_button_locator';
        buttonLocator.id = 'hood_button_locator_' + i + '_' + pad_position;
        buttonLocator.style.top = margin + 'px';
        buttonLocator.style.left = col*pad_display_width/2 + margin + 'px';
        buttonLocator.style.width = pad_display_width/2 - 2*margin + 'px';
        buttonLocator.style.height = pad_display_height - 2*margin + 'px';

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
      // get container
      var [padContainer, pad_display_width, pad_display_height] = this.get_padContainer(i)

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
          buttonLocator.style.height = pad_display_height/3 - 2*margin + 'px';

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

      if (this.hood_info.hypothesis_classifier_maps) {
        if (this.hood_info.hypothesis_classifier_maps[i]) {
            historyContainer.innerHTML = '<img src="' + this.hood_info.hypothesis_classifier_maps[i] + '") class="map-container" alt=""/>'
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
      hyp_elem.classList.remove('valid_hyp', 'invalid_hyp');

      var hood_info_elem = document.getElementById('hood_info_' + (i+1))
      hood_info_elem.innerHTML = ''

      var digitElem = document.createElement("div");
      digitElem.innerHTML = '' + i

      if (this.hood_info.hypothesis_validity[i]) {
        digitElem.className = 'hood_green_light';
        hyp_elem.classList.add('valid_hyp');
      } else {
        digitElem.className = 'hood_red_light';
        hyp_elem.classList.add('invalid_hyp');
      }

      hood_info_elem.appendChild(digitElem)
    },
    populate_hood_text_continuous: function(i) {
      var likelihood = this.hood_info.hypothesis_probability[i]
      var likelihood_with2Decimals_floored = likelihood.toString().match(/^-?\d+(?:\.\d{0,3})?/)[0]

      var hood_info_elem = document.getElementById('hood_info_' + (i+1))
      hood_info_elem.innerHTML = likelihood_with2Decimals_floored
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
  background-color: rgba(66, 65, 78, 0);
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
  /* background-color: rgba(100, 0, 0, 1); */
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
  --green_light_width: calc( 0.9 * var(--hood_text_width));
  --red_light_width: calc( 0.75 * var(--green_light_width) );
}



.hood_green_light {
  position: absolute;
  top: calc( (var(--hyp_container_height) - var(--green_light_width)) / 2);
  left: calc( (var(--hood_text_width) - var(--green_light_width)) / 2);
  width: var(--green_light_width);
  height: var(--green_light_width);
  border-radius: 50%;
  text-align: center;
  vertical-align: middle;
  font-size: 30px;
  font-weight: 600;
  line-height: calc( var(--green_light_width) );
  background-color: rgba(0, 255, 0, 1);
}

.hood_red_light {
  position: absolute;
  top: calc( (var(--hyp_container_height) - var(--red_light_width)) / 2);
  left: calc( (var(--hood_text_width) - var(--red_light_width)) / 2);
  width: var(--red_light_width);
  height: var(--red_light_width);
  border-radius: 50%;
  text-align: center;
  vertical-align: middle;
  font-size: 22px;
  font-weight: 600;
  line-height: calc( var(--red_light_width) );
  background-color: rgba(255, 0, 0, 1);
}

.valid_hyp {
  filter: blur(0px);
  -webkit-filter: blur(0px);
  background-color: rgba(0, 255, 0, 0.05);
  transform: scale(0.95);
  transform-origin: 50% 50%;
}

.invalid_hyp {
  filter: blur(0px);
  -webkit-filter: blur(0px);
  background-color: rgba(255, 0, 0, 0.05);
  transform: scale(0.9);
  transform-origin: 50% 50%;
  /* z-index: -1; */
}

/* width: var(--hyp_container_width); */
/* height: var(--hyp_container_height); */


</style>

<style scoped>
/* local styles */
</style>
