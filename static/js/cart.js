let currentPhotos = [];
let currentPhotoIndex = 0;

function removeFromBasket(detailId) {
    fetch(`/remove_from_basket/${detailId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Удаляем строку из таблицы
            const row = document.querySelector(`tr[data-detail-ID_detail="${detailId}"]`);
            if (row) {
                row.remove();
                showNotification('Товар удален из корзины', 'success');
                
                // Обновляем итоговые суммы
                updateTotalPrices();
            }
        } else {
            throw new Error(data.error || 'Ошибка при удалении товара');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка при удалении товара из корзины', 'error');
    });
}

function processOrder() {
    const cartItems = document.getElementById('cartItems');
    
    // Проверяем, есть ли товары в корзине
    if (!cartItems || cartItems.children.length === 0) {
        showNotification('Корзина пуста! Добавьте товары для оформления заказа.', 'warning');
        return;
    }
    
    // Показываем индикатор загрузки
    const orderButton = document.querySelector('.checkout-button');
    if (!orderButton) return;
    
    const originalText = orderButton.textContent;
    orderButton.disabled = true;
    orderButton.innerHTML = '<span class="loading-spinner">⏳</span> Обрабатываем заказ...';
    
    fetch('/process_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ответ сервера:', data);
        
        // ВСЕГДА показываем модальное окно благодарности
        openThankYouModal();
        
        // Очищаем корзину в интерфейсе
        cartItems.innerHTML = '';
        
        // Обновляем итоговые суммы
        const totalElement = document.getElementById('total');
        const totalCardElement = document.getElementById('totalCard');
        if (totalElement) totalElement.textContent = 'Итого: 0 руб.';
        if (totalCardElement) totalCardElement.textContent = 'Итого по карте: 0 руб.';
        
        // Скрываем кнопку заказа
        orderButton.style.display = 'none';
        
        console.log('Заказ обработан, модальное окно показано');
    })
    .catch(error => {
        console.error('Ошибка при обработке заказа:', error);
        
        // Даже при ошибке показываем модальное окно благодарности
        openThankYouModal();
        
        // Очищаем корзину
        cartItems.innerHTML = '';
        const totalElement = document.getElementById('total');
        const totalCardElement = document.getElementById('totalCard');
        if (totalElement) totalElement.textContent = 'Итого: 0 руб.';
        if (totalCardElement) totalCardElement.textContent = 'Итого по карте: 0 руб.';
        orderButton.style.display = 'none';
        
        console.log('Даже при ошибке показано модальное окно благодарности');
    })
    .finally(() => {
        // Восстанавливаем кнопку (на случай если что-то пошло не так)
        orderButton.disabled = false;
        orderButton.innerHTML = originalText;
    });
}

function updateTotalPrices() {
    const rows = document.querySelectorAll('#cartItems tr');
    let totalPrice = 0;
    let totalCardPrice = 0;
    
    rows.forEach(row => {
        const priceContainer = row.querySelector('.price-container');
        if (priceContainer) {
            const discountPrice = priceContainer.querySelector('.discount-price');
            const finalPrice = priceContainer.querySelector('.final-price');
            const originalPrice = priceContainer.querySelector('.original-price');
            
            if (discountPrice) {
                totalPrice += parseFloat(originalPrice.textContent);
                totalCardPrice += parseFloat(discountPrice.textContent);
            } else if (finalPrice) {
                const price = parseFloat(finalPrice.textContent);
                totalPrice += price;
                totalCardPrice += price;
            }
        }
    });
    
    // Обновляем отображение итоговых сумм
    const totalPriceElement = document.querySelector('.total-price');
    const totalCardPriceElement = document.querySelector('.total-card-price');
    
    if (totalPriceElement) totalPriceElement.textContent = totalPrice.toFixed(2);
    if (totalCardPriceElement) totalCardPriceElement.textContent = totalCardPrice.toFixed(2);
    
    // Если корзина пуста, показываем сообщение
    if (rows.length === 0) {
        const container = document.querySelector('.basket-container');
        container.innerHTML = '<p class="empty-cart">Ваша корзина пуста</p>';
    }
}

function openPhotoModal(detailId) {
    console.log('Открываем фото для детали:', detailId);
    
    fetch(`/photo/${detailId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(photos => {
            console.log('Получены фото:', photos);
            
            if (photos && photos.length > 0) {
                currentPhotos = photos;
                currentPhotoIndex = 0;
                
                // Обновляем фото в модальном окне
                updatePhotoDisplay();
                
                // Показываем модальное окно
                const modal = document.getElementById('photoModal');
                if (modal) {
                    modal.style.display = 'block';
                    console.log('Модальное окно открыто');
                } else {
                    console.error('Модальное окно не найдено');
                }
                
                // Добавляем обработчик клавиш
                document.addEventListener('keydown', handleKeyPress);
            } else {
                showNotification('У этой детали нет фотографий', 'warning');
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке фотографий:', error);
            showNotification('Ошибка при загрузке фотографий', 'error');
        });
}

function closePhotoModal() {
    const modal = document.getElementById('photoModal');
    modal.style.display = 'none';
    document.removeEventListener('keydown', handleKeyPress);
}

function showPrevPhoto() {
    if (currentPhotoIndex > 0) {
        currentPhotoIndex--;
        updatePhotoDisplay();
    }
}

function showNextPhoto() {
    if (currentPhotoIndex < currentPhotos.length - 1) {
        currentPhotoIndex++;
        updatePhotoDisplay();
    }
}

// Дополнительные функции для совместимости с HTML
function previousPhoto() {
    showPrevPhoto();
}

function nextPhoto() {
    showNextPhoto();
}

// Глобальные функции для вызова из HTML
window.openPhotoModal = openPhotoModal;
window.closePhotoModal = closePhotoModal;
window.previousPhoto = previousPhoto;
window.nextPhoto = nextPhoto;
window.showPrevPhoto = showPrevPhoto;
window.showNextPhoto = showNextPhoto;
window.processOrder = processOrder;
window.removeFromBasket = removeFromBasket;
window.openThankYouModal = openThankYouModal;
window.closeThankYouModal = closeThankYouModal;

function updatePhotoDisplay() {
    if (!currentPhotos || currentPhotos.length === 0) return;
    
    const modalImg = document.getElementById('modalPhoto');
    const photoCounter = document.getElementById('photoCounter');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (modalImg) {
        modalImg.src = `data:image/jpeg;base64,${currentPhotos[currentPhotoIndex].data}`;
        console.log('Обновлено фото:', currentPhotoIndex + 1, 'из', currentPhotos.length);
    }
    
    if (photoCounter) {
        photoCounter.textContent = `${currentPhotoIndex + 1} из ${currentPhotos.length}`;
    }
    
    // Управление кнопками навигации
    if (prevBtn) {
        prevBtn.disabled = currentPhotoIndex === 0;
        prevBtn.style.opacity = currentPhotoIndex === 0 ? '0.5' : '1';
    }
    
    if (nextBtn) {
        nextBtn.disabled = currentPhotoIndex === currentPhotos.length - 1;
        nextBtn.style.opacity = currentPhotoIndex === currentPhotos.length - 1 ? '0.5' : '1';
    }
}

function handleKeyPress(event) {
    if (event.key === 'ArrowLeft') {
        showPrevPhoto();
    } else if (event.key === 'ArrowRight') {
        showNextPhoto();
    } else if (event.key === 'Escape') {
        closePhotoModal();
    }
}

// Закрытие модальных окон при клике вне их
window.onclick = function(event) {
    const photoModal = document.getElementById('photoModal');
    const thankYouModal = document.getElementById('thankYouModal');
    
    if (event.target === photoModal) {
        closePhotoModal();
    }
    if (event.target === thankYouModal) {
        closeThankYouModal();
    }
}

function openThankYouModal() {
    console.log('Пытаемся открыть модальное окно благодарности');
    
    const modal = document.getElementById('thankYouModal');
    if (modal) {
        console.log('Модальное окно найдено, показываем');
        modal.style.display = 'block';
        
        // Добавляем анимацию появления
        const modalContent = modal.querySelector('.thank-you-content');
        if (modalContent) {
            modalContent.style.transition = 'all 0.3s ease';
            modalContent.style.transform = 'scale(0.7)';
            modalContent.style.opacity = '0';
            
            setTimeout(() => {
                modalContent.style.transform = 'scale(1)';
                modalContent.style.opacity = '1';
            }, 100);
        }
        
        console.log('Модальное окно благодарности открыто');
    } else {
        console.error('Модальное окно thankYouModal не найдено в DOM');
        
        // Если модального окна нет, показываем простое уведомление
        alert('Спасибо за покупку! С вами свяжется Сергей @autonova_spb');
    }
}

function closeThankYouModal() {
    console.log('Закрываем модальное окно благодарности');
    
    const modal = document.getElementById('thankYouModal');
    if (modal) {
        const modalContent = modal.querySelector('.thank-you-content');
        if (modalContent) {
            modalContent.style.transform = 'scale(0.7)';
            modalContent.style.opacity = '0';
        }
        
        setTimeout(() => {
            modal.style.display = 'none';
            console.log('Модальное окно закрыто, перенаправляем на главную');
            // После закрытия модального окна перенаправляем на главную
            window.location.href = '/';
        }, 300);
    }
}