let currentTicketId = null;
let messageInput, chatForm, submitBtn, chatHistory, errorAlert, charCountSpan, themeToggle, ticketList;

function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark');
        if (themeToggle) themeToggle.innerText = '☀️ Light Mode';
    } else {
        document.body.classList.remove('dark');
        if (themeToggle) themeToggle.innerText = '🌙 Dark Mode';
    }
    localStorage.setItem('resolvexTheme', theme);
    document.cookie = `theme=${theme}; path=/; max-age=31536000`;
}

function showError(message) {
    const errorMessageElm = document.getElementById('errorMessage');
    if (errorMessageElm) errorMessageElm.innerText = message;
    if (errorAlert) errorAlert.classList.remove('hidden');
    setTimeout(() => closeAlert('errorAlert'), 5000);
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
        if (btnText) btnText.textContent = '...';
    } else {
        spinner?.classList.add('hidden');
        if (btnText) btnText.textContent = 'Send';
    }
}

function appendMessage(content, type, data = null) {
    if (!chatHistory) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}-message`;
    
    const textSpan = document.createElement('span');
    textSpan.innerText = content;
    msgDiv.appendChild(textSpan);

    if (type === 'assistant' && data && data.confidence !== undefined) {
        const template = document.getElementById('feedbackTemplate');
        if (template) {
            const clone = template.content.cloneNode(true);
            
            // Populate data
            clone.querySelector('.intent-text').textContent = data.intent;
            clone.querySelector('.confidence-text').textContent = `${data.confidence}%`;
            
            const pill = clone.querySelector('.status-pill');
            pill.textContent = data.status;
            pill.style.background = data.status === 'Escalated' ? '#ef4444' : '#10b981';
            pill.style.color = 'white';

            // Buttons
            const yesBtn = clone.querySelector('.feedback-yes');
            const noBtn = clone.querySelector('.feedback-no');
            const detailed = clone.querySelector('.detailed-feedback');
            const submitBtn = clone.querySelector('.submit-detailed');
            const categorySelect = clone.querySelector('.correct-category');
            const answerText = clone.querySelector('.correct-answer');

            yesBtn.onclick = () => handleFeedback(currentTicketId, true, msgDiv);
            noBtn.onclick = () => detailed.classList.toggle('hidden');
            
            submitBtn.onclick = () => {
                handleFeedback(currentTicketId, false, msgDiv, categorySelect.value, answerText.value);
            };

            msgDiv.appendChild(clone);
        }
    }

    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: 'smooth' });
}

async function loadTickets() {
    if (!ticketList) return;
    try {
        const res = await fetch('/my-tickets?json=true'); // We'll update the route to support JSON
        if (!res.ok) throw new Error();
        const tickets = await res.json();
        
        ticketList.innerHTML = '';
        if (tickets.length === 0) {
            ticketList.innerHTML = '<div style="padding:20px; text-align:center; font-size:12px; opacity:0.5;">No previous chats found.</div>';
            return;
        }

        tickets.forEach(ticket => {
            const item = document.createElement('div');
            item.className = `ticket-item ${currentTicketId === ticket.id ? 'active' : ''}`;
            const firstMsg = ticket.messages ? ticket.messages[0].content : ticket.message || 'New Chat';
            item.innerHTML = `
                <div class="ticket-id">#${ticket.id}</div>
                <div class="ticket-preview">${firstMsg}</div>
            `;
            item.onclick = () => loadTicket(ticket.id);
            ticketList.appendChild(item);
        });
    } catch (e) {
        ticketList.innerHTML = '<div style="padding:20px; text-align:center; font-size:12px; color:red;">Failed to load history.</div>';
    }
}

async function loadTicket(id) {
    if (currentTicketId === id) return;
    currentTicketId = id;
    
    // Highlight in sidebar
    document.querySelectorAll('.ticket-item').forEach(i => i.classList.remove('active'));
    document.querySelector(`.ticket-item[onclick*="${id}"]`)?.classList.add('active');

    chatHistory.innerHTML = '<div style="padding:20px; text-align:center; opacity:0.5;">Loading conversation...</div>';

    try {
        const res = await fetch(`/api/ticket/${id}`);
        if (!res.ok) throw new Error();
        const ticket = await res.json();

        chatHistory.innerHTML = '';
        if (ticket.messages) {
            ticket.messages.forEach(msg => {
                appendMessage(msg.content, msg.role);
            });
        } else {
            // Legacy support
            appendMessage(ticket.message, 'user');
            appendMessage(ticket.response, 'assistant', ticket);
        }
    } catch (e) {
        showError('Failed to load conversation');
        resetChat();
    }
}

async function handleFeedback(ticketId, helpful, container, correctCat = null, correctAns = null) {
    const feedbackSection = container.querySelector('.feedback-container');
    const btns = feedbackSection.querySelectorAll('button');
    btns.forEach(b => b.disabled = true);

    let payload = { helpful };
    if (!helpful) {
        payload.correct_category = correctCat;
        payload.correct_answer = correctAns;
    }

    try {
        const res = await fetch(`/feedback/${ticketId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) throw new Error('Feedback failed');

        feedbackSection.innerHTML = `<div style="color: #10b981; font-size: 12px; margin-top: 10px; font-weight: 600;">✓ Feedback received!</div>`;
    } catch (e) {
        showError('Failed to send feedback');
        btns.forEach(b => b.disabled = false);
    }
}

