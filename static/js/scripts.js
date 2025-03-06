
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
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const photoData = await response.text(); // Получаем данные изображения
        openPhotoModal(photoData); // Открываем модальное окно с изображением
    } catch (error) {
        console.error('Ошибка при получении фото:', error);
    }
}

function openPhotoModal(photo) {
    const modal = document.getElementById('photoModal');
    const modalImage = document.getElementById('modalImage');
    modalImage.src = `data:image/jpeg;base64,${photo}`; // Устанавливаем источник изображения
    modal.style.display = "block"; // Показываем модальное окно
}

function closePhotoModal() {
    const modal = document.getElementById('photoModal');
    modal.style.display = "none"; // Скрываем модальное окно
}

function uploadFile(detailId) {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('detail_id', detailId); // Include the detail ID

        fetch('/add_photo', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/admin'; // Redirect to admin page
            } else {
                alert('Обновление фото не удалось');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при обновлении фото');
        });
    }
}
