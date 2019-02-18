<template>
    <b-img
      fluid-grow
      center
      class="pad"
      v-bind:ref="'pad_' + index"
      v-on:click="onClick('pad_' + index, $event)"
      v-bind:src="src"
      v-bind:blank="blank"
      v-bind:blank-color="color"
    >
    </b-img>
</template>

<script>
export default {
  name: 'Pad',
  props: {
    index: String,
    blank: {
      type: Boolean,
      default: true
    },
    color: {
      type: String,
      default: 'rgba(128, 128, 128, 0.5)'
    },
    src: {
      type: String,
      default: ""
    }
  },
  methods: {
    onClick: function (ref, event) {
      // get position of pad
      var elem_data = this.$refs[ref].getBoundingClientRect()

      // compute relative position of click in pad
      var rel_click = {}
      rel_click.x = (event.clientX - elem_data.x) / elem_data.width
      rel_click.y = (event.clientY - elem_data.y) / elem_data.height

      // send info to callback in parent
      this.$parent.padCallback({index: this.index, click: rel_click})
    }
  }
}
</script>

<style>
/* global styles */

.pad {
  border: 2px solid black;
}

.pad:active {
  border: 2px solid red;
}

</style>

<style scoped>
/* local styles */
</style>