function resetChat() {
    if (chatHistory) {
        chatHistory.innerHTML = `
            <div class="message assistant-message">
                Hello! I'm ResolveX. How can I help you today? Whether it's billing, technical issues, or account management, I'm here to assist.
            </div>
        `;
    }
    if (messageInput) {
        messageInput.value = '';
        messageInput.style.height = 'auto';
    }
    currentTicketId = null;
    document.querySelectorAll('.ticket-item').forEach(i => i.classList.remove('active'));
}

async function submitHandler(event) {
    event.preventDefault();
    const message = messageInput?.value.trim();
    if (!message) return;

    if (message.length < 2) {
        showError('Message too short');
        return;
    }

    appendMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';
    setLoading(true);

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, ticket_id: currentTicketId })
        });

        if (!res.ok) throw new Error('Server error');
        const data = await res.json();
        
        appendMessage(data.response, 'assistant', data);
        if (!currentTicketId) {
            currentTicketId = data.ticket_id;
            loadTickets(); // Refresh list to show the new chat
        }
    } catch (e) {
        appendMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        showError('Connection error');
    } finally {
        setLoading(false);
    }
}

async function resetChat() {
    currentTicketId = null;
    if (typeof chatHistory !== 'undefined') chatHistory.innerHTML = '';
    await fetch('/api/chat/reset', { method: 'POST' }).catch(() => {});
    const welcome = document.createElement('div');
    welcome.className = 'message ai-message';
    welcome.innerHTML = '<div class="bubble">Hello! I am ResolveX AI. How can I help you today?</div>';
    if (typeof chatHistory !== 'undefined') chatHistory.appendChild(welcome);
    document.querySelectorAll('.ticket-item').forEach(i => i.classList.remove('active'));
}

function initApp() {
    messageInput = document.getElementById('message');
    chatForm = document.getElementById('chatForm');
    submitBtn = document.getElementById('submitBtn');
    chatHistory = document.getElementById('chatHistory');
    errorAlert = document.getElementById('errorAlert');
    charCountSpan = document.getElementById('charCount');
    themeToggle = document.getElementById('themeToggle');
    ticketList = document.getElementById('ticketList');

    const savedTheme = localStorage.getItem('resolvexTheme') || 'light';
    applyTheme(savedTheme);

    themeToggle?.addEventListener('click', () => {
        const next = document.body.classList.contains('dark') ? 'light' : 'dark';
        applyTheme(next);
    });

    messageInput?.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (charCountSpan) charCountSpan.textContent = this.value.length;
    });

    messageInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    chatForm?.addEventListener('submit', submitHandler);
    
    loadTickets();
}

document.addEventListener('DOMContentLoaded', initApp);