async function removeFromBasket(detailId) {
    alert("meow")
    try {
        const response = await fetch(`/remove_from_basket/${detailId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Выводим состояние response в консоль
        alert('Response:', response.ok);

        if (response.ok) {
            alert("meow meow")
            const data = await response.json();
            alert(data.success);

            // Найдите строку таблицы, соответствующую удаляемой детали
            const row = document.querySelector(`tr[data-detail-id="${detailId}"]`);
            console.log('Row found:', row); // Выводим состояние row в консоль

            if (row) {
                row.remove(); // Удалите строку из таблицы
                alert(`Row with detail ID ${detailId} removed from table.`); // Исправлено на обратные кавычки
                console.log(`Row with detail ID ${detailId} removed from table.`);
            }

            // Обновите итоговые суммы
            updateTotals();
        } else {
            const data = await response.json();
            alert(data.error || 'Произошла ошибка при удалении детали из корзины.');
        }
    } catch (error) {
        console.error('Ошибка при удалении детали из корзины:', error);
        alert('Произошла ошибка при удалении детали из корзины.');
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