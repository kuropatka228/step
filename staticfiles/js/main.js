document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('nav ul');

    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('show');
        });
    }

    // Cart quantity controls
    document.querySelectorAll('.cart-quantity-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.cart-quantity-input');
            let value = parseInt(input.value);

            if (this.classList.contains('minus') && value > 1) {
                value--;
            } else if (this.classList.contains('plus')) {
                value++;
            }

            input.value = value;
        });
    });

    // Product image zoom
    document.querySelectorAll('.product-thumbnail').forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const mainImage = document.querySelector('.main-image img');
            mainImage.src = this.src;
        });
    });

    // Reviews slider
    if (document.querySelector('.reviews-slider')) {
        let currentReview = 0;
        const reviews = document.querySelectorAll('.review');
        const totalReviews = reviews.length;

        function showReview(index) {
            reviews.forEach(review => review.classList.remove('active'));
            reviews[index].classList.add('active');
        }

        // Auto-rotate reviews every 5 seconds
        setInterval(() => {
            currentReview = (currentReview + 1) % totalReviews;
            showReview(currentReview);
        }, 5000);

        showReview(0);
    }

    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let valid = true;
            const inputs = this.querySelectorAll('input[required], select[required], textarea[required]');

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('error');
                    valid = false;
                } else {
                    input.classList.remove('error');
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Для плавного появления форм отзывов
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок "Оставить отзыв"
    document.querySelectorAll('[onclick*="review-form"]').forEach(btn => {
        btn.onclick = function() {
            const formId = this.getAttribute('onclick').match(/'(.*?)'/)[1];
            document.getElementById(formId).style.display = 'block';
            this.style.display = 'none';

            // Плавное появление
            document.getElementById(formId).style.opacity = 0;
            let opacity = 0;
            const timer = setInterval(() => {
                if (opacity >= 1) clearInterval(timer);
                document.getElementById(formId).style.opacity = opacity;
                opacity += 0.1;
            }, 50);
        };
    });
});