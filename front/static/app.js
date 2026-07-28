const api = {
    listTickets: () => fetch('/api/chamados').then(res => res.json()),
    getTicket: id => fetch(`/api/chamados/${id}`).then(res => res.json()),
    createTicket: data => fetch('/api/chamados', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => res.json()),
    updateStatus: (id, status) => fetch(`/api/chamados/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    }).then(res => res.json()),
    addMessage: (id, message) => fetch(`/api/chamados/${id}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(message)
    }).then(res => res.json()),
    addFeedback: (id, feedback) => fetch(`/api/chamados/${id}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedback)
    }).then(res => res.json()),
};

const state = {
    selectedTicketId: null,
    tickets: [],
    ticketDetail: null,
};

const elements = {
    ticketList: document.getElementById('ticket-list'),
    ticketCount: document.getElementById('ticket-count'),
    themeToggle: document.getElementById('theme-toggle'),
    detailsTitle: document.getElementById('details-title'),
    detailsBody: document.getElementById('details-body'),
    statusSelect: document.getElementById('status-select'),
    historyBody: document.getElementById('history-body'),
    feedbackBody: document.getElementById('feedback-body'),
    messageList: document.getElementById('message-list'),
    messageForm: document.getElementById('message-form'),
    messageContent: document.getElementById('message-content'),
    createForm: document.getElementById('create-ticket-form'),
    ticketTitleInput: document.getElementById('ticket-title'),
    ticketDescInput: document.getElementById('ticket-desc'),
    feedbackForm: document.getElementById('feedback-form'),
    feedbackRating: document.getElementById('feedback-rating'),
    feedbackComentario: document.getElementById('feedback-comentario'),
    alertBox: document.getElementById('alert-box'),
};

function applyTheme(theme) {
    document.body.dataset.theme = theme;
    document.body.classList.add('theme-transitioning');
    localStorage.setItem('helpdesk-theme', theme);

    window.clearTimeout(window.__themeTransitionTimer);
    window.__themeTransitionTimer = window.setTimeout(() => {
        document.body.classList.remove('theme-transitioning');
    }, 450);

    if (elements.themeToggle) {
        const isDark = theme === 'dark';
        elements.themeToggle.setAttribute('aria-pressed', String(isDark));
        elements.themeToggle.querySelector('.theme-toggle-icon').textContent = isDark ? '☀️' : '🌙';
        elements.themeToggle.querySelector('.theme-toggle-label').textContent = isDark ? 'Tema claro' : 'Tema escuro';
    }
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('helpdesk-theme');
    const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    applyTheme(savedTheme || preferredTheme);

    if (elements.themeToggle) {
        elements.themeToggle.addEventListener('click', () => {
            const nextTheme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }
}

function showAlert(message, type = 'success') {
    elements.alertBox.textContent = message;
    elements.alertBox.className = `alert ${type}`;
    elements.alertBox.style.display = 'block';
    elements.alertBox.animate([
        { transform: 'translateY(-4px)', opacity: 0 },
        { transform: 'translateY(0)', opacity: 1 }
    ], { duration: 220, fill: 'forwards' });
    setTimeout(() => {
        elements.alertBox.style.display = 'none';
    }, 3500);
}

function clearDetailSection() {
    elements.detailsTitle.textContent = 'Selecione um chamado';
    elements.detailsBody.innerHTML = '<p class="empty-state">Clique em um chamado para ver os detalhes, mensagens e feedback.</p>';
    elements.statusSelect.innerHTML = '<option value="aberto">Aberto</option><option value="em andamento">Em andamento</option><option value="resolvido">Resolvido</option>';
    elements.historyBody.innerHTML = '<p class="empty-state">Histórico de status será exibido aqui.</p>';
    elements.messageList.innerHTML = '<p class="empty-state">Selecione um chamado para acompanhar a conversa.</p>';
    elements.feedbackBody.innerHTML = '<p class="empty-state">Feedback aparece aqui quando o chamado for resolvido.</p>';
}

function formatDate(value) {
    if (!value) return 'Sem data';
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return 'Sem data';
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(value) {
    if (!value) return 'Sem data';
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return 'Sem data';
    return date.toLocaleString('pt-BR');
}

function animateElement(selector, className) {
    const target = document.querySelector(selector);
    if (!target) return;
    target.classList.remove(className);
    void target.offsetWidth;
    target.classList.add(className);
}

function renderTicketList(tickets) {
    state.tickets = tickets;
    elements.ticketCount.textContent = tickets.length;
    elements.ticketList.innerHTML = tickets.map(ticket => {
        const active = ticket.id === state.selectedTicketId ? 'active' : '';
        const ticketDate = ticket.updated_at || ticket.created_at;
        const isNew = !state.tickets.some(existing => existing.id === ticket.id) && ticket.id;
        return `
            <button class="ticket-item ${active} ${isNew ? 'is-new' : ''}" data-id="${ticket.id}">
                <span class="ticket-title">${ticket.titulo}</span>
                <span class="ticket-meta">
                    <span>${formatDate(ticketDate)}</span>
                    <span class="ticket-status ${ticket.status.replace(' ', '-')}">${ticket.status}</span>
                </span>
            </button>
        `;
    }).join('');
    elements.ticketList.querySelectorAll('.ticket-item').forEach(button => {
        button.addEventListener('click', () => {
            const ticketId = Number(button.dataset.id);
            selectTicket(ticketId);
        });
    });
}

function renderTicketDetails(ticket) {
    state.ticketDetail = ticket;
    elements.detailsTitle.textContent = ticket.titulo;
    elements.detailsBody.classList.add('is-updating');
    elements.detailsBody.innerHTML = `
        <div class="ticket-meta">
            <span>Status: <strong>${ticket.status}</strong></span>
            <span>Criado em: ${formatDateTime(ticket.created_at)}</span>
            <span>Atualizado em: ${formatDateTime(ticket.updated_at)}</span>
        </div>
        <p class="ticket-description">${ticket.descricao}</p>
    `;

    elements.statusSelect.value = ticket.status;
    elements.historyBody.innerHTML = ticket.history.length
        ? ticket.history.map(entry => `
            <div class="history-item is-updating">
                <strong>${formatDateTime(entry.created_at)}</strong>
                <p>${entry.note || `${entry.previous_status} → ${entry.new_status}`}</p>
            </div>
        `).join('')
        : '<p class="empty-state">Nenhuma alteração de status registrada.</p>';

    elements.messageList.innerHTML = ticket.messages.length
        ? ticket.messages.map(message => `
            <div class="message-item is-updating">
                <div class="message-meta">
                    <span>${message.author}</span>
                    <span>${formatDateTime(message.created_at)}</span>
                </div>
                <p>${message.content}</p>
            </div>
        `).join('')
        : '<p class="empty-state">Nenhuma mensagem adicionada ainda.</p>';

    elements.feedbackBody.innerHTML = ticket.feedback
        ? `
            <div class="feedback-card">
                <p><strong>Nota:</strong> ${ticket.feedback.rating}/5</p>
                <p>${ticket.feedback.comentario || 'Sem comentário'}</p>
            </div>
        `
        : '<p class="empty-state">Feedback não enviado.</p>';

    elements.feedbackForm.style.display = ticket.status === 'resolvido' && !ticket.feedback ? 'block' : 'none';
}

function refreshData() {
    api.listTickets()
        .then(renderTicketList)
        .catch(() => showAlert('Erro ao carregar a lista de chamados.', 'error'));

    if (state.selectedTicketId) {
        selectTicket(state.selectedTicketId);
    }
}

function selectTicket(ticketId) {
    state.selectedTicketId = ticketId;
    const selected = state.tickets.find(item => item.id === ticketId);
    if (!selected) {
        return;
    }
    renderTicketList(state.tickets);
    api.getTicket(ticketId)
        .then(renderTicketDetails)
        .catch(() => showAlert('Erro ao carregar detalhes do chamado.', 'error'));
}

function setupEventHandlers() {
    elements.createForm.addEventListener('submit', event => {
        event.preventDefault();
        const payload = {
            titulo: elements.ticketTitleInput.value.trim(),
            descricao: elements.ticketDescInput.value.trim(),
        };

        if (!payload.titulo || !payload.descricao) {
            return showAlert('Preencha título e descrição.', 'error');
        }

        api.createTicket(payload)
            .then(() => {
                elements.ticketTitleInput.value = '';
                elements.ticketDescInput.value = '';
                elements.createForm.classList.add('is-updating');
                refreshData();
                showAlert('Chamado criado com sucesso.');
            })
            .catch(() => showAlert('Não foi possível criar o chamado.', 'error'));
    });

    elements.statusSelect.addEventListener('change', () => {
        if (!state.selectedTicketId) return;
        api.updateStatus(state.selectedTicketId, elements.statusSelect.value)
            .then(ticket => {
                elements.statusSelect.classList.add('is-updating');
                renderTicketDetails(ticket);
                refreshData();
                showAlert('Status atualizado com sucesso.');
            })
            .catch(() => showAlert('Erro ao atualizar status.', 'error'));
    });

    elements.messageForm.addEventListener('submit', event => {
        event.preventDefault();
        if (!state.selectedTicketId) return;

        const payload = {
            author: 'Usuário',
            content: elements.messageContent.value.trim(),
        };

        if (!payload.content) {
            return showAlert('Digite uma mensagem antes de enviar.', 'error');
        }

        api.addMessage(state.selectedTicketId, payload)
            .then(() => {
                elements.messageContent.value = '';
                elements.messageForm.classList.add('is-updating');
                selectTicket(state.selectedTicketId);
                showAlert('Mensagem adicionada.');
            })
            .catch(() => showAlert('Não foi possível enviar a mensagem.', 'error'));
    });

    elements.feedbackForm.addEventListener('submit', event => {
        event.preventDefault();
        if (!state.selectedTicketId) return;

        const selectedRating = document.querySelector('input[name="feedback-rating"]:checked');
        const payload = {
            rating: Number(selectedRating?.value || 5),
            comentario: elements.feedbackComentario.value.trim(),
        };

        api.addFeedback(state.selectedTicketId, payload)
            .then(() => {
                const defaultRating = document.getElementById('rating-5');
                if (defaultRating) defaultRating.checked = true;
                elements.feedbackComentario.value = '';
                elements.feedbackForm.classList.add('is-updating');
                selectTicket(state.selectedTicketId);
                refreshData();
                showAlert('Feedback enviado. Obrigado!');
            })
            .catch(() => showAlert('Erro ao enviar o feedback.', 'error'));
    });
}

function initialize() {
    initializeTheme();
    setupEventHandlers();
    clearDetailSection();
    refreshData();
}

window.addEventListener('DOMContentLoaded', initialize);
