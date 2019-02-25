<template>
  <div>
    <b-modal
      ref="codeModal"
      centered
      no-close-on-esc
      no-close-on-backdrop
      hide-header-close
      hide-footer
    >

      <div v-if="success">
        <div class="d-block text-center">
          <h1>Hooray !!!  &#x1F973</h1>
          <b-img :src="gif" fluid-grow></b-img>
          <p>The code is indeed: {{ code }}<p>
        </div>
        <b-button
          variant="success"
          block
          v-on:click="modalCallback"
        >
          Go to vault control panel
        </b-button>
      </div>
      <div v-else>
        <div class="d-block text-center">
          <div v-if="inconsistent">
            <h1>Hmmm... &#x1F937</h1>
            <b-img :src="gif" fluid-grow></b-img>
            <p>Sounds like you got mixed up.<p>
          </div>
          <div v-else>
            <h1>Oh Noooooo &#x1F914</h1>
            <b-img :src="gif" fluid-grow></b-img>
            <p>Sorry, the code is not: {{ code }}<p>
          </div>
        </div>
        <b-button
          v-if="disabled"
          variant="outline-success"
          block
          disabled
          v-on:click="modalCallback"
        >
          Try again in
          <b-badge pill variant="light">{{ remainingTimeDisplay }}</b-badge> seconds
        </b-button>
        <b-button
          v-else
          variant="success"
          block
          v-on:click="modalCallback"
        >
          Try again now !
        </b-button>
      </div>

    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'CodeModal',
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  data: function () {
      return {
        success: undefined,
        inconsistent: undefined,
        code: undefined,
        gif: undefined,
        endTime: undefined,
        remainingTime: undefined,
        interval: undefined
    }
  },
  computed: {
    disabled: function () {
      return (this.remainingTime > 0)
    },
    remainingTimeDisplay: function () {
      return Math.max(0, Math.round(this.remainingTime / 1000))
    }
  },
  methods: {
    show: function (data) {
      this.success = data.success
      this.inconsistent = data.inconsistent
      this.code = data.code
      this.gif = data.gif

      var nowTime = new Date().getTime()
      this.remainingTime = 1000*data.pause_in_second
      this.endTime = new Date(nowTime + this.remainingTime)

      this.interval = setInterval(() => {
        this.timerCount()
      }, 1000)
      this.$refs.codeModal.show()
    },
    hide: function () {
      this.$refs.codeModal.hide()
    },
    modalCallback: function () {
      this.hide()
      if (this.success) {
        this.$router.push({ path: '/vaultcontrol'})
      } else {
        this.callback()
      }
    },
    timerCount: function() {
      var nowTime = new Date().getTime()
      this.remainingTime = this.endTime - nowTime
      if (this.remainingTime < 0) {
        clearInterval(this.interval)
      }
    }
  }
}
</script>

<style>
/* global styles */
</style>

<style scoped>
/* local styles */
</style>
