function getDetail(partNumber, event) {
        event.preventDefault(); // Предотвращаем переход по ссылке
        fetch(`/get_detail/${partNumber}`)
            .then(response => response.json())
            .then(data => {
                const modal = document.getElementById('detail-modal');
                const modalContent = modal.querySelector('.modal-details');

                // Заполняем содержимое
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

                // Показываем модальное окно
                modal.style.display = 'flex';
            });
    }

    // Обработчик закрытия
    function closeDetail() {
        const modal = document.getElementById('detail-modal');
        modal.style.display = 'none';
    }

    // Закрытие по клику вне окна
    window.onclick = function(event) {
        const modal = document.getElementById('detail-modal');
        if (event.target == modal) {
            closeDetail();
        }
    }

    // Обновляем обработчики карточек
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
                alert('Товар добавлен в корзину');
            } else {
                alert('Ошибка при добавлении товара в корзину');
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        const sliders = document.querySelectorAll('.slider');
        sliders.forEach((slider, index) => {
            const photos = slider.querySelectorAll('.slider-photo');
            if (photos.length > 0) {
                photos[0].classList.add('active'); // Показываем первую фотографию
            }
        });
    });

    function changePhoto(direction, sliderIndex) {
        const slider = document.querySelectorAll('.slider')[sliderIndex];
        if (!slider) {
            alert('Slider not found');
            return;
        }

        const photos = slider.querySelectorAll('.slider-photo');
        if (photos.length === 0) {
            alert('No photos found');
            return;
        }

        let activeIndex = -1;

        // Находим индекс активной фотографии
        photos.forEach((photo, index) => {
            if (photo.classList.contains('active')) {
                activeIndex = index;
                photo.classList.remove('active');
            }
        });

        // Вычисляем новый индекс
        let newIndex = activeIndex + direction;
        if (newIndex < 0) {
            newIndex = photos.length - 1; // Переход к последней фотографии
        } else if (newIndex >= photos.length) {
            newIndex = 0; // Переход к первой фотографии
        }

        // Показываем новую фотографию
        photos[newIndex].classList.add('active');
}