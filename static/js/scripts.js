// Получаем модальное окно
var modal = document.getElementById("detailModal");

// Получаем кнопку, которая открывает модальное окно
var btn = document.getElementById("addDetailBtn");

// Получаем элемент <span>, который закрывает модальное окно
var span = document.getElementsByClassName("close")[0];

// Когда пользователь нажимает на кнопку, открывается модальное окно
if (btn) {
    btn.onclick = function() {
        openModal('add');
    };
}

// Когда пользователь нажимает на <span> (x), закрывается модальное окно
if (span) {
    span.onclick = function() {
        closeModal();
    };
}

function toggleMenu() {
    const menu = document.getElementById('menu');
    menu.classList.toggle('active');
}
// Когда пользователь нажимает в любом месте вне модального окна, оно закрывается
window.onclick = function(event) {
    const menu = document.getElementById('menu');
    const hamburger = document.querySelector('.hamburger'); // Получаем элемент гамбургера

    // Проверяем, был ли клик вне меню и вне гамбургера
    if (event.target !== menu && event.target !== hamburger && menu.classList.contains('active')){
        menu.classList.remove('active'); // Закрываем меню
    } else if (event.target === modal) {
        closeModal();
    } else if (event.target === photoModal) {
        closePhotoModal();
    }
};

// Функция для открытия модального окна
function openModal(action, detail = {}) {
    const title = document.getElementById('modalTitle');
    const detailId = document.getElementById('detailId');
    const nameInput = document.getElementById('name');
    const priceInput = document.getElementById('price');
    const priceWDiscountInput = document.getElementById('price_w_discount');
    const dateInput = document.getElementById('data_created');
    const commentInput = document.getElementById('comment');
    const origNumberInput = document.getElementById('orig_number');
    const conditionInput = document.getElementById('condition');
    const percentInput = document.getElementById('percent');
    const colorInput = document.getElementById('color');
    const skladInput = document.getElementById('sklad');
    const idDetailInput = document.getElementById('ID_detail');
    const brandInput = document.getElementById('brand');
    const modelAndYearInput = document.getElementById('model_and_year');
    const submitButton = document.getElementById('submitButton');

    if (action === 'edit') {
        title.textContent = 'Редактировать деталь';
        // Заполнение полей данными детали
        detailId.value = detail.id;
        skladInput.value = detail.sklad || '';
        idDetailInput.value = detail.ID_detail || '';
        brandInput.value = detail.brand || '';
        modelAndYearInput.value = detail.model_and_year || '';
        nameInput.value = detail.name || '';
        priceInput.value = detail.price || '';
        priceWDiscountInput.value = detail.price_w_discount || '';
        dateInput.value = detail.data_created || '';
        commentInput.value = detail.comment || '';
        origNumberInput.value = detail.orig_number || '';
        conditionInput.value = detail.condition || '';
        percentInput.value = detail.percent || 0;
        colorInput.value = detail.color || '';
        submitButton.textContent = 'Обновить данные';
    } else {
        title.textContent = 'Добавить деталь';
        // Очистка полей для добавления новой детали
        detailId.value = '';
        skladInput.value = '';
        idDetailInput.value = '';
        brandInput.value = '';
        modelAndYearInput.value = '';
        nameInput.value = '';
        priceInput.value = '';
        priceWDiscountInput.value = '';
        dateInput.value = '';
        commentInput.value = '';
        origNumberInput.value = '';
        conditionInput.value = '';
        percentInput.value = 0;
        colorInput.value = '';
        submitButton.textContent = 'Сохранить';
    }
    modal.style.display = 'block';
}

// Функция для закрытия модального окна
function closeModal() {
    modal.style.display = 'none';
}

// Функция для редактирования детали
function editDetail(detailId) {
    fetch(`/update_detail/${detailId}`)
        .then(response => response.json())
        .then(detail => {
            openModal('edit', detail);
        })
        .catch(error => console.error('Ошибка:', error));
}

