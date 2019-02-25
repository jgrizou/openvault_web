<template>
  <div>
      <b-container class="text-center" fluid>
        <b-row>
          <b-col>
            <b-button v-on:click="onClick">Back to level selection</b-button>
          </b-col>
        </b-row>
      </b-container>
  </div>
</template>


<script>
export default {
  name: 'VaultControl',
  components: {},
  data() {
    return {
    };
  },
  methods: {
    onClick: function (i) {
      this.$router.push({ path: '/'});
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
