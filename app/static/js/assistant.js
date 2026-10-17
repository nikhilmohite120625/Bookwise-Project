/**
 * BookWise Atelier — Conversational Reading Assistant
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendBtn = document.getElementById('chat-send-btn');
  const suggestionsBox = document.getElementById('chat-suggestions');

  if (!chatMessages || !chatInput || !chatSendBtn) return;

  function appendMessage(sender, text, books = []) {
    const msgDiv = document.createElement('div');
    msgDiv.style.marginBottom = '16px';
    msgDiv.style.display = 'flex';
    msgDiv.style.flexDirection = 'column';
    msgDiv.style.alignItems = sender === 'user' ? 'flex-end' : 'flex-start';

    const bubble = document.createElement('div');
    bubble.style.maxWidth = '80%';
    bubble.style.padding = '12px 18px';
    bubble.style.borderRadius = '12px';
    bubble.style.fontSize = '0.95rem';
    bubble.style.lineHeight = '1.5';
    bubble.style.whiteSpace = 'pre-wrap';

    if (sender === 'user') {
      bubble.style.backgroundColor = 'var(--color-primary)';
      bubble.style.color = '#ffffff';
    } else {
      bubble.style.backgroundColor = 'var(--color-bg-card)';
      bubble.style.border = '1px solid var(--color-border)';
      bubble.style.color = 'var(--color-text-main)';
    }

    bubble.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>');
    msgDiv.appendChild(bubble);

    // If books returned, render compact cards
    if (books && books.length > 0) {
      const bookContainer = document.createElement('div');
      bookContainer.style.display = 'flex';
      bookContainer.style.flexWrap = 'wrap';
      bookContainer.style.gap = '12px';
      bookContainer.style.marginTop = '10px';
      bookContainer.style.maxWidth = '100%';

      books.forEach(b => {
        const bCard = document.createElement('a');
        bCard.href = `/books/${b.id}`;
        bCard.style.display = 'flex';
        bCard.style.alignItems = 'center';
        bCard.style.gap = '10px';
        bCard.style.padding = '8px 12px';
        bCard.style.backgroundColor = 'var(--color-bg-surface)';
        bCard.style.border = '1px solid var(--color-border-gold)';
        bCard.style.borderRadius = '8px';
        bCard.style.textDecoration = 'none';
        bCard.style.color = 'inherit';
        bCard.style.maxWidth = '300px';

        bCard.innerHTML = `
          <img src="${b.cover_url}" style="width: 40px; height: 56px; object-fit: cover; border-radius: 4px;" alt="${b.title}">
          <div style="font-size: 0.85rem; overflow: hidden;">
            <div style="font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${b.title}</div>
            <div style="color: var(--color-text-muted); font-size: 0.75rem;">${b.author}</div>
            <div style="color: var(--color-accent-gold-dark); font-size: 0.75rem;">⭐ ${b.rating || 'N/A'} • ${b.estimated_duration || 30}m</div>
          </div>
        `;
        bookContainer.appendChild(bCard);
      });

      msgDiv.appendChild(bookContainer);
    }

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function setSuggestions(suggestions) {
    if (!suggestionsBox) return;
    suggestionsBox.innerHTML = '';
    if (!suggestions || suggestions.length === 0) return;

    suggestions.forEach(s => {
      const pill = document.createElement('button');
      pill.type = 'button';
      pill.className = 'btn-atelier btn-atelier-secondary btn-atelier-sm';
      pill.style.borderRadius = '20px';
      pill.style.fontSize = '0.8rem';
      pill.textContent = s;
      pill.addEventListener('click', () => {
        chatInput.value = s;
        sendMessage();
      });
      suggestionsBox.appendChild(pill);
    });
  }

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage('user', text);
    chatInput.value = '';
    chatInput.focus();

    // Loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'assistant-loading';
    loadingDiv.style.color = 'var(--color-text-muted)';
    loadingDiv.style.fontSize = '0.85rem';
    loadingDiv.style.fontStyle = 'italic';
    loadingDiv.textContent = 'Curating response...';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      // Fetch CSRF token from page
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

      const resp = await fetch('/assistant/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ message: text })
      });

      const data = await resp.json();
      loadingDiv.remove();

      appendMessage('assistant', data.reply, data.books);
      setSuggestions(data.suggestions);
    } catch (e) {
      loadingDiv.remove();
      appendMessage('assistant', 'Apologies, I encountered an issue retrieving that recommendation. Please try again.');
    }
  }

  chatSendBtn.addEventListener('click', sendMessage);
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });

  // Attach default suggestions if present
  document.querySelectorAll('.initial-suggestion-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      chatInput.value = this.textContent.trim();
      sendMessage();
    });
  });
});
