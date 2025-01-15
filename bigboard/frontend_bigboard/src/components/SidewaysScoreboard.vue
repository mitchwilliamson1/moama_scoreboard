<template>
  <div v-if="detail" class="container-fluid h-100 w-100 p-0" style="background-color: black;">
    <div class="container-fluid w-100 h-100 d-flex flex-column">
      <h1 class="row justify-content-center text-info p-0 m-0" style="height: 12%; font-weight: bold;">{{rink}}</h1>

      <div class="row m-0 p-0 align-items-center" style="height: 40%;">
        <div v-for="competitor in detail.competitors" class="col-6 m-0 p-0" style="height: 85%">
          <template v-if="detail.coordinator_running" >
            <img v-if="competitor.display == 'Logo'"
              class="logo"
              :src="'http://'+detail.coordinator_ip+'/players/get_logo/'+competitor.logo">
            <div v-else-if="competitor.display == 'First Initial'"
              class="txt">{{competitor.first_name.charAt(0)}}</div>
            <div v-else-if="competitor.display == 'Fist and Last Initial'"
              class="txt">{{competitor.first_name.charAt(0)}}{{competitor.last_name.charAt(0)}}</div>
            <img v-else="competitor.display == 'Default'" class="logo"
              :src="'http://127.0.0.1:8081/'+competitor.default_logo">
          </template>
          <template v-else>
            <div v-if="competitor.display == 'first name'"
              class="txt">{{competitor.first_name.charAt(0)}}</div>
            <div v-else-if="competitor.display == 'Fist and Last Initial'" 
              class="txt">{{competitor.first_name.charAt(0)}}{{competitor.last_name.charAt(0)}}</div>
            <img v-else="competitor.display == 'Default'" 
              class="logo" :src="'http://127.0.0.1:8081/'+competitor.default_logo">
          </template>
        </div>
      </div>

      <div class="row m-0 p-0 align-items-center" style="min-height: 25%;">
        <div v-for="competitor in detail.competitors" class="col p-0 align-self-center">
          <Ticker :number="competitor.score.toString()" 
                    fontSize="9"
                    fontColour="yellow"/>
        </div>
      </div>

      <div class="row m-0 p-0 align-items-center overflow-hidden" style="height: 33%;">
        <div class="col">
          <Ticker :number="detail.ends.toString()"
                  fontSize="7"
                  fontColour="white"/>
        </div>
      </div>

    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'
import axios from 'axios'
import { reactive, onMounted } from "vue";


export default {
  name: 'Board',
  props: {
    detail: Object,
    rink: String,
  },
  components: {
    Ticker,
  },
  data() {
    return {
      // game: null,
    }
  },
  watch: {
    // details() {
    //   this.updateGame();
    // },
  },
  computed: {
  },
  methods: {
    isMobile() {
     if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
       return true
     } else {
       return false
     }
   }
    // updateGame() {
    //   this.game = this details
    // },
  },

}
</script>

<style scoped type="text/css">
@font-face {
  font-family: bigText;
  src: url(../assets/fonts/ebrima-bold.ttf);
}

.row {
  background-color: black;
}

.txt {
  font-family: bigText;
  color: white;
  font-size: 16vh;
  text-align: center;
  line-height: 1.0;
}

.ends {
  font-family: bigText;
  color: white;
  text-align: center;
  line-height: 1.0;
}

.logo {
  background-color: white;
  padding: 0px;
  margin: 0px;
  /*top: 10%;*/
  aspect-ratio: 4/3;
  position: relative;
  height: 100%;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.add {
  /*background-color: white;*/
  position: relative;
  /*height: 100%;*/
  display: block;
  margin-left: auto;
  margin-right: auto;

  background-size:contain;
  background-repeat: no-repeat;
  background-position: center center;
  height: 100%;

}


</style>
