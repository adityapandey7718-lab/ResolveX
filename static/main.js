<<<<<<< HEAD
let currentTicketId = null;
const messageInput = document.getElementById("message");
const chatForm = document.getElementById("chatForm");
const submitBtn = document.getElementById("submitBtn");
const resultDiv = document.getElementById("result");
const errorAlert = document.getElementById("errorAlert");
const charCountSpan = document.getElementById("charCount");
=======
﻿let currentTicketId = null;
let messageInput, chatForm, submitBtn, resultDiv, errorAlert, charCountSpan, themeToggle;

function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark');
        if (themeToggle) themeToggle.innerText = '☀️ Light Mode';
    } else {
        document.body.classList.remove('dark');
        if (themeToggle) themeToggle.innerText = '🌙 Dark Mode';
    }
    localStorage.setItem('resolvexTheme', theme);
}

function showError(message) {
    const errorMessageElm = document.getElementById('errorMessage');
    if (errorMessageElm) errorMessageElm.innerText = message;
    if (errorAlert) errorAlert.classList.remove('hidden');
}

function closeAlert(alertId) {
    const el = document.getElementById(alertId);
    if (el) el.classList.add('hidden');
}
>>>>>>> 1f8d99bdc5b2cb9c8c0a008d63d1e293f25d179d

function setLoading(isLoading) {
    if (!submitBtn) return;
    submitBtn.disabled = isLoading;
    const spinner = submitBtn.querySelector('.spinner');
    const btnText = submitBtn.querySelector('.btn-text');

<<<<<<< HEAD
// Form submission
chatForm.addEventListener("submit", async function(e) {
    // Merged and cleaned version of main.js
    let currentTicketId = null;
    const messageInput = document.getElementById("message");
    const chatForm = document.getElementById("chatForm");
    const submitBtn = document.getElementById("submitBtn");
    const resultDiv = document.getElementById("result");
    const errorAlert = document.getElementById("errorAlert");
    const charCountSpan = document.getElementById("charCount");
    const themeToggle = document.getElementById('themeToggle');

    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark');
            if (themeToggle) themeToggle.innerText = '☀️ Light Mode';
        } else {
            document.body.classList.remove('dark');
            if (themeToggle) themeToggle.innerText = '🌙 Dark Mode';
        }
        localStorage.setItem('resolvexTheme', theme);
    }

    function showError(message) {
        const errorMessageElm = document.getElementById('errorMessage');
        if (errorMessageElm) errorMessageElm.innerText = message;
        if (errorAlert) errorAlert.classList.remove('hidden');
    }

    function closeAlert(alertId) {
        const el = document.getElementById(alertId);
        if (el) el.classList.add('hidden');
    }

    function setLoading(isLoading) {
        if (!submitBtn) return;
        submitBtn.disabled = isLoading;
        const spinner = submitBtn.querySelector('.spinner');
        const btnText = submitBtn.querySelector('.btn-text');

        if (isLoading) {
            spinner?.classList.remove('hidden');
            if (btnText) btnText.textContent = 'Sending...';
        } else {
            spinner?.classList.add('hidden');
            if (btnText) btnText.textContent = 'Send Message';
        }
    }

    function disableFeedbackButtons(disabled) {
        const yes = document.getElementById('feedbackYes');
        const no = document.getElementById('feedbackNo');
        if (yes) yes.disabled = disabled;
        if (no) no.disabled = disabled;
    }

    function resetChat() {
        if (messageInput) messageInput.value = '';
        if (charCountSpan) charCountSpan.textContent = '0';
        if (resultDiv) resultDiv.classList.add('hidden');
        currentTicketId = null;
        closeAlert('errorAlert');
        messageInput?.focus();
    }

    // Character counter
    if (messageInput && charCountSpan) {
        messageInput.addEventListener("input", function() {
            charCountSpan.textContent = this.value.length;
        });
    }

    // Form submission
    if (chatForm) {
        chatForm.addEventListener("submit", async function(e) {
            e.preventDefault();
            closeAlert("errorAlert");

            const message = (messageInput?.value || '').trim();

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
                const intentEl = document.getElementById("intent");
                const responseEl = document.getElementById("response");
                if (intentEl) intentEl.innerText = data.intent.charAt(0).toUpperCase() + data.intent.slice(1);
                if (responseEl) responseEl.innerText = data.response;

                resultDiv.classList.remove("hidden");
                resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
            } catch (error) {
                console.error("Error:", error);
                showError("Failed to get response. Please try again.");
            } finally {
                setLoading(false);
            }
        });
    }

    async function sendFeedback(helpful) {
        if (!currentTicketId) return;
        disableFeedbackButtons(true);
        try {
            await fetch('/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ticket_id: currentTicketId, helpful })
            });
        } catch (e) {
            console.error('Feedback error', e);
        } finally {
            disableFeedbackButtons(false);
        }
    }
    setLoading(true);

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        const data = await res.json();

        if (!data.ticket_id || !data.intent || !data.response) {
            throw new Error('Invalid response format from server.');
        }

        currentTicketId = data.ticket_id;

        const intentEl = document.getElementById('intent');
        const responseEl = document.getElementById('response');

        if (intentEl) intentEl.innerText = data.intent.charAt(0).toUpperCase() + data.intent.slice(1);
        if (responseEl) responseEl.innerText = data.response;

        const confidenceEl = document.getElementById('confidence');
        if (confidenceEl && data.confidence !== undefined) {
            confidenceEl.innerText = `${data.confidence}%`;
        }

        resultDiv?.classList.remove('hidden');
        resultDiv?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to get response. Please try again.');
    } finally {
        setLoading(false);
    }
}

function initApp() {
    messageInput = document.getElementById('message');
    chatForm = document.getElementById('chatForm');
    submitBtn = document.getElementById('submitBtn');
    resultDiv = document.getElementById('result');
    errorAlert = document.getElementById('errorAlert');
    charCountSpan = document.getElementById('charCount');
    themeToggle = document.getElementById('themeToggle');

    const savedTheme = localStorage.getItem('resolvexTheme') || 'light';
    applyTheme(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const nextTheme = document.body.classList.contains('dark') ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }

    messageInput?.addEventListener('input', function() {
        charCountSpan.textContent = this.value.length;
    });

    messageInput?.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm?.requestSubmit();
        }
    });

    chatForm?.addEventListener('submit', submitHandler);

    messageInput?.focus();
}

document.addEventListener('DOMContentLoaded', initApp);