// Глобальные переменные для работы с фотографиями
let currentPhotoIndex = 0;
let photoData = [];
let currentDetailId = null;

async function fetchPhoto(detailId) {
    try {
        currentDetailId = detailId;
        const response = await fetch(`/photo/${detailId}`); // Запрос на сервер для получения фото
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        photoData = await response.json(); // Получаем данные изображения как массив
        openPhotoModal(photoData); // Открываем модальное окно с изображениями
    } catch (error) {
        console.error('Ошибка при получении фото:', error);
    }
}

function openPhotoModal(photos) {
    const modal = document.getElementById('photoModal'); // Получаем элемент модального окна
    const photoContainer = modal.querySelector('.photo-container'); // Получаем контейнер для фотографий
    const totalPhotosElement = document.getElementById('total-photos');
    const currentPhotoIndexElement = document.getElementById('current-photo-index');

    // Очищаем контейнер перед добавлением новых изображений
    photoContainer.innerHTML = '';
    
    // Обновляем счетчик фотографий
    totalPhotosElement.textContent = photos.length;
    currentPhotoIndex = 0;
    currentPhotoIndexElement.textContent = currentPhotoIndex + 1;

    // Добавляем каждую фотографию в контейнер
    photos.forEach((photo, index) => {
        const img = document.createElement('img'); // Создаем элемент изображения
        img.src = `data:image/jpeg;base64,${photo.data}`; // Устанавливаем источник изображения
        img.alt = `Photo ${index + 1}`; // Устанавливаем альтернативный текст
        img.dataset.index = index; // Сохраняем индекс фотографии
        img.dataset.id = photo.id; // Сохраняем ID фотографии
        photoContainer.appendChild(img); // Добавляем изображение в контейнер
    });

    // Показываем модальное окно
    modal.style.display = 'block';
    
    // Обновляем видимость кнопок навигации
    updateCarouselButtons();
}

function updateCarouselButtons() {
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    const deleteButton = document.querySelector('.delete-photo');
    
    // Скрываем кнопки навигации, если фотографий меньше 2
    if (photoData.length <= 1) {
        prevButton.style.display = 'none';
        nextButton.style.display = 'none';
    } else {
        prevButton.style.display = 'flex';
        nextButton.style.display = 'flex';
    }
    
    // Скрываем кнопку удаления, если фотографий нет
    if (photoData.length === 0) {
        deleteButton.style.display = 'none';
    } else {
        deleteButton.style.display = 'flex';
    }
}

function prevPhoto() {
    if (currentPhotoIndex > 0) {
        currentPhotoIndex--;
        updateCarousel();
    }
}

function nextPhoto() {
    if (currentPhotoIndex < photoData.length - 1) {
        currentPhotoIndex++;
        updateCarousel();
    }
}

function updateCarousel() {
    const photoContainer = document.querySelector('.photo-container');
    const currentPhotoIndexElement = document.getElementById('current-photo-index');
    
    // Обновляем позицию карусели
    photoContainer.style.transform = `translateX(-${currentPhotoIndex * 100}%)`;
    
    // Обновляем счетчик
    currentPhotoIndexElement.textContent = currentPhotoIndex + 1;
}

function editCurrentPhoto() {
    // Если нет фотографий, нечего редактировать
    if (photoData.length === 0) return;
    
    // Открываем диалог выбора файла
    document.getElementById('edit-photo-input').click();
}

function uploadEditedPhoto() {
    const fileInput = document.getElementById('edit-photo-input');
    const file = fileInput.files[0];
    
    if (file) {
        // Получаем ID текущей фотографии
        const photoId = getCurrentPhotoId();
        
        if (photoId) {
            // Отправляем запрос на редактирование фото
            editPhoto(photoId, file);
        }
    }
    
    // Сбрасываем input
    fileInput.value = '';
}

