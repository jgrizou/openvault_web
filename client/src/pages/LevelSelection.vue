<template>
  <div>
      <b-container class="text-center" fluid>
        <b-row v-for="(row, i) of configs" :key="i">
          <b-col>
            <b-button v-on:click="onClick(i)">{{ row.message }}</b-button>
          </b-col>
        </b-row>
      </b-container>
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
    connect: function () {
      console.log('## Socket connected')
    },
    disconnect: function () {
      console.log('## Socket disconnected')
    },
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
</style>

<style scoped>
/* local styles */

.row {
  margin-bottom: 10px;
}

</style>
