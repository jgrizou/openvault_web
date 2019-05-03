<template>
  <div>
    <div class="level-selector" v-for="(row, i) of configs" :key="i">
      <button class="level-button" v-on:click="onClick(i)">{{ row.message }}</button>
    </div>
  </div>
</template>


<script>
export default {
  name: 'LevelSelection',
  components: {},
  data() {
    return {
      configs: []
    };
  },
  sockets: {
    set_configs: function (configs){
      this.configs = configs
    }
  },
  methods: {
    onClick: function (i) {
      this.$router.push({ path: `/ui/${this.configs[i].filename}`});
    }
  },
  mounted() {
    this.$socket.emit('get_configs')
  }
}
</script>


<style>
/* global styles */

.level-selector {
  text-align: center;
  margin-top: 20px;
}

.level-button {
  display: inline-block;
  width: 200px;
  height: 50px;
  outline: none; /* remove contour when clicked */
  border: none;
  background-color: rgba(150, 150, 150, 1);
  color: black;
  font-size: 16px;
  text-align: center;
  text-decoration: none;
}

</style>

<style scoped>
/* local styles */
</style>
