<template>
  <div class="text-center">

    <codeModal ref="codeModal" :callback="modal_callback"></codeModal>

    <b-container class="passwordui" fluid>

      <panel ref="display" index="display" ></panel>
      <br>
      <panel ref="code" index="code"></panel>
      <br>
      <panel ref="pad" index="pad" :callback="pad_callback"></panel>
      <br>

      <b-container class="text-center" fluid>
        <b-row>
          <b-col>
            <b-button v-on:click="reset">
              <b-badge pill variant="light">{{ n_iteration }}</b-badge>
              Reset
            </b-button>
          </b-col>
          <b-col>
            <router-link :to="{ name: 'LevelSelection'}">
              <b-button>
                Level selection
              </b-button>
            </router-link>
          </b-col>
          <b-col>
            <b-button @click="emit_success">Success</b-button>
            <b-button @click="emit_fail">Failure</b-button>
          </b-col>
        </b-row>
      </b-container>

    </b-container>
  </div>
</template>

<script>
import Panel from './../components/Panel.vue'
import CodeModal from './../components/CodeModal.vue'

export default {
  name: 'PasswordUI',
  components: { Panel, CodeModal },
  data() {
    return {
      n_iteration: 0,
      success: undefined
    };
  },
  sockets: {
    connect: function () {
      console.log('## Socket connected')
      this.$socket.emit('is_spawn')
    },
    disconnect: function () {
      console.log('## Socket disconnected')
    },
    grid: function (data) {
      var child = this.$refs[data.panel_index]
      child.grid = data.grid
    },
    n_iteration: function (n_iteration) {
      this.n_iteration = n_iteration
    },
    spawn_state: function (state) {
      if (!state) {
        this.spawn_learner()
      }
    },
    modal: function (data) {
      this.success = data.success
      this.$refs.codeModal.show(data)
    }
  },
  methods: {
    reset: function () {
      this.$socket.emit('reset')
    },
    spawn_learner: function () {
      // spawn the learner given link given in url
      this.$socket.emit('spawn_learner', this.$route.params.pathMatch)
    },
    pad_callback: function (data) {
      var click_info = {}
      click_info.panel_index = data.panel_component.index
      click_info.tile_index = data.tile_component.index
      click_info.relative_click = data.relative_click
      click_info.display_grid = this.$refs.display.grid
      this.$socket.emit('click', click_info)
    },
    emit_success: function (data) {
      this.$socket.emit('success')
    },
    emit_fail: function (data) {
      this.$socket.emit('fail')
    },
    modal_callback: function () {
      if (this.success) {
        this.$router.push({ path: '/'})
      } else {
        this.reset()
      }
    }
  },
  mounted() {
    window.addEventListener('keypress', (event) => {
      var key_info = {}
      key_info.key = String.fromCharCode(event.keyCode)
      key_info.display_grid = this.$refs.display.grid
      this.$socket.emit('key', key_info)
    });
    // spawn the learner given link given in url
    this.spawn_learner()
  }
}
</script>


<style>
/* global styles */

.container {
  border: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.row {
  border: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.col {
  border: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.passwordui {
  max-width: 30rem;
}

</style>

<style scoped>
/* local styles */
</style>
