(function () {
    const messagesContainer = document.getElementById('messagesContainer');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    const clearBtn = document.getElementById('clearBtn');
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    let sessionId = null;
    let isLoading = false;

    function init() {
        createSession();
        bindEvents();
        autoResizeTextarea();
    }

    function bindEvents() {
        chatForm.addEventListener('submit', handleSubmit);
        messageInput.addEventListener('input', handleInputChange);
        messageInput.addEventListener('keydown', handleKeyDown);
        newChatBtn.addEventListener('click', startNewChat);
        clearBtn.addEventListener('click', clearConversation);
        menuToggle.addEventListener('click', toggleSidebar);
        overlay.addEventListener('click', closeSidebar);

        document.querySelectorAll('.chip').forEach(function (chip) {
            chip.addEventListener('click', function () {
                var prompt = chip.getAttribute('data-prompt');
                messageInput.value = prompt;
                handleInputChange();
                messageInput.focus();
            });
        });
    }

    async function createSession() {
        try {
            var response = await fetch('/api/session', { method: 'POST' });
            var data = await response.json();
            sessionId = data.session_id;
        } catch (err) {
            showError('Failed to initialize chat session.');
        }
    }

    function handleInputChange() {
        autoResizeTextarea();
        sendBtn.disabled = !messageInput.value.trim() || isLoading;
    }

    function handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    }

    function autoResizeTextarea() {
        messageInput.style.height = 'auto';
        messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
    }

    async function handleSubmit(e) {
        e.preventDefault();
        var message = messageInput.value.trim();
        if (!message || isLoading || !sessionId) return;

        hideWelcome();
        appendMessage('user', message);
        messageInput.value = '';
        messageInput.style.height = 'auto';
        sendBtn.disabled = true;
        isLoading = true;

        var typingEl = showTypingIndicator();

        try {
            var response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId, message: message }),
            });

            var data = await response.json();
            typingEl.remove();

            if (data.success && data.reply) {
                appendMessage('assistant', data.reply);
            } else {
                appendMessage('error', data.error || 'Something went wrong.');
            }
        } catch (err) {
            typingEl.remove();
            appendMessage('error', 'Network error. Please check your connection.');
        }

        isLoading = false;
        handleInputChange();
        messageInput.focus();
    }

    function hideWelcome() {
        if (welcomeScreen) {
            welcomeScreen.classList.add('hidden');
        }
    }

    function showWelcome() {
        if (welcomeScreen) {
            welcomeScreen.classList.remove('hidden');
        }
    }

    function appendMessage(role, content) {
        var messageEl = document.createElement('div');
        messageEl.className = 'message ' + role;

        var avatarLabel = role === 'user' ? 'You' : role === 'error' ? '!' : 'AI';

        messageEl.innerHTML =
            '<div class="message-inner">' +
                '<div class="message-avatar">' + avatarLabel + '</div>' +
                '<div class="message-content">' + formatContent(content) + '</div>' +
            '</div>';

        messagesContainer.appendChild(messageEl);
        scrollToBottom();
    }

    function formatContent(text) {
        var escaped = escapeHtml(text);
        escaped = escaped.replace(/```(\w*)\n([\s\S]*?)```/g, function (_, lang, code) {
            return '<pre><code>' + code.trim() + '</code></pre>';
        });
        escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
        escaped = escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/\n\n/g, '</p><p>');
        escaped = escaped.replace(/\n/g, '<br>');
        return '<p>' + escaped + '</p>';
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function showTypingIndicator() {
        var el = document.createElement('div');
        el.className = 'message assistant';
        el.innerHTML =
            '<div class="message-inner">' +
                '<div class="message-avatar">AI</div>' +
                '<div class="message-content">' +
                    '<div class="typing-indicator">' +
                        '<span></span><span></span><span></span>' +
                    '</div>' +
                '</div>' +
            '</div>';
        messagesContainer.appendChild(el);
        scrollToBottom();
        return el;
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function startNewChat() {
        await createSession();
        var messages = messagesContainer.querySelectorAll('.message');
        messages.forEach(function (msg) { msg.remove(); });
        showWelcome();
        closeSidebar();
        messageInput.focus();
    }

    async function clearConversation() {
        if (!sessionId) return;
        try {
            await fetch('/api/session/' + sessionId, { method: 'DELETE' });
            var messages = messagesContainer.querySelectorAll('.message');
            messages.forEach(function (msg) { msg.remove(); });
            showWelcome();
        } catch (err) {
            showError('Failed to clear conversation.');
        }
    }

    function toggleSidebar() {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
    }

    function showError(msg) {
        appendMessage('error', msg);
    }

    init();
})();