function getCurrentPhotoId() {
    // Получаем ID текущей фотографии из атрибута data-id
    const currentImg = document.querySelector(`.photo-container img[data-index="${currentPhotoIndex}"]`);
    if (currentImg) {
        return currentImg.dataset.id;
    }
    return null;
}

async function editPhoto(photoId, file) {
    const formData = new FormData();
    formData.append('file', file); // Добавляем файл в FormData

    try {
        const response = await fetch(`/edit_photo/${photoId}`, {
            method: 'PUT',
            body: formData, // Отправляем FormData
        });

        const result = await response.json();

        if (response.ok) {
            console.log(result.message); // Успешное обновление
            // Обновляем фото в карусели
            const reader = new FileReader();
            reader.onload = function(e) {
                // Преобразуем файл в base64
                const base64String = e.target.result.split(',')[1];
                // Обновляем фото в массиве
                photoData[currentPhotoIndex].data = base64String;
                // Обновляем изображение в карусели
                const img = document.querySelector(`.photo-container img[data-index="${currentPhotoIndex}"]`);
                if (img) {
                    img.src = `data:image/jpeg;base64,${base64String}`;
                }
            };
            reader.readAsDataURL(file);
        } else {
            console.error(`Ошибка: ${result.message}`); // Ошибка
        }
    } catch (error) {
        console.error('Ошибка при редактировании фото:', error);
    }
}

function addNewPhoto() {
    const fileInput = document.getElementById('add-photo-input');
    const file = fileInput.files[0];
    
    if (file && currentDetailId) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('detail_id', currentDetailId);
        
        fetch('/add_photo', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при загрузке файла');
            }
            return response.json();
        })
        .then(data => {
            console.log('Успешно загружено:', data);
            // Обновляем список фотографий
            fetchPhoto(currentDetailId);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
    
    // Сбрасываем input
    fileInput.value = '';
}

function deleteCurrentPhoto() {
    // Если нет фотографий, нечего удалять
    if (photoData.length === 0) return;
    
    // Получаем ID текущей фотографии
    const photoId = getCurrentPhotoId();
    
    if (photoId !== null) {
        // Запрашиваем красивое подтверждение
        showConfirmDialog(
            'Вы уверены, что хотите удалить это фото?',
            () => deletePhoto(photoId),
            () => console.log('Удаление фото отменено')
        );
    }
}

async function deletePhoto(photoId) {
    try {
        const response = await fetch(`/delete_photo/${photoId}`, {
            method: 'DELETE',
        });

        const result = await response.json();

        if (response.ok) {
            console.log(result.message); // Успешное удаление
            // Удаляем фото из массива
            photoData.splice(currentPhotoIndex, 1);
            
            // Если удалили последнее фото, закрываем модальное окно
            if (photoData.length === 0) {
                closePhotoModal();
            } else {
                // Иначе обновляем карусель
                openPhotoModal(photoData);
            }
        } else {
            console.log(`Ошибка: ${result.message}`); // Ошибка
        }
    } catch (error) {
        console.error('Ошибка при удалении фото:', error);
    }
}

function closePhotoModal() {
    const modal = document.getElementById('photoModal');
    modal.style.display = "none"; // Скрываем модальное окно
}

function showNotification(message, type = 'success', duration = 3000) {
    const container = document.getElementById('notification-container');
    
    if (!container) {
        console.error('Контейнер для уведомлений не найден');
        return;
    }
    
    const notification = document.createElement('div');

    // Настройки иконок в зависимости от типа
    const icons = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ'
    };

    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <strong>${icons[type]}</strong>
        <span>${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(notification);

    // Автоматическое удаление через указанное время
    const timeoutId = setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'fadeOut 0.3s ease-in forwards';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, duration);

    // Добавляем возможность закрыть уведомление кликом на крестик
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', function(e) {
        e.stopPropagation();
        clearTimeout(timeoutId);
        notification.style.animation = 'fadeOut 0.3s ease-in forwards';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    });
    
    // Ограничиваем количество уведомлений на экране
    const notifications = container.querySelectorAll('.notification');
    if (notifications.length > 5) {
        const oldest = notifications[0];
        oldest.style.animation = 'fadeOut 0.3s ease-in forwards';
        setTimeout(() => {
            if (oldest.parentNode) {
                oldest.remove();
            }
        }, 300);
    }
}

