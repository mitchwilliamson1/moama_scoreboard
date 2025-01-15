<template>
  <div v-if="state.data" class="h-100 w-100" style="background-color: black;">
    <BPLLayout v-if="state.data['layout'] == 'BPL'" 
        :scoreboards="state.data['scoreboards']" />
    <BowlsLayout v-else-if="state.data['layout'] == 'General Scoreboard (8) Rinks'" 
        :scoreboards="state.data['scoreboards']" />
    <FourRinkLayout v-else-if="state.data['layout'] == 'Premier Pennant (4) Rinks & Masterboard'" 
        :scoreboards="state.data['scoreboards']" 
        :masterboard="state.data['masterboard']" />
    <TwoByThreeRinkAndMaster v-else-if="state.data['layout'] == '(2) Pennant Games with (3) Rinks & Masterboard'" 
        :scoreboards="state.data['scoreboards']" 
        :masterboard="state.data['masterboard']" />
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'
import BPLLayout from './BPLLayout.vue'
import BowlsLayout from './BowlsLayout.vue'
import FourRinkLayout from './FourRinkLayout.vue'
import TwoByThreeRinkAndMaster from './TwoByThreeRinkAndMaster.vue'

export default {
  name: 'Backboard',
  components: {
    BPLLayout,
    BowlsLayout,
    FourRinkLayout,
    TwoByThreeRinkAndMaster,
  },

  data(){
    return{
      path: "",
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
      getScoreboards()
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
    post() {
      (async () => {
      const rawResponse = await fetch(this.path+'/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: JSON.stringify(this.state)
      })
      const content = await rawResponse.json();
      console.log(content);
      })();
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
