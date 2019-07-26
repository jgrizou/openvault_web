<template>
  <div>

    <transition name="loader-delayed">
      <div v-if="delayed_show">
        <div class="loader">
          <div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
        </div>
      </div>
    </transition>

    <transition name="loader-immediate">
      <div v-if="immediate_show">
        <div class="loader">
          <div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>

export default {
  name: "Loader",
  data() {
    return {
      delayed_show: false,
      immediate_show: false,
      last_loading_onset_time: undefined
    }
  },
  mounted () {
    this.show_no_delay()
  },
  methods: {
    show_no_delay: function () {
      this.delayed_show = false
      this.immediate_show = true
      this.reset_loading_timer()
    },
    show_with_delay: function () {
      this.delayed_show = true
      this.immediate_show = false
      this.reset_loading_timer()
    },
    hide: function () {
      this.delayed_show = false
      this.immediate_show = false
    },
    reset_loading_timer: function () {
      this.last_loading_onset_time = new Date();
    },
    is_loading: function () {
      return this.delayed_show || this.immediate_show
    },
    get_loading_duration_ms: function () {
      if ( this.is_loading() ) {
        return new Date() - this.last_loading_onset_time; //in ms
      } else {
        return 0
      }
    }
  }
}

</script>

<style>
/* global styles */


.loader {
  position: absolute;
  top: var(--display_height);
  left: 0px;
  width: var(--screen_width);
  height: var(--digit_height);
  background-color: rgba(255, 255, 255, 0.5);
}


.loader-delayed-enter-active {
  transition: opacity 1.5s cubic-bezier(0.95, 0.05, 0.795, 0.035);
}

.loader-delayed-leave-active {
  transition: opacity .5s ease;
}

.loader-delayed-enter, .loader-delayed-leave-to {
  opacity: 0;
}


.loader-immediate-enter-active {
  transition: opacity 0s ease;
}

.loader-immediate-leave-active {
  transition: opacity .5s ease;
}

.loader-immediate-enter, .loader-immediate-leave-to {
  opacity: 0;
}


/* inspired from https://loading.io/css/ */

:root {
  --spiner_diameter: var(--digit_height);
  --spiner_transform_xy: calc( var(--spiner_diameter) / 2);
  --spiner_color: rgba(100, 100, 100, 1);

  --spiner_blade_top: 0px;
  --spiner_blade_left: calc( (var(--spiner_diameter) - var(--spiner_blade_width)) / 2);
  --spiner_blade_width: calc( var(--spiner_diameter) / 10);
  --spiner_blade_height: calc( var(--spiner_diameter) / 4);
}

.lds-spinner {
  position: absolute;
  display: inline-block;
  top: calc( (var(--digit_height) - var(--spiner_diameter)) / 2 );
  left: calc( (var(--screen_width) - var(--spiner_diameter)) / 2 );
  width: var(--spiner_diameter);
  height: var(--spiner_diameter);
}

.lds-spinner div {
  transform-origin: var(--spiner_transform_xy) var(--spiner_transform_xy);
  animation: lds-spinner 1.2s linear infinite;
}

.lds-spinner div:after {
  content: " ";
  display: block;
  position: absolute;
  top: var(--spiner_blade_top);
  left: var(--spiner_blade_left);
  width: var(--spiner_blade_width);
  height: var(--spiner_blade_height);
  border-radius: 20%;
  background: var(--spiner_color);
}
.lds-spinner div:nth-child(1) {
  transform: rotate(0deg);
  animation-delay: -1.1s;
}
.lds-spinner div:nth-child(2) {
  transform: rotate(30deg);
  animation-delay: -1s;
}
.lds-spinner div:nth-child(3) {
  transform: rotate(60deg);
  animation-delay: -0.9s;
}
.lds-spinner div:nth-child(4) {
  transform: rotate(90deg);
  animation-delay: -0.8s;
}
.lds-spinner div:nth-child(5) {
  transform: rotate(120deg);
  animation-delay: -0.7s;
}
.lds-spinner div:nth-child(6) {
  transform: rotate(150deg);
  animation-delay: -0.6s;
}
.lds-spinner div:nth-child(7) {
  transform: rotate(180deg);
  animation-delay: -0.5s;
}
.lds-spinner div:nth-child(8) {
  transform: rotate(210deg);
  animation-delay: -0.4s;
}
.lds-spinner div:nth-child(9) {
  transform: rotate(240deg);
  animation-delay: -0.3s;
}
.lds-spinner div:nth-child(10) {
  transform: rotate(270deg);
  animation-delay: -0.2s;
}
.lds-spinner div:nth-child(11) {
  transform: rotate(300deg);
  animation-delay: -0.1s;
}
.lds-spinner div:nth-child(12) {
  transform: rotate(330deg);
  animation-delay: 0s;
}
@keyframes lds-spinner {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

</style>

<style scoped>
/* local styles */
</style>