// Красивая функция подтверждения
function showConfirmDialog(message, onConfirm, onCancel) {
    // Создаем модальное окно подтверждения
    const modal = document.createElement('div');
    modal.className = 'confirm-modal';
    modal.innerHTML = `
        <div class="confirm-content">
            <div class="confirm-header">
                <div class="confirm-icon">?</div>
                <h3>Подтверждение</h3>
            </div>
            <div class="confirm-message">
                ${message}
            </div>
            <div class="confirm-buttons">
                <button class="confirm-btn cancel-btn" onclick="cancelConfirm()">Отмена</button>
                <button class="confirm-btn confirm-btn-yes" onclick="acceptConfirm()">Да</button>
            </div>
        </div>
    `;

    // Добавляем стили если их еще нет
    if (!document.getElementById('confirm-styles')) {
        const styles = document.createElement('style');
        styles.id = 'confirm-styles';
        styles.textContent = `
            .confirm-modal {
                display: flex;
                position: fixed;
                z-index: 10000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease-in;
            }

            .confirm-content {
                background: white;
                border-radius: 12px;
                padding: 30px;
                max-width: 400px;
                width: 90%;
                text-align: center;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                animation: slideInScale 0.3s ease-out;
            }

            .confirm-header {
                margin-bottom: 20px;
            }

            .confirm-icon {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: #ff9800;
                color: white;
                font-size: 30px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 15px;
            }

            .confirm-header h3 {
                margin: 0;
                color: #333;
                font-size: 20px;
            }

            .confirm-message {
                color: #666;
                font-size: 16px;
                margin-bottom: 25px;
                line-height: 1.5;
            }

            .confirm-buttons {
                display: flex;
                gap: 15px;
                justify-content: center;
            }

            .confirm-btn {
                padding: 12px 25px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s ease;
                min-width: 100px;
            }

            .cancel-btn {
                background: #f5f5f5;
                color: #666;
            }

            .cancel-btn:hover {
                background: #e0e0e0;
            }

            .confirm-btn-yes {
                background: #ff9800;
                color: white;
            }

            .confirm-btn-yes:hover {
                background: #f57c00;
                transform: translateY(-1px);
            }

            @keyframes slideInScale {
                from {
                    opacity: 0;
                    transform: scale(0.8) translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }
            }

            @media (max-width: 480px) {
                .confirm-content {
                    padding: 20px;
                }
                
                .confirm-buttons {
                    flex-direction: column;
                }
                
                .confirm-btn {
                    width: 100%;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    // Функции для кнопок
    window.acceptConfirm = function() {
        document.body.removeChild(modal);
        if (onConfirm) onConfirm();
        delete window.acceptConfirm;
        delete window.cancelConfirm;
    };

    window.cancelConfirm = function() {
        document.body.removeChild(modal);
        if (onCancel) onCancel();
        delete window.acceptConfirm;
        delete window.cancelConfirm;
    };

    // Закрытие по клику вне модального окна
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            window.cancelConfirm();
        }
    });

    // Добавляем в DOM
    document.body.appendChild(modal);
}

async function removeFromBasket(detailId) {
        try {
            const response = await fetch(`/remove_from_basket/${detailId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();

                // Найдите строку таблицы, соответствующую удаляемой детали
                const row = document.querySelector(`tr[data-detail-ID_detail="${detailId}"]`);

                if (row) {
                    row.remove();
                    console.log(`Row with detail ID ${detailId} removed from table.`);
                }

                // Обновите итоговые суммы
                showNotification('I am kapibara');
                updateTotals();
            } else {
                const data = await response.json();
                showNotification(data.error || 'Произошла ошибка при удалении детали из корзины.');
            }
        } catch (error) {
            console.error('Ошибка при удалении детали из корзины:', error);
            showNotification('Произошла ошибка при удалении детали из корзины.');
        }
    }

    // Функция для обновления итоговых сумм
    function updateTotals() {
        let total = 0;
        let totalCard = 0;

        // Переберите все строки таблицы и пересчитайте суммы
        const rows = document.querySelectorAll('#cartItems tr');
        rows.forEach(row => {
            const price = parseFloat(row.querySelector('td:nth-child(5)').innerText) || 0; // Цена
            const priceCard = parseFloat(row.querySelector('td:nth-child(6)').innerText) || 0; // Цена по карте
            total += price;
            totalCard += priceCard;
        });

        document.getElementById('total').innerText = `Итого: ${total} руб.`;
        document.getElementById('totalCard').innerText = `Итого по карте: ${totalCard} руб.`;
    }

    // Обработчик события blur для ячеек таблицы
    document.getElementById('cartItems').addEventListener('blur', function(e) {
        if (e.target.tagName === 'TD' && e.target.innerHTML.trim() === '') {
            const row = e.target.parentNode; // Получаем родительскую строку
            row.remove(); // Удаляем строку, если ячейка пустая
            updateTotals(); // Обновляем итоговые суммы
        }
    }, true);


