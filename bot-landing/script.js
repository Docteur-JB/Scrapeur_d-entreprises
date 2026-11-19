// Navigation mobile
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    const navButtons = document.querySelector('.nav-buttons');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            const isExpanded = navMenu.style.display === 'flex';

            if (isExpanded) {
                navMenu.style.display = 'none';
                navButtons.style.display = 'none';
                mobileMenuBtn.classList.remove('active');
            } else {
                navMenu.style.display = 'flex';
                navButtons.style.display = 'flex';
                mobileMenuBtn.classList.add('active');

                // Style pour mobile
                navMenu.style.flexDirection = 'column';
                navMenu.style.position = 'absolute';
                navMenu.style.top = '100%';
                navMenu.style.left = '0';
                navMenu.style.right = '0';
                navMenu.style.background = 'rgba(255, 255, 255, 0.98)';
                navMenu.style.padding = '1rem';
                navMenu.style.gap = '1rem';

                navButtons.style.flexDirection = 'column';
                navButtons.style.position = 'absolute';
                navButtons.style.top = 'calc(100% + 200px)';
                navButtons.style.left = '0';
                navButtons.style.right = '0';
                navButtons.style.background = 'rgba(255, 255, 255, 0.98)';
                navButtons.style.padding = '1rem';
                navButtons.style.gap = '0.5rem';
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .step, .stat').forEach(el => {
        observer.observe(el);
    });

    // Simple counter animation for stats
    const stats = document.querySelectorAll('.stat-number');
    if (stats.length > 0) {
        stats.forEach(stat => {
            const target = parseInt(stat.textContent);
            let current = 0;
            const increment = target / 50;

            const updateStat = () => {
                if (current < target) {
                    current += increment;
                    stat.textContent = Math.round(current).toLocaleString();
                    requestAnimationFrame(updateStat);
                } else {
                    stat.textContent = target.toLocaleString();
                }
            };

            // Start animation when stat is in view
            const statObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        updateStat();
                        statObserver.unobserve(entry.target);
                    }
                });
            });

            statObserver.observe(stat.parentElement);
        });
    }
});