<template>
  <div>

    <div class="select-config">

      <select id="configs">
        <option v-for="(row, i) of configs" :key="i" :value ="get_link(i)">{{ row.message }}
        </option>
      </select>

      <button
        class="btn-config"
        v-on:click="on_submit">
          Open
      </button>

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
    },
    on_submit: function () {
      var select_elem = document.getElementById("configs");
      var selected_url = select_elem.options[select_elem.selectedIndex].value;
      this.redirect_to(selected_url)
    },
    redirect_to: function (url) {
      // https://stackoverflow.com/questions/13109233/how-to-redirect-and-reload-the-right-way-in-dart
      window.location.assign(url)
    },
  },
  mounted() {
    this.$socket.emit('get_configs')

    // to overwrite overflow-y: hidden from body and wrapper needed for disabling mobile refresh by pull down
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

.select-config {
  margin-top: 20px;
  text-align: center;
}

.btn-config {
  color: black;
  border: 2px solid rgba(150, 150, 150, 1);
  background-color: rgba(200, 200, 200, 1);
}

</style>

<style scoped>
/* local styles */
</style>
