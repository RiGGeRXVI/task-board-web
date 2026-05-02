document.addEventListener("DOMContentLoaded", () => {
    const taskCards = document.querySelectorAll(".task-card");
    const columns = document.querySelectorAll(".column");

    
    let draggedCard = null;
    let draggedTaskId = null;

    taskCards.forEach(card => {
        card.addEventListener("dragstart", () => {
            draggedCard = card;
            draggedTaskId = card.dataset.taskId;
            card.classList.add("dragging");
        });

        card.addEventListener("dragend", () => {
            card.classList.remove("dragging");
        });
    });

    columns.forEach(column => {
        column.addEventListener("dragover", (event) => {
            event.preventDefault();
            column.classList.add("column-hover");
        });

        column.addEventListener("dragleave", () => {
            column.classList.remove("column-hover");
        });

        column.addEventListener("drop", async (event) => {
            event.preventDefault();
            column.classList.remove("column-hover");

            const newStatus = column.dataset.status;

            if (!draggedCard || !draggedTaskId) return;

            try {
                const response = await fetch(`/tasks/${draggedTaskId}/move`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ status: newStatus })
                });

                const result = await response.json();

                if (result.success) {
                    column.appendChild(draggedCard);
                } else {
                    alert("Не удалось переместить задачу");
                }
            } catch (error) {
                alert("Ошибка при перемещении задачи");
            }
        });
    });
});