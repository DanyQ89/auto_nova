let currentPhotos = [];
let currentPhotoIndex = 0;
let currentDetailId = null;

function fetchPhoto(detailId) {
    console.log('Fetching photos for detail:', detailId);
    currentDetailId = detailId;
    
    // Fetch photos from the server
    fetch(`/api/photos/${detailId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received photos data:', data);
            currentPhotos = data.photos || [];
            currentPhotoIndex = 0;
            updatePhotoDisplay();
            document.getElementById('photoModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching photos:', error);
            alert('Ошибка при загрузке фотографий: ' + error.message);
        });
}

function updatePhotoDisplay() {
    const currentPhoto = document.getElementById('currentPhoto');
    const thumbnailsContainer = document.getElementById('thumbnailsContainer');
    
    // Update main photo
    if (currentPhotos.length > 0) {
        currentPhoto.src = currentPhotos[currentPhotoIndex];
        currentPhoto.style.display = 'block';
    } else {
        currentPhoto.style.display = 'none';
    }

    // Update thumbnails
    thumbnailsContainer.innerHTML = '';
    currentPhotos.forEach((photo, index) => {
        const thumbnail = document.createElement('img');
        thumbnail.src = photo;
        thumbnail.className = `thumbnail ${index === currentPhotoIndex ? 'active' : ''}`;
        thumbnail.onclick = () => {
            currentPhotoIndex = index;
            updatePhotoDisplay();
        };
        thumbnailsContainer.appendChild(thumbnail);
    });
}

function prevPhoto() {
    if (currentPhotos.length > 0) {
        currentPhotoIndex = (currentPhotoIndex - 1 + currentPhotos.length) % currentPhotos.length;
        updatePhotoDisplay();
    }
}

function nextPhoto() {
    if (currentPhotos.length > 0) {
        currentPhotoIndex = (currentPhotoIndex + 1) % currentPhotos.length;
        updatePhotoDisplay();
    }
}

function editCurrentPhoto() {
    document.getElementById('photoInput').click();
}

function deleteCurrentPhoto() {
    if (currentPhotos.length === 0) return;
    
    if (confirm('Вы уверены, что хотите удалить это фото?')) {
        const photoToDelete = currentPhotos[currentPhotoIndex];
        fetch(`/api/photos/${currentDetailId}/${encodeURIComponent(photoToDelete)}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentPhotos.splice(currentPhotoIndex, 1);
                if (currentPhotos.length === 0) {
                    currentPhotoIndex = 0;
                } else {
                    currentPhotoIndex = Math.min(currentPhotoIndex, currentPhotos.length - 1);
                }
                updatePhotoDisplay();
            } else {
                alert('Ошибка при удалении фото');
            }
        })
        .catch(error => {
            console.error('Error deleting photo:', error);
            alert('Ошибка при удалении фото');
        });
    }
}

function addNewPhoto() {
    document.getElementById('photoInput').click();
}

function handlePhotoUpload(input) {
    if (input.files && input.files[0]) {
        const formData = new FormData();
        formData.append('photo', input.files[0]);
        formData.append('detail_id', currentDetailId);

        fetch('/api/photos/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentPhotos.push(data.photo_url);
                currentPhotoIndex = currentPhotos.length - 1;
                updatePhotoDisplay();
            } else {
                alert('Ошибка при загрузке фото');
            }
        })
        .catch(error => {
            console.error('Error uploading photo:', error);
            alert('Ошибка при загрузке фото');
        });
    }
}

function closePhotoModal() {
    document.getElementById('photoModal').style.display = 'none';
    currentPhotos = [];
    currentPhotoIndex = 0;
    currentDetailId = null;
} 