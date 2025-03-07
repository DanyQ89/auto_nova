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
    const cpkInput = document.getElementById('CpK');
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
        cpkInput.value = detail.CpK || '';
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
        cpkInput.value = '';
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

// Функция для переключения меню


async function fetchPhoto(detailId) {
    try {
        const response = await fetch(`/photo/${detailId}`); // Запрос на сервер для получения фото
        alert(`${response.ok}`)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const photoData = await response.json(); // Получаем данные изображения как массив
        openPhotoModal(photoData); // Открываем модальное окно с изображениями
    } catch (error) {
        console.error('Ошибка при получении фото:', error);
    }
}

function openPhotoModal(photoData) {
    const modal = document.getElementById('photoModal'); // Получаем элемент модального окна
    const photoContainer = modal.querySelector('.photo-container'); // Получаем контейнер для фотографий

    // Очищаем контейнер перед добавлением новых изображений
    photoContainer.innerHTML = '';

    // Добавляем каждую фотографию в контейнер
    photoData.forEach((photo, index) => {
        const imgContainer = document.createElement('div'); // Создаем контейнер для изображения и кнопок

        const img = document.createElement('img'); // Создаем элемент изображения
        img.src = `data:image/jpeg;base64,${photo}`; // Устанавливаем источник изображения
        img.alt = 'Photo'; // Устанавливаем альтернативный текст
        img.classList.add('modal-photo'); // Добавляем класс для стилизации

        // Создаем кнопку "Редактировать"
        const editButton = document.createElement('button');
        editButton.textContent = 'Редактировать';
        editButton.classList.add('edit-button');
        editButton.onclick = () => editPhoto(index); // Привязываем обработчик события

        // Создаем кнопку "Удалить"
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.classList.add('delete-button');
        deleteButton.onclick = () => deletePhoto(index); // Привязываем обработчик события

        // Добавляем изображение и кнопки в контейнер
        imgContainer.appendChild(img);
        imgContainer.appendChild(editButton);
        imgContainer.appendChild(deleteButton);
        photoContainer.appendChild(imgContainer); // Добавляем контейнер изображения в основной контейнер
    });

    // Показываем модальное окно
    modal.style.display = 'block';
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
            alert(result.message); // Успешное обновление
            // Обновите интерфейс, если нужно
        } else {
            alert(`Ошибка: ${result.message}`); // Ошибка
        }
    } catch (error) {
        console.error('Ошибка при редактировании фото:', error);
        alert('Произошла ошибка при редактировании фото');
    }
}

async function deletePhoto(photoId) {
    try {
        const response = await fetch(`/delete_photo/${photoId}`, {
            method: 'DELETE',
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message); // Успешное удаление
            // Обновите интерфейс, если нужно
        } else {
            alert(`Ошибка: ${result.message}`); // Ошибка
        }
    } catch (error) {
        console.error('Ошибка при удалении фото:', error);
        alert('Произошла ошибка при удалении фото');
    }
}

function closePhotoModal() {
    const modal = document.getElementById('photoModal');
    modal.style.display = "none"; // Скрываем модальное окно
}

function uploadPhoto(detailId) {
    const fileInput = document.getElementById(`file-input-${detailId}`);
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('detail_id', detailId); // Добавляем ID детали

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
            // Здесь можно обновить интерфейс или показать сообщение об успехе
            alert(data.message); // Показываем сообщение об успехе
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка при загрузке фото: ' + error.message);
        });
    } else {
        alert('Пожалуйста, выберите файл для загрузки.');
    }
}