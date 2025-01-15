<template>
  <div class="h-100 w-100" style="background-color: black;">
    <div class="container p-0 h-100 w-100">
      <div class="row h-100 w-100 m-0 p-0">
        <div class="col-1 m-0 p-0 h-100">
          <div class="row align-items-center h-50 m-0">
            <div class="" style="height: 30%; text-align: center; color: lime; font-weight: bold; font-size: 3vh;">Bowls</div>
            <div class="" style="height: 20%; text-align: center; color: yellow; font-weight: bold; font-size: 3vh;">SCORE</div>
            <div class="" style="height: 15%; text-align: center; color: white; font-weight: bold; font-size: 3vh">ENDS</div>

          </div>
          <div class="row align-items-center h-50 m-0">
            <div class="" style="height: 30%; text-align: center; color: lime; font-weight: bold; font-size: 4vh;"></div>
            <div class="" style="height: 20%; text-align: center; color: yellow; font-weight: bold; font-size: 3vh;">SCORE</div>
            <div class="" style="height: 15%; text-align: center; color: white; font-weight: bold; font-size: 3vh">ENDS</div>
          </div>
        </div>
        <div class="col m-0 p-0 h-100">
          <div class="row m-0 p-0 h-100">
            <div v-for="board, rink in scoreboards" class="col-3 border border-light m-0 p-0 h-50">
              <BPL v-if="board.competition == 'BPL'" class="row m-0 p-0" :rink="rink" :detail="board"/>
              <Scoreboard v-else class="row m-0 p-0" :rink="rink" :detail="board"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'
import Scoreboard from './Scoreboard.vue'
import BPL from './BPL.vue'

export default {
  name: 'Backboard',
  props: {
    scoreboards: Object,
  },
  components: {
    Scoreboard,
    BPL,
  },

  data(){
    return{
      path: "",
      blah:[1,2,3,4,5,6]
    }
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
</style>
