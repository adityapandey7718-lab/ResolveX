let currentTicketId = null;
const messageInput = document.getElementById("message");
const chatForm = document.getElementById("chatForm");
const submitBtn = document.getElementById("submitBtn");
const resultDiv = document.getElementById("result");
const errorAlert = document.getElementById("errorAlert");
const charCountSpan = document.getElementById("charCount");

// Character counter
messageInput.addEventListener("input", function() {
    charCountSpan.textContent = this.value.length;
});

// Form submission
chatForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    closeAlert("errorAlert");

    const message = messageInput.value.trim();

    // Validation
    if (!message) {
        showError("Please enter a message before sending.");
        return;
    }

    if (message.length < 10) {
        showError("Please provide more details (at least 10 characters).");
        return;
    }

    // Show loading state
    setLoading(true);

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }

        const data = await res.json();

        if (!data.ticket_id || !data.intent || !data.response) {
            throw new Error("Invalid response format from server.");
        }

        currentTicketId = data.ticket_id;

        // Display results
        document.getElementById("intent").innerText = data.intent.charAt(0).toUpperCase() + data.intent.slice(1);
        document.getElementById("response").innerText = data.response;

        resultDiv.classList.remove("hidden");
        resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch (error) {
        console.error("Error:", error);
        showError("Failed to get response. Please try again.");
    } finally {
        setLoading(false);
    }
});

async function sendFeedback(helpful) {
    if (!currentTicketId) {
        showError("Error: No ticket ID found.");
        return;
    }

    // Disable feedback buttons
    disableFeedbackButtons(true);

    try {
        const res = await fetch("/feedback/" + currentTicketId, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ helpful: helpful })
        });

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }

        // Show success message
        const feedbackSection = document.querySelector(".feedback-section");
        const originalContent = feedbackSection.innerHTML;
        feedbackSection.innerHTML = `
            <div style="text-align: center; color: #10b981; font-weight: 600;">
                ✓ Thank you for your feedback! The model is being updated...
            </div>
        `;

        // Restore feedback section after 3 seconds
        setTimeout(() => {
            feedbackSection.innerHTML = originalContent;
            disableFeedbackButtons(false);
        }, 3000);
    } catch (error) {
        console.error("Error sending feedback:", error);
        showError("Failed to send feedback. Please try again.");
        disableFeedbackButtons(false);
    }
}

function resetChat() {
    messageInput.value = "";
    charCountSpan.textContent = "0";
    resultDiv.classList.add("hidden");
    currentTicketId = null;
    closeAlert("errorAlert");
    messageInput.focus();
}

function showError(message) {
    document.getElementById("errorMessage").innerText = message;
    errorAlert.classList.remove("hidden");
}

function closeAlert(alertId) {
    document.getElementById(alertId).classList.add("hidden");
}

function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    const spinner = submitBtn.querySelector(".spinner");
    const btnText = submitBtn.querySelector(".btn-text");

    if (isLoading) {
        spinner.classList.remove("hidden");
        btnText.textContent = "Sending...";
    } else {
        spinner.classList.add("hidden");
        btnText.textContent = "Send Message";
    }
}

function disableFeedbackButtons(disabled) {
    document.getElementById("feedbackYes").disabled = disabled;
    document.getElementById("feedbackNo").disabled = disabled;
}

// Set initial focus
messageInput.focus();