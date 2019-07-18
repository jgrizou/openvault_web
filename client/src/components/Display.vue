<template>
  <div>
    <div v-for="(item, index) in code">
      <div :class="{
        'tile': true,
        ['c' + index]: true,
        'found': item['found'],
        'ongoing': item['ongoing'],
        'noselect': true
        }"
      >
        {{ item['text'] }}
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: 'Display',
  data() {
    return {
      code: [
        {'found': false, 'ongoing': false, 'text': ''},
        {'found': false, 'ongoing': false, 'text': ''},
        {'found': false, 'ongoing': false, 'text': ''},
        {'found': false, 'ongoing': false, 'text': ''}
      ]
    }
  }
}

</script>

<style>
/* global styles */

:root {
  --tile_width: 80px;
  --tile_height: 100px;
  --tile_top_offset: 50px;
  --tile_side_offset: 70px;
  --tile_spacing: calc( ( (var(--screen_width) - 2*var(--tile_side_offset)) - 4*var(--tile_width)) / 3 );
  --tile_color: rgba(255, 204, 204, 1);
  --tile_border: 10px;
}

.tile {
  position: absolute;
  width: var(--tile_width);
  height: var(--tile_height);
  border-radius: 0px; /* rounding */
  text-align: center;
  vertical-align: middle;
  font-size: 70px;
  font-weight: 700;
  line-height: var(--tile_height);
  background-color: var(--tile_color);
}

.ongoing {
  width: calc( var(--tile_width) - 2*var(--tile_border) );
  height: calc( var(--tile_height) - 2*var(--tile_border) );
  line-height: calc( var(--tile_height) - var(--tile_border) );
  border-width: var(--tile_border);
  border-style: solid;
  border-color: rgba(50, 50, 50, 1);
  background-color: rgba(255, 224, 224, 1);
}

.found {
  background-color: rgba(255, 224, 224, 1);
}

.c0 {
  top: var(--tile_top_offset);
  left: calc( var(--tile_side_offset) + 0 * (var(--tile_width) + var(--tile_spacing)) );
}

.c1 {
  top: var(--tile_top_offset);
  left: calc( var(--tile_side_offset) + 1 * (var(--tile_width) + var(--tile_spacing)) );
}

.c2 {
  top: var(--tile_top_offset);
  left: calc( var(--tile_side_offset) + 2 * (var(--tile_width) + var(--tile_spacing)) );
}

.c3 {
  top: var(--tile_top_offset);
  left: calc( var(--tile_side_offset) + 3 * (var(--tile_width) + var(--tile_spacing)) );
}


</style>

<style scoped>
/* local styles */
</style>
