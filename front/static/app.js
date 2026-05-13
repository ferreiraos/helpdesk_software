const apiBase = "/api";
const state = {
    chamados: [],
    selectedId: null,
};

const elements = {
    chamadosList: document.getElementById("chamados-list"),
    detailTitle: document.getElementById("detail-title"),
    detailStatus: document.getElementById("detail-status"),
    detailContent: document.getElementById("detail-content"),
    messagesList: document.getElementById("messages-list"),
    statusActions: document.getElementById("status-actions"),
    feedbackSection: document.getElementById("feedback-section"),
    historyList: document.getElementById("history-list"),
    newChamadoForm: document.getElementById("new-chamado-form"),
    messageForm: document.getElementById("message-form"),
    messageContent: document.getElementById("message-content"),
};

async function request(path, options = {}) {
    const response = await fetch(`${apiBase}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Erro de rede");
    }

    return response.json();
}

async function loadChamados() {
    state.chamados = await request("/chamados");
    renderChamados();

    if (!state.selectedId && state.chamados.length) {
        selectChamado(state.chamados[0].id);
    }
}

async function selectChamado(id) {
    const chamado = await request(`/chamados/${id}`);
    state.selectedId = id;
    state.selected = chamado;
    renderDetail();
}

function renderChamados() {
    elements.chamadosList.innerHTML = "";

    if (!state.chamados.length) {
        elements.chamadosList.innerHTML = "<p class='small'>Nenhum chamado encontrado.</p>";
        return;
    }

    state.chamados.forEach((chamado) => {
        const item = document.createElement("button");
        item.className = `list-item ${state.selectedId === chamado.id ? "active" : ""}`;
        item.textContent = `${chamado.titulo} - ${chamado.status}`;
        item.onclick = () => selectChamado(chamado.id);
        elements.chamadosList.appendChild(item);
    });
}

function renderDetail() {
    const chamado = state.selected;
    if (!chamado) {
        elements.detailTitle.textContent = "Selecione um chamado";
        elements.detailStatus.textContent = "";
        elements.detailContent.innerHTML = "<p class='placeholder'>Escolha um chamado no painel à esquerda para ver detalhes.</p>";
        elements.messagesList.innerHTML = "";
        elements.statusActions.innerHTML = "";
        elements.feedbackSection.innerHTML = "";
        elements.historyList.innerHTML = "";
        return;
    }

    elements.detailTitle.textContent = chamado.titulo;
    elements.detailStatus.textContent = chamado.status;
    elements.detailContent.innerHTML = `
        <p class='section-label'>Descrição</p>
        <p>${chamado.descricao}</p>
    `;

    renderMessages(chamado.messages);
    renderStatusActions(chamado);
    renderFeedback(chamado);
    renderHistory(chamado.history);
}

function renderMessages(messages) {
    if (!messages.length) {
        elements.messagesList.innerHTML = "<p class='small'>Sem mensagens ainda.</p>";
        return;
    }

    elements.messagesList.innerHTML = messages
        .map(
            (message) => `
            <div class="message-card">
                <div class="message-meta">
                    <span>${message.author}</span>
                    <span>${new Date(message.created_at).toLocaleString()}</span>
                </div>
                <p>${message.content}</p>
            </div>
        `
        )
        .join("");
}

function renderStatusActions(chamado) {
    const status = chamado.status;
    const actions = [];

    if (status === "aberto") {
        actions.push({ label: "Marcar em andamento", value: "em andamento" });
        actions.push({ label: "Resolver chamado", value: "resolvido" });
    } else if (status === "em andamento") {
        actions.push({ label: "Resolver chamado", value: "resolvido" });
    }

    if (!actions.length) {
        elements.statusActions.innerHTML = "<p class='small'>Nenhuma ação disponível.</p>";
        return;
    }

    elements.statusActions.innerHTML = actions
        .map(
            (action) => `
            <button class="btn btn-primary action-btn" data-status="${action.value}">${action.label}</button>
        `
        )
        .join("");

    elements.statusActions.querySelectorAll(".action-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            await changeStatus(button.dataset.status);
        });
    });
}

function renderFeedback(chamado) {
    const feedbacks = chamado.feedbacks || [];

    if (chamado.status !== "resolvido") {
        elements.feedbackSection.innerHTML = "<p class='small'>Feedback disponível somente após resolução.</p>";
        return;
    }

    if (feedbacks.length) {
        const feedback = feedbacks[0];
        elements.feedbackSection.innerHTML = `
            <div class="feedback-card">
                <div class="feedback-header">Avaliação: ${feedback.rating}/5</div>
                <p>${feedback.comentario || "Sem comentário."}</p>
            </div>
        `;
        return;
    }

    elements.feedbackSection.innerHTML = `
        <form id="feedback-form" class="feedback-form">
            <label for="rating">Nota (1-5)</label>
            <input id="rating" name="rating" type="number" min="1" max="5" required />
            <label for="comentario">Comentário</label>
            <textarea id="comentario" name="comentario" rows="3" placeholder="Deixe seu comentário..."></textarea>
            <button type="submit" class="btn btn-secondary">Enviar Feedback</button>
        </form>
    `;

    document.getElementById("feedback-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        await sendFeedback();
    });
}

function renderHistory(history) {
    if (!history.length) {
        elements.historyList.innerHTML = "<p class='small'>Nenhum registro de status.</p>";
        return;
    }

    elements.historyList.innerHTML = history
        .map(
            (item) => `
            <div class="history-item">
                <div class="history-title">${item.status}</div>
                <p>${item.note || "Sem observação."}</p>
                <span>${new Date(item.created_at).toLocaleString()}</span>
            </div>
        `
        )
        .join("");
}

async function changeStatus(status) {
    try {
        const payload = { status };
        await request(`/chamados/${state.selectedId}/status`, {
            method: "PUT",
            body: JSON.stringify(payload),
        });
        await selectChamado(state.selectedId);
        await loadChamados();
    } catch (error) {
        alert(error.message);
    }
}

async function sendMessage() {
    try {
        const content = elements.messageContent.value.trim();
        if (!content) return;

        await request(`/chamados/${state.selectedId}/messages`, {
            method: "POST",
            body: JSON.stringify({ content }),
        });

        elements.messageContent.value = "";
        await selectChamado(state.selectedId);
    } catch (error) {
        alert(error.message);
    }
}

async function sendFeedback() {
    try {
        const rating = Number(document.getElementById("rating").value);
        const comentario = document.getElementById("comentario").value.trim();

        await request(`/chamados/${state.selectedId}/feedback`, {
            method: "POST",
            body: JSON.stringify({ rating, comentario }),
        });

        await selectChamado(state.selectedId);
    } catch (error) {
        alert(error.message);
    }
}

async function createChamado(event) {
    event.preventDefault();
    const title = document.getElementById("titulo").value.trim();
    const description = document.getElementById("descricao").value.trim();

    if (!title || !description) {
        return;
    }

    try {
        const chamado = await request("/chamados", {
            method: "POST",
            body: JSON.stringify({ titulo: title, descricao: description }),
        });

        document.getElementById("titulo").value = "";
        document.getElementById("descricao").value = "";
        await loadChamados();
        selectChamado(chamado.id);
    } catch (error) {
        alert(error.message);
    }
}

function attachEvents() {
    elements.newChamadoForm.addEventListener("submit", createChamado);
    elements.messageForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await sendMessage();
    });
}

window.addEventListener("DOMContentLoaded", async () => {
    attachEvents();
    await loadChamados();
});