async function fetchDetail() {
    const partNumber = document.getElementById('partNumber').value;

    // Проверка, что номер детали является числом и больше или равен 0
    if (!partNumber || partNumber < 0) {
        showNotification('Пожалуйста, введите номер детали, который должен быть >= 0.');
        return;
    }

    try {
        const response = await fetch(`/get_detail/${partNumber}`);
        const data = await response.json();

        if (response.ok) {
            // Заполнение таблицы данными
            document.getElementById('detailId').innerText = data.id;
            document.getElementById('detailIDDetail').innerText = data.ID_detail;
            document.getElementById('detailOriginalNumber').innerText = data.orig_number;
            document.getElementById('detailBrand').innerText = data.brand;
            document.getElementById('detailModelAndYear').innerText = data.model_and_year;
            document.getElementById('detailName').innerText = data.name;
            document.getElementById('detailPrice').innerText = data.price;
            document.getElementById('detailPriceWDiscount').innerText = data.price_w_discount;
            document.getElementById('detailCondition').innerText = data.condition;
            document.getElementById('detailColor').innerText = data.color;
            document.getElementById('detailComment').innerText = data.comment;

            // Показать таблицу
            document.getElementById('detailTable').style.display = 'table';

            // Добавляем кнопку для добавления в корзину, если товар не в корзине
            const actionCell = document.getElementById('actionCell');
            actionCell.innerHTML = ''; // Очищаем предыдущие действия

            // Проверяем, находится ли деталь в корзине
            if (!data.detail_in_basket) {
                actionCell.innerHTML = `<button class="button" onclick="addToCart('${data.ID_detail}')">Добавить в корзину</button>`;
            } else {
                actionCell.innerHTML = `<span>Деталь уже в корзине</span>`;
            }
        } else {
            showNotification(data.error);
            document.getElementById('detailTable').style.display = 'none';
        }
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
        showNotification('Произошла ошибка при получении данных.');
    }
}

// Функция для добавления детали в корзину
async function addToCart(detailId) {
    try {
        const response = await fetch(`/add_to_basket/${detailId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            showNotification(data.success);
            // Здесь можно обновить интерфейс или выполнить другие действия
        } else {
            const data = await response.json();
            showNotification(data.error || 'Произошла ошибка при добавлении детали в корзину.');
        }
    } catch (error) {
        console.error('Ошибка при добавлении детали в корзину:', error);
        showNotification('Произошла ошибка при добавлении детали в корзину.');
    }
}