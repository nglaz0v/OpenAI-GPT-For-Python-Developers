<template>
  <div>
    <h2>DrugBot</h2>
    <div v-if="messages.length">
	  <div v-for="message in messages" :key="message.id">
	    <strong>{{ message.author }}:</strong> {{ message.text }}
	  </div>
    </div>
    <form @submit.prevent="sendMessage">
	  <input type="text" v-model="newMessage" placeholder="Введите ваше сообщение">
	  <button type="submit">Send</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
	  messages: [
	    { id: 1, author: "ИИ", text: "Привет, чем я могу помочь?" },
	  ],
	  newMessage: "",
     };
    },
    methods: {
      sendMessage() {
	    if (this.newMessage.trim() === "") {
	      return;
	    }
	    this.messages.push({
	      id: this.messages.length + 1,
	      author: "Человек",
	      text: this.newMessage.trim(),
	    });

	    const messageText = this.newMessage.trim();

	    axios.get(`http://127.0.0.1:5000/?m=${encodeURI(messageText)}`)
	    .then(response => {
	      const message = {
		  id: this.messages.length + 1,
		  author: "ИИ",
		  text: response.data.m
	    };
	    this.messages.push(message);
	  })
	  .catch(error => {
	   console.error(error);
	    this.messages.push({
		  id: this.messages.length + 1,
		  author: "ИИ",
		  text: "Извините, я не понимаю.",
	    });
	  });

	 this.newMessage = "";
   },
 },
};
</script>
