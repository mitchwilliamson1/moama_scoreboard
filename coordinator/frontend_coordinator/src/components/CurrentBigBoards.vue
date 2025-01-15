<template>
  <div class="container">
    <div class="row">
      <h3 class="p-3">Big Board Setup</h3>
    </div>

    <div v-for="bigboard, i in bigboards" :key="i">
      <div class="row shadow p-2 mb-1 bg-body rounded"
        data-bs-toggle="collapse" 
        :data-bs-target="'#collapseTeam'+i" 
        aria-expanded="false" 
        aria-controls="collapseOne">
        <div class="col">{{bigboard.bigboard}} - Currently setup for {{bigboard.current_layout.layout}}</div>
      </div>
      <div class="row p-2">
        <div class="col collapse"
          :id="'collapseTeam'+i"
          data-parent="#accordion">
          <edit-bigboard :rinks="rinks" :layouts="layouts" :bigboard="bigboard"/>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import EditBigboard from '../components/EditBigboard.vue'


export default {
  name: 'CurrentRinks',
  components: {
    EditBigboard,
  },
  props: {
    bigboards: Object,
    rinks: Object,
    layouts: Object,
  },

  setup() {
    const state = reactive({
      someData: null,
    });

    onMounted(async () => {});

    return {
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
    post() {
      (async () => {
      const rawResponse = await fetch('http://127.0.0.1:8000/save', {
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
    edit(game) {
      console.log(game)
    },
  },
}
</script>

<style scoped>

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

h3 {
  margin: 40px 0 0;
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
