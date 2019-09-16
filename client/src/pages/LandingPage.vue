<template>
  <iframe
    class="iframe-fullpage"
    src="https://jgrizou.com/projects/vault/quickaccess/"
  >
  </iframe>
</template>


<script>
export default {
  name: 'LandingPage',
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

.iframe-fullpage{
  position: fixed;
  top: 0px;
  bottom: 0px;
  right: 0px;
  width: 100%;
  border: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  z-index: 999999;
  height: 100%;
}

</style>

<style scoped>
/* local styles */
</style>
