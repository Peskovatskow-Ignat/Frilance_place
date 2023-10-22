// Ваш JavaScript код может выглядеть примерно так:
document.addEventListener('DOMContentLoaded', function () {
    const fullscreenNotification = document.getElementById('fullscreen-notification');

    // Показать уведомление
    function showFullscreenNotification() {
        fullscreenNotification.style.display = 'flex';
    }

    // Скрыть уведомление
    function hideFullscreenNotification() {
        fullscreenNotification.style.display = 'none';
    }

    // Вызывайте функцию showFullscreenNotification() и hideFullscreenNotification()
    // в соответствующих местах вашего кода, например, при успешной регистрации и при отображении сообщения flash.
});
