// 新闻聚合器的主JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 启用Bootstrap工具提示
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 处理收藏按钮点击
    setupFavoriteButtons();

    // 5秒后自动关闭提示
    setupAutoDismissAlerts();

    // 设置搜索表单验证
    setupSearchValidation();

    // 为卡片添加淡入动画
    animateCards();
});

function setupFavoriteButtons() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');

    favoriteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const articleId = this.getAttribute('data-article-id');
            const button = this;

            fetch('/favorite/' + articleId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    button.classList.add('active');
                    button.innerHTML = '<i class="fas fa-heart"></i>';
                    showToast('Article added to favorites');
                } else {
                    button.classList.remove('active');
                    button.innerHTML = '<i class="far fa-heart"></i>';
                    showToast('Article removed from favorites');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error updating favorite status', 'danger');
            });
        });
    });
}

function setupAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');

    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

function setupSearchValidation() {
    const searchForm = document.querySelector('form[action*="search"]');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.classList.add('is-invalid');

                // 如果不存在则创建错误消息
                if (!document.getElementById('search-error')) {
                    const errorDiv = document.createElement('div');
                    errorDiv.id = 'search-error';
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = 'Please enter a search term';
                    searchInput.parentNode.appendChild(errorDiv);
                }
            } else {
                searchInput.classList.remove('is-invalid');
            }
        });
    }
}

function animateCards() {
    const cards = document.querySelectorAll('.article-card, .source-card');

    cards.forEach(function(card, index) {
        card.classList.add('fade-in');
        card.style.animationDelay = (index * 0.05) + 's';
    });
}

function showToast(message, type = 'success') {
    // 如果不存在则创建toast容器
    let toastContainer = document.querySelector('.toast-container');

    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // 创建toast元素
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    // 创建toast内容
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    // 将toast添加到容器
    toastContainer.appendChild(toastEl);

    // 初始化并显示toast
    const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 3000
    });

    toast.show();

    // toast隐藏后移除元素
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}
