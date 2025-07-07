const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const loading = document.getElementById('loading');
const darkToggle = document.getElementById('dark-toggle');
const resetBtn = document.getElementById('reset-btn');

window.onload = () => userInput.focus();

function appendMessage(sender, text) {
  let msgElem = document.createElement('div');
  msgElem.className = "msg " + (sender === 'user' ? 'user' : 'assistant');

  let avatar = document.createElement('div');
  avatar.className = "avatar";
  avatar.textContent = sender === 'user' ? '🧑' : '🤖';

  let content = document.createElement('div');
  content.className = "content";
  content.innerHTML = text;

  if (sender === 'user') {
    msgElem.appendChild(content);
    msgElem.appendChild(avatar);
  } else {
    msgElem.appendChild(avatar);
    msgElem.appendChild(content);
  }

  chatBox.appendChild(msgElem);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}

function appendAssistantMessage({thought, observation, response}) {
  // Create the message container
  let msgElem = document.createElement('div');
  msgElem.className = "msg assistant";

  let avatar = document.createElement('div');
  avatar.className = "avatar";
  avatar.textContent = '🤖';

  let content = document.createElement('div');
  content.className = "content";

  // Main answer
  let answerElem = document.createElement('div');
  answerElem.innerHTML = escapeHtml(response).replace(/\n/g, '<br>');

  // Process (thought + observation), hidden by default
  let processElem = document.createElement('div');
  processElem.style.display = 'none';
  processElem.innerHTML = `
    <em>Thought:</em> ${escapeHtml(thought)}<br>
    <em>Observation:</em> ${escapeHtml(observation)}
  `;

  // Show process button
  let btn = document.createElement('button');
  btn.textContent = "Show process";
  btn.className = "header-btn";
  btn.style.marginTop = "0.75em";
  btn.onclick = function() {
    if (processElem.style.display === 'none') {
      processElem.style.display = '';
      btn.textContent = "Hide process";
    } else {
      processElem.style.display = 'none';
      btn.textContent = "Show process";
    }
  };

  content.appendChild(answerElem);
  content.appendChild(btn);
  content.appendChild(processElem);

  msgElem.appendChild(avatar);
  msgElem.appendChild(content);

  chatBox.appendChild(msgElem);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}

let thinkingElem = null;

function showThinkingBubble() {
  removeThinkingBubble();

  thinkingElem = document.createElement('div');
  thinkingElem.className = "msg assistant";
  let avatar = document.createElement('div');
  avatar.className = "avatar";
  avatar.textContent = '🤖';

  let content = document.createElement('div');
  content.className = "content";
  content.innerHTML = '<span class="thinking-dots">Thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></span>';

  thinkingElem.appendChild(avatar);
  thinkingElem.appendChild(content);
  chatBox.appendChild(thinkingElem);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}

function removeThinkingBubble() {
  if (thinkingElem && thinkingElem.parentNode) {
    thinkingElem.parentNode.removeChild(thinkingElem);
    thinkingElem = null;
  }
}

function setLoading(isLoading) {
  loading.style.display = 'none';
  sendBtn.disabled = isLoading;
  userInput.disabled = isLoading;
  if (isLoading) {
    showThinkingBubble();
  } else {
    removeThinkingBubble();
  }
}

function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  appendMessage('user', escapeHtml(text));
  userInput.value = '';
  setLoading(true);

  fetch('/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: text })
  })
    .then(res => res.json())
    .then(data => {
      setLoading(false);
      if (data.clarification) {
        appendMessage('assistant', `<strong>Clarification:</strong> ${escapeHtml(data.clarification)}`);
      } else if (data.image_url) {  // Handle graph responses
        appendMessage('assistant', `
          <img src="${data.image_url}" alt="Generated Graph" style="max-width: 100%; border-radius: 8px;" />
          <br>${escapeHtml(data.message || "")}
        `);
      } else if (data.thought || data.observation || data.response) {
        appendAssistantMessage({
          thought: data.thought || "",
          observation: data.observation || "",
          response: data.response || ""
        });
      } else {
        appendMessage('assistant', escapeHtml(data.response || "Sorry, there was an error.").replace(/\n/g, '<br>'));
      }
    })
    .catch(err => {
      setLoading(false);
      appendMessage('assistant', "Sorry, there was an error.");
    });
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/[&<>"']/g, function (m) {
    return {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[m];
  });
}

sendBtn.onclick = sendMessage;
userInput.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

let lastUserMsg = '';
userInput.addEventListener('keydown', function (e) {
  if (e.key === 'ArrowUp' && lastUserMsg) {
    userInput.value = lastUserMsg;
  }
});
userInput.addEventListener('input', function () {
  lastUserMsg = userInput.value;
});

// Dark mode toggle
darkToggle.onclick = () => {
  document.body.classList.toggle('dark-mode');
  darkToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️ Light' : '🌙 Dark';
};

resetBtn.onclick = () => {
  fetch('/reset', { method: 'POST' })
    .then(() => location.reload());
};
