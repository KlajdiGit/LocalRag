const API_BASE = "http://127.0.0.1:8000";

function addMessage(text, sender) {
    const chat = document.getElementById("chat-window");
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    const response = await fetch(`${API_BASE}/answer`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question})
    });

    const data = await response.json();

    let botText = `<strong>${data.answer}</strong><br><br><em>Sources:</em><ul>`;
    data.sources.forEach(src => {
        botText += `<li><strong>${src.doc}</strong>: ${src.text}</li>`;
    });
    botText += "</ul>";

    addMessage(botText, "bot");
}

async function uploadPDF() {
    const fileInput = document.getElementById("pdf-upload");
    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch(`${API_BASE}/test_rag`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    addMessage(`PDF uploaded: ${data.message}`, "bot");
}

async function resetRAG() {
    const response = await fetch(`${API_BASE}/reset_rag`, {
        method: "POST"
    });

    const data = await response.json();
    addMessage("Knowledge base reset.", "bot");
}
