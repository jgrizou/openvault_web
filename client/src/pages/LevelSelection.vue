<template>
  <div>
    <div class="level-selector" v-for="(row, i) of configs" :key="i">
      <a :href="get_link(i)">{{ row.message }}</a>
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
    get_link: function (i) {
      return `#/ui/${this.configs[i].filename}`
    }
  },
  mounted() {
    this.$socket.emit('get_configs')

    // to overwrite overflow-y: hidden from body and wrapper needed for disabling moble refresh by pull down
    var all = document.getElementsByClassName('body');
    for (var i = 0; i < all.length; i++) {
      all[i].style.overflowY = 'auto';
    }

    var all = document.getElementsByClassName('wrapper');
    for (var i = 0; i < all.length; i++) {
      all[i].style.overflowY = 'auto';
    }

  }
}
</script>


<style>
/* global styles */

.level-selector {
  text-align: center;
  margin-top: 10px;
}

</style>

<style scoped>
/* local styles */
</style>
