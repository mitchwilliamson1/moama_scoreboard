<template>
  <div class="container-fluid h-100 w-100 p-0" style="background-color: black;">
      <div class="row m-0 p-0 align-items-center justify-content-between" style="height:70%">
        <div class="col p-2 m-0" style="height: 75%;">
          <img class="logo" :src="'http://'+masterboard['coordinator_ip']+'/players/get_logo/'+masterboard['competitors'][1]['logo']">
        </div>
        <div class="col p-0 ">
          <Ticker :number="masterboard['competitors'][1]['score'].toString()" 
                    fontSize="20"
                    fontColour="yellow"/>
        </div>
        <div class="col p-0 ">
          <Ticker :number="masterboard['competitors'][2]['score'].toString()" 
                    fontSize="20"
                    fontColour="yellow"/>
        </div>
        <div class="col p-2 m-0" style="height: 75%;">
          <img class="logo" :src="'http://'+masterboard['coordinator_ip']+'/players/get_logo/'+masterboard['competitors'][2]['logo']">
        </div>
      </div>

      <div class="row align-items-center h-25" style="height:30%">
        <div class="col p-0 align-self-center">
          <Ticker :number="masterboard['ends'].toString()" 
                    fontSize="10"
                    fontColour="white"/>
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
    masterboard: Object,
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

.count {
  font-family: clock-look;
  color: yellow;
  text-align: center;
  stroke: solid;
  background-color: black;
  line-height: 0.8;
}


</style>
