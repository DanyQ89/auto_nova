function getDetail(partNumber, event) {
    event.preventDefault();
    event.stopPropagation();
    
    fetch(`/get_detail/${partNumber}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('detail-modal');
            const modalContent = modal.querySelector('.modal-details');

            // Создаем галерею фотографий
            let photosHtml = '';
            if (data.photos && data.photos.length > 0) {
                photosHtml = `
                    <div class="modal-photos">
                        <h3>Фотографии товара</h3>
                        <div class="modal-photos-grid">
                            ${data.photos.map((photo, index) => `
                                <div class="modal-photo-item">
                                    <img src="data:image/jpg;base64,${photo}" 
                                         alt="${data.name} - фото ${index + 1}"
                                         class="modal-photo"
                                         onclick="showFullPhoto('data:image/jpg;base64,${photo}')">
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            modal.querySelector('.modal-image').src = `data:image/jpg;base64,${data.photo}`;
            modalContent.innerHTML = `
                <h2>${data.name}</h2>
                <div class="detail-grid">
                    <div class="detail-item">
                        <span class="detail-label">Артикул:</span>
                        <span class="detail-value">${data.orig_number}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Бренд:</span>
                        <span class="detail-value">${data.brand}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Модель:</span>
                        <span class="detail-value">${data.model_and_year}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Состояние:</span>
                        <span class="detail-value">${data.condition}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Цвет:</span>
                        <span class="detail-value">${data.color}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Цена:</span>
                        <span class="detail-value price">${data.price} ₽</span>
                    </div>
                    ${data.price_w_discount ? `
                    <div class="detail-item">
                        <span class="detail-label">Цена по карте:</span>
                        <span class="detail-value discount-price">${data.price_w_discount} ₽</span>
                    </div>` : ''}
                    <div class="full-description">${data.comment}</div>
                </div>
                ${photosHtml}
                <button onclick="addToCartFromModal('${data.ID_detail}')"
                        class="add-to-cart modal-cart-btn">
                    Добавить в корзину
                </button>
            `;

            modal.style.display = 'flex';
        });
}

function showFullPhoto(photoSrc) {
    const fullPhotoModal = document.getElementById('full-photo-modal');
    if (!fullPhotoModal) {
        // Создаем модальное окно для полноразмерного фото
        const modal = document.createElement('div');
        modal.id = 'full-photo-modal';
        modal.className = 'full-photo-overlay';
        modal.innerHTML = `
            <div class="full-photo-content">
                <button onclick="closeFullPhoto()" class="full-photo-close">×</button>
                <img src="${photoSrc}" alt="Полноразмерное фото" class="full-photo-image">
            </div>
        `;
        document.body.appendChild(modal);
    } else {
        fullPhotoModal.querySelector('.full-photo-image').src = photoSrc;
        fullPhotoModal.style.display = 'flex';
    }
}

function closeFullPhoto() {
    const modal = document.getElementById('full-photo-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function closeDetail() {
    const modal = document.getElementById('detail-modal');
    modal.style.display = 'none';
}

// Закрытие полноразмерного фото по клику вне изображения
window.addEventListener('click', function(event) {
    const fullPhotoModal = document.getElementById('full-photo-modal');
    if (event.target === fullPhotoModal) {
        closeFullPhoto();
    }
    
    const detailModal = document.getElementById('detail-modal');
    if (event.target === detailModal) {
        closeDetail();
    }
});

// Закрытие по Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeDetail();
        closeFullPhoto();
    }
});

// Предотвращаем всплытие событий от кнопки "Добавить в корзину"
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    });
});

function addToCart(productId) {
    event.stopPropagation();
    fetch(`/add_to_basket/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Товар добавлен в корзину', 'success');
        } else {
            showNotification('Ошибка при добавлении товара в корзину', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка при добавлении в корзину:', error);
        showNotification('Произошла ошибка при добавлении товара', 'error');
    });
}

function addToCartFromModal(productId) {
    fetch(`/add_to_basket/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Товар добавлен в корзину', 'success');
        } else {
            showNotification('Ошибка при добавлении товара в корзину', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка при добавлении в корзину:', error);
        showNotification('Произошла ошибка при добавлении товара', 'error');
    });
}

function changePhoto(direction, sliderIndex) {
    const slider = document.querySelectorAll('.slider')[sliderIndex];
    if (!slider) return;

    const slides = slider.querySelectorAll('.slide-wrapper');
    if (slides.length === 0) return;

    let currentIndex = -1;
    slides.forEach((slide, index) => {
        if (slide.classList.contains('active')) {
            currentIndex = index;
            slide.classList.remove('active');
        }
    });

    let newIndex = currentIndex + direction;
    if (newIndex < 0) {
        newIndex = slides.length - 1;
    } else if (newIndex >= slides.length) {
        newIndex = 0;
    }

    slides[newIndex].classList.add('active');
}

document.addEventListener('DOMContentLoaded', function() {
    const sliders = document.querySelectorAll('.slider');
    sliders.forEach((slider, index) => {
        const slides = slider.querySelectorAll('.slide-wrapper');
        if (slides.length > 0) {
            slides[0].classList.add('active');
        }
    });
});