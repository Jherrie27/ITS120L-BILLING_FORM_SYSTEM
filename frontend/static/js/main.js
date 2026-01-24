// frontend/static/js/main.js

let draggedCard = null;

// Search functionality
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('.card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(searchTerm) ? 'block' : 'none';
    });
});

// Drag and drop setup
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('dragstart', handleDragStart);
    card.addEventListener('dragend', handleDragEnd);
});

document.querySelectorAll('.drop-zone').forEach(zone => {
    zone.addEventListener('dragover', handleDragOver);
    zone.addEventListener('drop', handleDrop);
    zone.addEventListener('dragleave', handleDragLeave);
});

function handleDragStart(e) {
    draggedCard = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');
    return false;
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    this.classList.remove('drag-over');
    
    if (draggedCard) {
        const newStatus = this.dataset.status;
        const itemId = draggedCard.dataset.id;
        
        // Move card visually
        this.appendChild(draggedCard);
        
        // Update counts
        updateCounts();
        
        // Send to Django backend
        updateItemStatus(itemId, newStatus);
    }
    
    return false;
}

function updateCounts() {
    document.querySelectorAll('.column').forEach(column => {
        const count = column.querySelectorAll('.card').length;
        column.querySelector('.column-count').textContent = count;
    });
}

function updateItemStatus(itemId, status) {
    fetch('/update-status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: itemId,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            alert('Error updating status');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating status');
        location.reload();
    });
}