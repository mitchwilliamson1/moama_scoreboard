<template>
  <div v-if="scoreboards" class="h-100 w-100" style="background-color: black;">
    <div style="background-color: white">
      <!-- {{masterTwo}} -->
    </div>
    <div class="container p-0 h-100 w-100">
      <div class="row p-0 m-0 align-items-center" style="height:8%">
        <div class="col p-0 m-0 txt">
          PENNANT
        </div>
        <div class="col p-0 m-0 txt">
          PENNANT
        </div>
      </div>
      <div class="row m-0 p-0" style="height:92%">
        <div class="col h-100 m-0 p-0 border bg-danger">
          <template v-for="board, rink in scoreboards">
            <div v-if="rink < 4" class="row border m-0 p-0 bg-danger" style="height:33.33%">
              <SidewaysBPL v-if="board.competition == 'BPL'" class="row m-0 p-0" :rink="rink" :detail="board"/>
              <SidewaysScoreboard v-else class="row m-0 p-0" :rink="rink" :detail="board"/>
            </div>
          </template>
        </div>
        <div class="col h-100 m-0 p-0 h-100 border bg-warning">
          <SidewaysMasterboard class="row m-0 p-0 h-100" :masterboard="masterOne"/>
        </div>
        <div class="col h-100 m-0 p-0 border bg-success">
          <template v-for="board, rink in scoreboards">
            <div v-if="rink > 3" class="row border m-0 p-0 bg-success" style="height:33.33%">
              <SidewaysBPL v-if="board.competition == 'BPL'" class="row m-0 p-0" :rink="rink" :detail="board"/>
              <SidewaysScoreboard v-else class="row m-0 p-0" :rink="rink" :detail="board"/>
            </div>
          </template>
        </div>
        <div class="col h-100 m-0 p-0 h-100 border bg-primary">
          <SidewaysMasterboard class="row m-0 p-0 h-100" :masterboard="masterTwo"/>
        </div>
        
      </div>

    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'
import SidewaysScoreboard from './SidewaysScoreboard.vue'
import SidewaysMasterboard from './SidewaysMasterboard.vue'
import SidewaysBPL from './SidewaysBPL.vue'

export default {
  name: 'Backboard',
  props: {
    scoreboards: Object,
    masterboard: Object,
  },
  components: {
    SidewaysScoreboard,
    SidewaysMasterboard,
    SidewaysBPL,
  },

  data(){
    return{
      path: "",
      masterboardOne: {
        'coordinator_ip':'',
        'ends':0,
        'competitors':{
            '1':{
                'score':0,
                "logo": "moama_steamers.png"
            },
            '2':{
                'score':0,
                "logo": "away.jpeg"
            },
          }
        },
      masterboardTwo: {
        'coordinator_ip':'',
        'ends':0,
        'competitors':{
            '1':{
                'score':0,
                "logo": "moama_steamers.png"
            },
            '2':{
                'score':0,
                "logo": "away.jpeg"
            },
          }
        },
    }
  },
  computed: {
    masterOne() {
      var endsOne = 0

      var masterOnePlayerOneScore = 0
      var masterOnePlayerTwoScore = 0

      for (const [key, board] of Object.entries(this.scoreboards)) {
        if (key < 4){
          this.masterboardOne['coordinator_ip'] = board.coordinator_ip
          endsOne += board.ends
          for (const [key, value] of Object.entries(board.competitors)){
            if (key == 1){
              masterOnePlayerOneScore += parseInt(value.score)
              this.masterboardOne.competitors[key]['logo'] = value.logo
            }else if (key == 2){
              masterOnePlayerTwoScore += parseInt(value.score)
              this.masterboardOne.competitors[key]['logo'] = value.logo
            }
          }
        }
      }
      this.masterboardOne['ends'] = endsOne

      this.masterboardOne.competitors[1]['score'] = masterOnePlayerOneScore
      this.masterboardOne.competitors[2]['score'] = masterOnePlayerTwoScore

      return this.masterboardOne
    },
    masterTwo() {
      var endsTwo = 0

      var masterTwoPlayerOneScore = 0
      var masterTwoPlayerTwoScore = 0

      for (const [key, board] of Object.entries(this.scoreboards)) {
        if (key > 3){
          this.masterboardTwo['coordinator_ip'] = board.coordinator_ip
          endsTwo += board.ends
          for (const [key, value] of Object.entries(board.competitors)){
            if (key == 1){
              masterTwoPlayerOneScore += parseInt(value.score)
              this.masterboardTwo.competitors[key]['logo'] = value.logo
            }else if (key == 2){
              masterTwoPlayerTwoScore += parseInt(value.score)
              this.masterboardTwo.competitors[key]['logo'] = value.logo
            }
          }
        }
      }
      this.masterboardTwo['ends'] = endsTwo

      this.masterboardTwo.competitors[1]['score'] = masterTwoPlayerOneScore
      this.masterboardTwo.competitors[2]['score'] = masterTwoPlayerTwoScore

      return this.masterboardTwo
    },
  },
  setup() {
    const state = reactive({
      data: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8083/'
    }else{
      path = window.location.toString();
    }

    onMounted(async () => {
    })

    function getScoreboards() {
      axios.get(path+'get_scoreboards')
      .then(function (response) {
        if (response.status == 200){
          state.data = response.data
          this.updateMasterboardOne()
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {
        setTimeout(getScoreboards, 1000)
      });
    }

    return {
      path,
      state
    };
  },
  methods:{
    addRow() {
      (async () => {
      const Response = await fetch(this.path+'/add_row', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
      })
      const addContent = await Response.json();
      console.log(addContent);
      })();
    },
    tabSelect(id) {
      for (const tab in this.selected){
        console.log(tab, id)
        if (id == tab){
          this.selected[tab] = true
        } else {
          this.selected[tab] = false
        }
      }
    },
  },
}
</script>
<style scoped type="text/css">
.container {
  max-width: 100%;
  /*margin: 0%;*/
}
.row {
  max-width: 100%;
  /*margin: 0%;*/
}
.txt {
  font-family: bigText;
  color: lime;
  font-size: 6vh;
  text-align: center;
  line-height: 1.0;
}
</style>
