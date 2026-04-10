// ================================
// Dynamic Sky Background Based on Time
// ================================

function updateSkyGradient() {
    const hour = new Date().getHours();
    const body = document.body;

    // Remove all time classes
    body.classList.remove('morning', 'midday', 'evening', 'night');

    // Add appropriate class based on time
    if (hour >= 5 && hour < 8) {
        body.classList.add('morning');
    } else if (hour >= 8 && hour < 17) {
        body.classList.add('midday');
    } else if (hour >= 17 && hour < 20) {
        body.classList.add('evening');
    } else {
        body.classList.add('night');
    }
}

// ================================
// Intersection Observer for Animations
// ================================

function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards and features
    const animatedElements = document.querySelectorAll('.glass-card, .feature, .step');
    animatedElements.forEach(el => observer.observe(el));
}

// ================================
// Interactive Card Effects
// ================================

function setupInteractiveCards() {
    const cards = document.querySelectorAll('.interactive-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // Add slight tilt effect based on mouse position
            card.style.transition = 'transform 0.1s ease';
        });

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px) scale(1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transition = 'transform 0.3s ease';
            card.style.transform = '';
        });
    });
}

// ================================
// Smooth Scrolling for Navigation
// ================================

function setupSmoothScroll() {
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
}

// ================================
// Parallax Effect for Floating Sun
// ================================

function setupParallax() {
    const floatingSun = document.getElementById('floatingSun');

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.5;

        floatingSun.style.transform = `translateY(${rate}px)`;
    });
}

// ================================
// Progress Bar Animation
// ================================

function animateProgressBar() {
    const progressFill = document.getElementById('progressFill');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                progressFill.style.animation = 'fillProgress 3s ease-in-out infinite';
            }
        });
    }, { threshold: 0.5 });

    if (progressFill) {
        observer.observe(progressFill);
    }
}

// ================================
// Random Floating Particles
// ================================

function createFloatingParticles() {
    const particleCount = 20;
    const container = document.body;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';

        const size = Math.random() * 4 + 2;
        const left = Math.random() * 100;
        const animationDuration = Math.random() * 10 + 10;
        const delay = Math.random() * 5;

        particle.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            background: radial-gradient(circle, var(--yellow), transparent);
            border-radius: 50%;
            left: ${left}%;
            top: -10px;
            opacity: 0.3;
            pointer-events: none;
            z-index: -1;
            animation: floatDown ${animationDuration}s linear ${delay}s infinite;
        `;

        container.appendChild(particle);
    }

    // Add floating animation CSS
    if (!document.getElementById('particle-styles')) {
        const style = document.createElement('style');
        style.id = 'particle-styles';
        style.textContent = `
            @keyframes floatDown {
                0% {
                    transform: translateY(-10px) translateX(0);
                    opacity: 0;
                }
                10% {
                    opacity: 0.3;
                }
                90% {
                    opacity: 0.3;
                }
                100% {
                    transform: translateY(100vh) translateX(20px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// ================================
// Easter Egg: Click the floating sun
// ================================

function setupSunEasterEgg() {
    const floatingSun = document.getElementById('floatingSun');
    let clickCount = 0;

    floatingSun.addEventListener('click', () => {
        clickCount++;

        // Add bounce animation
        floatingSun.style.animation = 'none';
        setTimeout(() => {
            floatingSun.style.animation = 'float 6s ease-in-out infinite';
        }, 10);

        // Add temporary scale effect
        const sunCore = floatingSun.querySelector('.sun-core');
        sunCore.style.transform = 'translate(-50%, -50%) scale(1.3)';
        setTimeout(() => {
            sunCore.style.transform = 'translate(-50%, -50%) scale(1)';
        }, 300);

        // After 5 clicks, show a message
        if (clickCount === 5) {
            alert('☀️ You found the sun! Now go find the real one outside! ☀️');
            clickCount = 0;
        }
    });

    // Make it look clickable on hover
    floatingSun.style.cursor = 'pointer';
}

// ================================
// Initialize Everything
// ================================

document.addEventListener('DOMContentLoaded', () => {
    updateSkyGradient();
    setupScrollAnimations();
    setupInteractiveCards();
    setupSmoothScroll();
    setupParallax();
    animateProgressBar();
    createFloatingParticles();
    setupSunEasterEgg();

    // Update sky gradient every minute
    setInterval(updateSkyGradient, 60000);
});

// ================================
// Handle reduced motion preferences
// ================================

if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Disable animations for users who prefer reduced motion
    document.querySelectorAll('*').forEach(el => {
        el.style.animation = 'none';
        el.style.transition = 'none';
    });
}
