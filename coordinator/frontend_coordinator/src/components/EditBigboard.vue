<template>
  <div class="">
    <div class="card p-2 pt-0 shadow">
      <div class="row g-3">
        <div class="col-md-6">
          <h4 for="name" class="form-label">Big Board Name</h4>
          <input type="text" class="form-control" id="name" v-model="bigboard.bigboard">
        </div>
        <div class="col-md-6">
          <h4 for="ipAddress" class="form-label">IP Address</h4>
          <input type="text" class="form-control" id="ipAddress" v-model="bigboard.ip">
        </div>
      </div>

      <div class="row border rounded m-2">
        <div class="col">
          <h4>Current Layout</h4>
          <div v-for="layout, index in layouts" class="form-check-inline">
            <input type="radio" class="btn-check" name="options-outlined" :id="'inlineCheckbox'+index" autocomplete="off" :value="layout" v-model="bigboard.current_layout">
            <label class="btn btn-outline-secondary" :for="'inlineCheckbox'+index">{{layout.layout}}</label>
          </div>

        </div>
      </div>
      <div class="row">
        <div class="col">
          <button @click="updateLayout(bigboard)" type="submit" class="btn btn-primary">Update</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'

export default {
  name: 'Editbigboards',
  props: {
    bigboard: Object,
    rinks: Object,
    layouts: Object,
  },

  setup(props) {
    const state = reactive({
      ips: [],
    });

    var path = ""
    path = 'http://127.0.0.1:8000/games'

    onMounted(async () => {
      // getMasterboard()
      // getIpList()
    });
    function updateLayout(bigboard) {
      axios.post(this.path+'/update_layout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        update_layout: JSON.stringify(bigboard)
      })
      .then(function (response) {
        console.log(response);
        alert("Saved");
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    return {
      updateLayout,
      path,
      state
    };
  },
  data(){
    return{
      isActive: false,
    }
  },
  created () {
  },
  mounted () {
  },

  computed: {
    
  },

  methods:{
    // updateLayout(bigboard) {
    //   (async () => {
    //   const rawResponse = await fetch(this.path+'/update_layout', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     mode: 'no-cors',
    //     body: JSON.stringify(bigboard)
    //   })
    //   const content = await rawResponse;
    //   console.log(content);
    //   alert(content);
    //   })();
    // },
    addRemove(ip){
      console.log(ip)
      this.state.ips.push(ip)
    },
    addIP(){
      this.state.ips.push("")
    },
    removeIP(key){
      this.state.ips.splice(key, 1)
    },
  },
}
</script>

<style scoped>
.row{
  padding: 10px;
}

.flex-container {
  display: flex;
  justify-content: space-around;
}

.flex-child-spend {
  background-color: #b8fcbb;
  flex-grow: 1;
  border: 2px solid grey;
  margin: 5px;
  margin-top: 50px;
  margin-bottom: 80px;
  padding-bottom: 10px;
}

.flex-child {
  background-color: #e6dfcc;
  flex-grow: 1;
  border: 2px solid grey;
  margin: 2px;
}

input {
  width: 90%;
}

ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
