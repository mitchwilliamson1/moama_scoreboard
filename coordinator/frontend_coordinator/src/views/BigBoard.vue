<template>
  <div class="home">
    <div class="row">

      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">New Big Board</div>

      <div class="offcanvas offcanvas-end w-50" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Big Board</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">

          <div class="row p-1">
            <div class="col-4">Big Board Name</div>
            <input class="col" v-model="createMasterboard.masterboard" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">IP Address</div>
            <input class="col" v-model="createMasterboard.ip" type="text">
          </div>

          <div class="">
            <button @click="createMasterboardButton(this.createMasterboard)" class="btn btn-success">Create Big Board</button>
          </div>
        </div>
      </div>

      <div class="row">
        <div v-if="state.bigboards" class="col-12">
          <current-big-boards :rinks="state.rinks" :layouts="state.layouts" :bigboards="state.bigboards"/>
        </div>
      </div>

      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import CurrentBigBoards from '../components/CurrentBigBoards.vue'
import axios from 'axios'
import { DateTime } from "luxon";

export default {
  name: 'PlayersView',
  components: {
    CurrentBigBoards,
  },
  data() {
    return {
      createRink: {
        'rink':null,
        'ip':null,
      },
      createMasterboard: {
        'masterboard':null,
        'ip':null,
      }
    }
  },
  setup() {
    const state = reactive({
      rinks: null,
      bigboards: null,
    });

    var path = ""
    path = 'http://127.0.0.1:8000/'
    
    onMounted(async () => { 
      getBigboards()
      getRinks()
      getLayouts()
    });
    function createMasterboardButton(masterboard) {
      axios.post(path+'games/create_bigboard', {
      create_masterboard: masterboard,
      })
      .then(function (response) {
        console.log(response);
        getMasterboards()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    function getBigboards() {
      axios.get(path+'games/get_bigboards')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.bigboards = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getRinks() {
      axios.get(path+'games/get_rinks')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.rinks = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getLayouts() {
      axios.get(path+'games/get_layouts')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.layouts = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }

    return {
      path,
      state,
      createMasterboardButton,
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>