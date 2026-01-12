document.addEventListener("DOMContentLoaded", function() {
    const chatMessagesContainer = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const chatErrorsContainer = document.getElementById("chat-errors");
    const messageCountBadge = document.getElementById("message-count");

    // Asegurarse de que eventId esté definido (viene del template)
    if (typeof eventId === "undefined" || eventId === null) {
        console.error("eventId no está definido. Asegúrate de que el script en el template lo proporcione.");
        return;
    }

    function escapeHtml(text) {
        const map = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "\"": "&quot;",
            "\'": "&#039;"
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    function createMessageElement(message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", "card", "mb-2");
        messageDiv.setAttribute("data-message-id", message.id);

        if (message.is_highlighted) {
            messageDiv.classList.add("highlighted");
        }

        let deleteButtonHtml = "";
        if (message.can_delete) {
            deleteButtonHtml = `
                <button type="button" class="btn btn-sm btn-outline-danger delete-message" data-message-id="${message.id}">
                    <i class="fas fa-trash"></i>
                </button>
            `;
        }

        messageDiv.innerHTML = `
            <div class="card-body p-2">
                <div class="message-header d-flex justify-content-between align-items-center">
                    <strong>${escapeHtml(message.display_name)}</strong>
                    <small class="text-muted">${message.created_at}</small>
                </div>
                <p class="message-content mb-0">${escapeHtml(message.message)}</p>
                <div class="message-actions mt-1">
                    ${deleteButtonHtml}
                </div>
            </div>
        `;
        return messageDiv;
    }

    function scrollToBottom() {
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }

    function updateMessageCount(count) {
        if (messageCountBadge) {
            messageCountBadge.textContent = count;
        }
    }

    async function loadMessages() {
        try {
            const response = await fetch(`/chat/${eventId}/messages/`);
            const data = await response.json();

            if (response.ok) {
                chatMessagesContainer.innerHTML = ""; // Limpiar mensajes existentes
                data.messages.forEach(message => {
                    chatMessagesContainer.appendChild(createMessageElement(message));
                });
                scrollToBottom();
                updateMessageCount(data.messages.length);
            } else {
                console.error("Error al cargar mensajes:", data);
                chatMessagesContainer.innerHTML = `<p class="text-danger text-center">Error al cargar mensajes: ${data.error || "Desconocido"}</p>`;
            }
        } catch (error) {
            console.error("Error de red al cargar mensajes:", error);
            chatMessagesContainer.innerHTML = `<p class="text-danger text-center">Error de conexión al cargar mensajes.</p>`;
        }
    }

    async function sendMessage(event) {
        event.preventDefault();
        chatErrorsContainer.innerHTML = ""; // Limpiar errores previos

        const formData = new FormData(chatForm);
        const messageText = formData.get("message");

        if (!messageText || !messageText.trim()) {
            chatErrorsContainer.innerHTML = "El mensaje no puede estar vacío.";
            return;
        }

        try {
            const response = await fetch(`/chat/${eventId}/send/`, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            });
            const data = await response.json();

            if (response.ok && data.success) {
                chatForm.reset(); // Limpiar el formulario
                loadMessages(); // Recargar mensajes para ver el nuevo
            } else {
                console.error("Error al enviar mensaje:", data);
                if (data.errors && data.errors.message) {
                    chatErrorsContainer.innerHTML = data.errors.message.join("<br>");
                } else if (data.errors && data.errors.__all__) {
                    chatErrorsContainer.innerHTML = data.errors.__all__;
                } else {
                    chatErrorsContainer.innerHTML = "Error desconocido al enviar mensaje.";
                }
            }
        } catch (error) {
            console.error("Error de red al enviar mensaje:", error);
            chatErrorsContainer.innerHTML = "Error de conexión al enviar mensaje.";
        }
    }

    async function deleteMessage(messageId) {
        if (!confirm("¿Estás seguro de que quieres eliminar este mensaje?")) {
            return;
        }

        try {
            const response = await fetch(`/chat/message/${messageId}/delete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            });
            const data = await response.json();

            if (response.ok && data.success) {
                loadMessages(); // Recargar mensajes
            } else {
                console.error("Error al eliminar mensaje:", data);
                alert(data.error || "Error desconocido al eliminar mensaje.");
            }
        } catch (error) {
            console.error("Error de red al eliminar mensaje:", error);
            alert("Error de conexión al eliminar mensaje.");
        }
    }

    // Event Listeners
    if (chatForm) {
        chatForm.addEventListener("submit", sendMessage);
    }

    chatMessagesContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("delete-message")) {
            const messageId = event.target.getAttribute("data-message-id");
            if (messageId) {
                deleteMessage(messageId);
            }
        }
    });

    // Inicialización
    loadMessages();
    setInterval(loadMessages, 3000); // Polling cada 3 segundos
});
