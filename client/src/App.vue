<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>

:root {
  --screen_width: 480px;
  --screen_height: 800px;
  --display_height: 200px;
  --digit_height: 150px;
  --pad_height: calc( var(--screen_height) - var(--display_height) - var(--digit_height));

  --on_color: rgba(160, 160, 160, 0.85);
  --on_color_active: rgba(110, 110, 110, 0.85);
  --on_shadow_color: rgba(110, 110, 110, 0.85);
  --on_shadow_color_active: rgba(60, 60, 60, 0.85);

  --off_color: rgba(255, 200, 0, 0.85);
  --off_color_active: rgba(200, 150, 0, 0.85);
  --off_shadow_color: rgba(200, 150, 0, 0.85);
  --off_shadow_color_active: rgba(150, 100, 0, 0.85);

  --neutral_color: rgba(66, 65, 78, 1);
  --neutral_color_active: rgba(47, 46, 57, 1);
  --neutral_color_shadow: rgba(20, 20, 20, 1);
  --neutral_color_shadow_active: rgba(0, 0, 0, 1);

  --shadow_full: 12px;
  --shadow_min: 3px;
  --shadow_diff: calc( var(--shadow_full) - var(--shadow_min) );

  --btn_spacing: 10px;
}

#app {
  position: fixed;
  left: 0px;
  top: 0px;
  width: var(--screen_width);
  height: var(--screen_height);
  font-family: "Avenir";
}

.noflash {
  background-color: var(--off_color);
  box-shadow: 0 var(--shadow_full) var(--off_shadow_color);
}

.noflash:active {
  background-color: var(--off_color_active);
  box-shadow: 0 var(--shadow_min) var(--off_shadow_color_active);
}

.flash {
  background-color: var(--on_color);
  box-shadow: 0 var(--shadow_full) var(--on_shadow_color);
}

.flash:active {
  background-color: var(--on_color_active);
  box-shadow: 0 var(--shadow_min) var(--on_shadow_color_active);
}

.neutral {
  background-color: var(--neutral_color);
  box-shadow: 0 var(--shadow_full) var(--neutral_color_shadow);
}

.neutral:active {
  background-color: var(--neutral_color_active);
  box-shadow: 0 var(--shadow_min) var(--neutral_color_shadow_active);
}

.btn {
  border-radius: 15px;
  /* cursor: url(./assets/hand.svg) 10 10, pointer; */
}

.btn:active {
  transform: translateY(var(--shadow_diff));
  /* cursor: url(./assets/hand_click.svg) 10 10, pointer; */
}

.fullscreen {
  position: absolute;
  top: 0px;
  width: var(--screen_width);
  height: var(--screen_height);
  background-color: rgba(255, 255, 255, 1);
}

.display {
  position: absolute;
  top: 0px;
  width: var(--screen_width);
  height: var(--display_height);
  background-color: rgba(255, 255, 255, 1);
}

.digit {
  position: absolute;
  top: var(--display_height);
  width: var(--screen_width);
  height: var(--digit_height);
  background-color: rgba(255, 255, 255, 1);
}

.pad {
  position: absolute;
  top: calc( var(--display_height) + var(--digit_height) );
  width: var(--screen_width);
  height: var(--pad_height);
  background-color: rgba(255, 255, 255, 1);
}

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
}


</style>
