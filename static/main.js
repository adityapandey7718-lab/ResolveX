let currentTicketId = null;

document.getElementById("chatForm").addEventListener("submit", async function(e) {

e.preventDefault();

let message = document.getElementById("message").value;

let res = await fetch("/chat", {

method: "POST",

headers: { "Content-Type": "application/json" },

body: JSON.stringify({ message: message })

});

let data = await res.json();

currentTicketId = data.ticket_id;

document.getElementById("intent").innerText = data.intent;

document.getElementById("confidence").innerText = data.confidence + "%";

document.getElementById("response").innerText = data.response;

document.getElementById("result").classList.remove("hidden");

});

async function sendFeedback(helpful) {

await fetch("/feedback/" + currentTicketId, {

method: "POST",

headers: { "Content-Type": "application/json" },

body: JSON.stringify({ helpful: helpful })

});

alert("Feedback recorded. Thank you!");

}