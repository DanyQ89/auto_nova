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
            const row = document.querySelector(`tr[data-detail-id="${detailId}"]`);

            if (row) {
                row.remove(); // Удалите строку из таблицы
            }

            // Обновите итоговые суммы
            updateTotals();

            // Показать всплывающее уведомление об успехе
            alert('Деталь удалена из корзины.');
        } else {
            const data = await response.json();

            // Показать всплывающее уведомление об ошибке
            showNotification(data.message || 'Не удалось удалить деталь из корзины.', true);
        }
    } catch (error) {
        console.error('Ошибка при удалении детали из корзины:', error);

        // Показать всплывающее уведомление об ошибке
        showNotification('Произошла ошибка при удалении детали из корзины.', true);
    }
}

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