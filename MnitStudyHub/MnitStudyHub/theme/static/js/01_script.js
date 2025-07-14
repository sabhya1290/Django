document.addEventListener('DOMContentLoaded', function() {
    const logoutForm = document.getElementById('logout-form');
    const logoutModal = document.getElementById('logoutModal');
    const cancelLogout = document.getElementById('cancelLogout');
    const confirmLogout = document.getElementById('confirmLogout');

    if (logoutForm && logoutModal && cancelLogout && confirmLogout) {
        logoutForm.addEventListener('submit', function(event) {
            event.preventDefault();
            logoutModal.classList.remove('hidden');
        });

        cancelLogout.addEventListener('click', function() {
            logoutModal.classList.add('hidden');
        });

        confirmLogout.addEventListener('click', function() {
            logoutModal.classList.add('hidden');
            logoutForm.submit();
        });
    }
});