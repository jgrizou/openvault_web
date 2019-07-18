<template>
  <div>

    <transition name="slide-reset">

      <div class="reset noselect" v-show="active">

        <div class="reset-text">
          Experience started
        </div>

        <button
          class="reset-btn"
          v-on:click="on_click"
          :disabled="!active">
            Restart
        </button>

      </div>

    </transition>

  </div>
</template>

<script>

export default {
  name: 'Reset',
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      n_iteration: 0,
      force_hide: false
    }
  },
  computed: {
    active: function () {
      return this.n_iteration > 0 && !this.force_hide
    }
  },
  sockets: {
    n_iteration: function (n_iteration) {
      this.n_iteration = n_iteration
    }
  },
  methods: {
    on_click: function () {
      this.callback()
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --reset_height: 20px
}

.reset {
  position: absolute;
  top: 0px;
  left: 0px;
  width: var(--screen_width);
  height: var(--reset_height);
  background-color: rgba(0, 0, 0, 1);
  font-size: 12px;
  font-weight: 400;
  color: rgba(255, 255, 255, 1);
}

.reset-btn {
  position: absolute;
  top: 2px;
  right: 5px;
  width: 60px;
  height: calc(var(--reset_height) - 4px);
  outline: none; /* remove contour when clicked */
  border: none;
  border-radius: 4px;
  color: rgba(255, 255, 255, 1);
  background-color: rgba(100, 100, 100, 1);
}

.reset-btn:hover {
  background-color: rgba(120, 120, 120, 1);
}

.reset-btn:active {
  background-color: rgba(150, 150, 150, 1);
}

.reset-text {
  position: absolute;
  top: 0px;
  left: 5px;
  line-height: var(--reset_height);
}

.slide-reset-enter-active {
  transition: all 1s ease-out;
}

.slide-reset-leave-active {
  transition: all .5s ease-in-out;
}

.slide-reset-enter, .slide-reset-leave-to {
  transform: translateY(-20px);
}

</style>

<style scoped>
/* local styles */
</style>
