<script>
export default {
  data() {
    return {
      name: 'MagicWand app - sigma version',
      status: 'active',
      tasks: ['lorem', 'ipsum', 'dolor'],
      link: 'https://www.put.poznan.pl',
    };
  },
  methods: {
    toggleStatus() { 
      if (this.status === 'active') {
        this.status = 'pending';
      }
      else if (this.status === 'pending') {
        this.status = 'inactive';
      }
      else {
        this.status = 'active';
      }
    },
  },
};
</script>

<template>
  <h1>{{ name }}</h1>
  <p v-if="status === 'active'">User is conntected.</p>
  <p v-else-if="status === 'pending'">User is pending.</p>
  <p v-else>User is inactive.</p>
  <h3>Rules:</h3>
  <ul>
    <li v-for="task in tasks" :key="task">{{ task }}</li>
  </ul>
  <br>
  <div>
    <img src="@/assets/spinning-cat.gif" alt="cat GIF" />
  </div>

  <button @click="toggleStatus">Change Status</button>
</template>

<style scoped>
  h1 {
    color: pink;
  }
</style>