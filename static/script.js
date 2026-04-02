const messagesDiv = document.getElementById("messages");
let isFirstMessage = true;

function sendQuery() {
  const query = document.getElementById("queryInput").value.trim();

  if (!query) {
    return;
  }

  if (isFirstMessage) {
    messagesDiv.innerHTML = "";
    isFirstMessage = false;
  }

  const userGroup = document.createElement("div");
  userGroup.className = "message-group user";
  userGroup.innerHTML = `
                <div style="order: 2;">
                    <div class="message user">${escapeHtml(query)}</div>
                </div>
                <div class="message-avatar user">You</div>
            `;
  messagesDiv.appendChild(userGroup);

  document.getElementById("queryInput").value = "";
  document.getElementById("sendBtn").disabled = true;

  const loadingGroup = document.createElement("div");
  loadingGroup.className = "message-group bot";
  loadingGroup.innerHTML = `
                <div class="message-avatar bot">🤖</div>
                <div class="message-content">
                    <div class="loading">
                        <div class="spinner"></div>
                    </div>
                </div>
            `;
  messagesDiv.appendChild(loadingGroup);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  fetch("/api/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query }),
  })
    .then((response) => response.json())
    .then((data) => {
      messagesDiv.removeChild(loadingGroup);

      const botGroup = document.createElement("div");
      botGroup.className = "message-group bot";
      botGroup.innerHTML = `<div class="message-avatar bot">🤖</div>`;

      if (data.error) {
        const errorMsg = document.createElement("div");
        errorMsg.className = "message error";
        errorMsg.textContent = "Error:  " + data.error;
        botGroup.appendChild(errorMsg);
      } else if (data.docs && data.docs.length > 0) {
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.textContent = data.docs[0];
        botGroup.appendChild(botMsg);
      } else {
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.textContent =
          "Sorry, I couldn't find relevant information for that query.";
        botGroup.appendChild(botMsg);
      }

      messagesDiv.appendChild(botGroup);
      document.getElementById("sendBtn").disabled = false;
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch((error) => {
      messagesDiv.removeChild(loadingGroup);
      const botGroup = document.createElement("div");
      botGroup.className = "message-group bot";
      const errorMsg = document.createElement("div");
      errorMsg.className = "message error";
      errorMsg.textContent = " Error: " + error.message;
      botGroup.appendChild(errorMsg);
      messagesDiv.appendChild(botGroup);
      document.getElementById("sendBtn").disabled = false;
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

function newChat() {
  messagesDiv.innerHTML = `
                <div class="initial-message">
                    <h2 style="font-size: 2em;">Chat Bot</h2>
                    <p>Start a conversation. Ask anything about WSC policy!</p>
                </div>
            `;
  document.getElementById("queryInput").value = "";
  isFirstMessage = true;
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

document
  .getElementById("queryInput")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendQuery();
    }
  });

document.getElementById("queryInput").focus();
