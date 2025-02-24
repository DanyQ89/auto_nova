async function fetchDetail() {
    const partNumber = document.getElementById('partNumber').value;

    // Проверка, что номер детали является числом и больше или равен 0
    if (!partNumber || partNumber < 0) {
        alert('Пожалуйста, введите номер детали, который должен быть >= 0.');
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
            alert(data.error);
            document.getElementById('detailTable').style.display = 'none';
        }
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
        alert('Произошла ошибка при получении данных.');
    }
}

// Функция для добавления детали в корзину
async function addToCart(detailId) {
    console.log("Something")
    try {
        const response = await fetch(`/add_to_basket/${detailId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.success);
            // Здесь можно обновить интерфейс или выполнить другие действия
        } else {
            const data = await response.json();
            alert(data.error || 'Произошла ошибка при добавлении детали в корзину.');
        }
    } catch (error) {
        console.error('Ошибка при добавлении детали в корзину:', error);
        alert('Произошла ошибка при добавлении детали в корзину.');
    }
}