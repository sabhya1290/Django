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

document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const pdfId = this.getAttribute('data-pdf-id');
      
      fetch(`/resources/bookmark/${pdfId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
      .then(response => {
        const contentType = response.headers.get('content-type');
        if (response.status === 403 || (contentType && contentType.includes('text/html'))) {
          document.getElementById('loginRequiredModal').classList.remove('hidden');
          throw new Error('Not authenticated');
        }
        return response.json();
      })
      .then(data => {
        if (data.error === 'Not authenticated') {
          document.getElementById('loginRequiredModal').classList.remove('hidden');
          return;
        }
        const icon = document.getElementById(`bookmark-icon-${pdfId}`);
        icon.textContent = data.bookmarked ? '★' : '☆';
      })
      .catch(error => {
        console.error('AJAX error:', error);
      });
  });
});


// Handle closing the login required modal
const closeLoginModalBtn = document.getElementById('closeLoginModal');
const loginRequiredModal = document.getElementById('loginRequiredModal');
if (closeLoginModalBtn && loginRequiredModal) {
  closeLoginModalBtn.addEventListener('click', function() {
    loginRequiredModal.classList.add('hidden');
  });
}

// PDF Preview Modal Logic

document.addEventListener('DOMContentLoaded', function() {
  // PDF Preview
  const pdfModal = document.getElementById('pdfPreviewModal');
  const pdfFrame = document.getElementById('pdfFrame');
  const closePdfModal = document.getElementById('closePdfModal');

  // Delegate event for dynamically loaded buttons
  document.body.addEventListener('click', function(e) {
    if (e.target.classList.contains('pdf-preview-btn')) {
      e.preventDefault();
      const pdfUrl = e.target.getAttribute('data-pdf-url');
      pdfFrame.src = pdfUrl;
      pdfModal.classList.remove('hidden');
      pdfModal.classList.add('flex');
    }
  });

  if (closePdfModal && pdfModal && pdfFrame) {
    closePdfModal.addEventListener('click', function() {
      pdfModal.classList.add('hidden');
      pdfModal.classList.remove('flex');
      pdfFrame.src = '';
    });
    // Optional: close modal when clicking outside content
    pdfModal.addEventListener('click', function(e) {
      if (e.target === pdfModal) {
        pdfModal.classList.add('hidden');
        pdfModal.classList.remove('flex');
        pdfFrame.src = '';
      }
    });
  }
});

// Helper to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}