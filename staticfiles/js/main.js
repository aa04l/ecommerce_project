/**
 * Main JavaScript file for E-commerce Project
 * Handles common functionality across the site
 */

// Global variables
let currentUser = null;
let notificationCount = 0;

// DOM Ready function
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    setupEventListeners();
    initializeNotifications();
    setupProductModals();
    setupSwiper();
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }

    // Close modals when clicking outside
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show');
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

/**
 * Initialize notification system
 */
function initializeNotifications() {
    const notificationBadge = document.getElementById('notification-badge');
    if (notificationBadge) {
        notificationCount = parseInt(notificationBadge.textContent) || 0;
    }

    // Check for new notifications every 30 seconds
    if (document.body.classList.contains('authenticated')) {
        setInterval(checkNewNotifications, 30000);
    }
}

/**
 * Check for new notifications
 */
function checkNewNotifications() {
    fetch('/products/check-new-notifications/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.new_notifications && data.new_notifications.length > 0) {
            updateNotificationBadge(data.unread_count);
            showNotificationToast(data.new_notifications[0]);
        }
    })
    .catch(error => {
        console.error('Error checking notifications:', error);
    });
}

/**
 * Update notification badge
 */
function updateNotificationBadge(count) {
    let badge = document.getElementById('notification-badge');
    if (count > 0) {
        if (!badge) {
            badge = document.createElement('span');
            badge.className = 'notification-badge';
            badge.id = 'notification-badge';
            const notificationLink = document.querySelector('a[href*="notifications"]');
            if (notificationLink) {
                notificationLink.appendChild(badge);
            }
        }
        badge.textContent = count;
        notificationCount = count;
    } else if (badge) {
        badge.remove();
        notificationCount = 0;
    }
}

/**
 * Show notification toast
 */
function showNotificationToast(notification) {
    const toast = document.createElement('div');
    toast.className = 'notification-toast';
    
    const icon = getNotificationIcon(notification.type);
    
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 16px;">${icon}</span>
            <strong style="font-size: 14px;">${notification.title}</strong>
        </div>
        <p style="margin: 0; font-size: 12px; color: #666;">${notification.message}</p>
        <button onclick="this.parentElement.remove()" style="position: absolute; top: 8px; right: 8px; background: none; border: none; font-size: 16px; cursor: pointer;">×</button>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Hide toast after 5 seconds
    setTimeout(() => {
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

/**
 * Get notification icon based on type
 */
function getNotificationIcon(type) {
    const icons = {
        'order_status': '📦',
        'product_restock': '🔄',
        'promotion': '🎉',
        'system': '🔔'
    };
    return icons[type] || '🔔';
}

/**
 * Setup product modals
 */
function setupProductModals() {
    const productCards = document.querySelectorAll('.product-card');
    const modal = document.getElementById('product-modal');
    
    if (!modal || productCards.length === 0) return;

    const modalImage = document.getElementById('modal-image');
    const modalName = document.getElementById('modal-name');
    const modalPrice = document.getElementById('modal-price');
    const modalDescription = document.getElementById('modal-description');
    const modalCategory = document.getElementById('modal-category');
    const closeModalBtn = document.querySelector('.close-btn');

    let hoverTimeout;
    const HOVER_DELAY = 500;
    let modalVisible = false;

    productCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            hoverTimeout = setTimeout(() => {
                // Fill modal data
                modalImage.src = card.getAttribute('data-image');
                modalName.textContent = card.getAttribute('data-name');
                modalPrice.textContent = `$${card.getAttribute('data-price')}`;
                modalDescription.textContent = card.getAttribute('data-content');
                modalCategory.textContent = `Category: ${card.getAttribute('data-category')}`;

                modal.classList.add('show');
                modalVisible = true;
            }, HOVER_DELAY);
        });

        card.addEventListener('mouseleave', () => {
            clearTimeout(hoverTimeout);
        });

        card.addEventListener('click', () => {
            const productId = card.getAttribute('data-id');
            window.location.href = `/products/product-details/${productId}/`;
        });
    });

    // Close modal events
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            hideModal();
        });
    }

    modal.addEventListener('mouseleave', () => {
        hideModal();
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal();
        }
    });

    function hideModal() {
        modal.classList.remove('show');
        modalVisible = false;
    }
}

/**
 * Setup Swiper for banners
 */
function setupSwiper() {
    const swiperContainer = document.querySelector('.swiper-container');
    if (!swiperContainer) return;

    // Check if Swiper is loaded
    if (typeof Swiper === 'undefined') {
        console.warn('Swiper not loaded');
        return;
    }

    const swiper = new Swiper('.swiper-container', {
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true,
        },
    });
}

/**
 * Close all modals
 */
function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.classList.remove('show');
    });
}

/**
 * Show loading spinner
 */
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

/**
 * Show success message
 */
function showSuccess(message) {
    showMessage(message, 'success');
}

/**
 * Show error message
 */
function showError(message) {
    showMessage(message, 'error');
}

/**
 * Show message with type
 */
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-toast ${type}`;
    messageDiv.textContent = message;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => messageDiv.classList.add('show'), 100);
    
    setTimeout(() => {
        messageDiv.classList.add('hide');
        setTimeout(() => messageDiv.remove(), 300);
    }, 3000);
}

/**
 * Format price
 */
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for use in other files
window.AppUtils = {
    showLoading,
    hideLoading,
    showSuccess,
    showError,
    showMessage,
    formatPrice,
    debounce,
    throttle,
    closeAllModals
}; 