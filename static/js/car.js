function getDetail(partNumber, event) {
    event.preventDefault();
    fetch(`/get_detail/${partNumber}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('detail-modal');
            const modalContent = modal.querySelector('.modal-details');

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
                <button onclick="addToCart('${data.ID_detail}')"
                        class="add-to-cart modal-cart-btn">
                    Добавить в корзину
                </button>
            `;

            modal.style.display = 'flex';
        });
}

function closeDetail() {
    const modal = document.getElementById('detail-modal');
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('detail-modal');
    if (event.target == modal) {
        closeDetail();
    }
}

document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('click', function(e) {
        const productId = this.querySelector('.add-to-cart').getAttribute('onclick').match(/'([^']+)'/)[1];
        getDetail(productId, e);
    });
});

function addToCart(productId) {
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