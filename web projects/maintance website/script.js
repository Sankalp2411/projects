document.addEventListener('DOMContentLoaded', () => {
    // === Theme Toggle ===
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    const storedTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', storedTheme);

    themeToggleBtn.addEventListener('click', () => {
        const current = htmlElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        htmlElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    });

    // === Mobile Menu ===
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // === Scroll Progress Bar ===
    const scrollProgress = document.getElementById('scroll-progress');
    const backToTop = document.getElementById('back-to-top');

    window.addEventListener('scroll', () => {
        const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const progress = (scrollTop / scrollHeight) * 100;
        scrollProgress.style.width = progress + '%';

        // Back to top visibility
        if (backToTop) {
            if (scrollTop > 400) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        }
    });

    // Back to top click
    if (backToTop) {
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // === Navbar Scroll ===
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // === Intersection Observer for Scroll Animations ===
    const animateOnScrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { root: null, rootMargin: '0px', threshold: 0.15 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => animateOnScrollObserver.observe(el));

    // === Counter Animation ===
    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000;
                const startTime = performance.now();

                function updateCounter(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    counter.textContent = Math.round(eased * target);
                    if (progress < 1) {
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                }
                requestAnimationFrame(updateCounter);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-number').forEach(c => counterObserver.observe(c));

    // === Typing Animation ===
    const typedElement = document.getElementById('hero-typed');
    if (typedElement) {
        const phrases = [
            'Clean Energy · Tech Sustainability · Innovation',
            'Building Tomorrow\'s Energy Infrastructure.',
            'Powering Lumiris · Defending with Rakshavahan.',
            'Engineering a Sustainable Future.'
        ];
        let phraseIndex = 0, charIndex = 0, isDeleting = false, typeSpeed = 60;

        function typeEffect() {
            const currentPhrase = phrases[phraseIndex];
            if (isDeleting) {
                typedElement.textContent = currentPhrase.substring(0, charIndex - 1);
                charIndex--;
                typeSpeed = 25;
            } else {
                typedElement.textContent = currentPhrase.substring(0, charIndex + 1);
                charIndex++;
                typeSpeed = 55;
            }
            if (!isDeleting && charIndex === currentPhrase.length) {
                typeSpeed = 2500;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                phraseIndex = (phraseIndex + 1) % phrases.length;
                typeSpeed = 400;
            }
            setTimeout(typeEffect, typeSpeed);
        }
        setTimeout(typeEffect, 1000);
    }

    // === Particle System ===
    const canvas = document.getElementById('particle-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];
        let animationId;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        class Particle {
            constructor() { this.reset(); }
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = (Math.random() - 0.5) * 0.3;
                this.speedY = (Math.random() - 0.5) * 0.3;
                this.opacity = Math.random() * 0.5 + 0.1;
                this.pulseSpeed = Math.random() * 0.02 + 0.005;
                this.pulseOffset = Math.random() * Math.PI * 2;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                this.currentOpacity = this.opacity + Math.sin(Date.now() * this.pulseSpeed + this.pulseOffset) * 0.15;
                if (this.x < 0) this.x = canvas.width;
                if (this.x > canvas.width) this.x = 0;
                if (this.y < 0) this.y = canvas.height;
                if (this.y > canvas.height) this.y = 0;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(74, 222, 128, ${this.currentOpacity})`;
                ctx.fill();
            }
        }

        const particleCount = Math.min(60, Math.floor(window.innerWidth * window.innerHeight / 20000));
        for (let i = 0; i < particleCount; i++) particles.push(new Particle());

        function drawConnections() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    if (distance < 120) {
                        const opacity = (1 - distance / 120) * 0.12;
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(74, 222, 128, ${opacity})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            drawConnections();
            animationId = requestAnimationFrame(animate);
        }
        animate();

        document.addEventListener('visibilitychange', () => {
            if (document.hidden) cancelAnimationFrame(animationId);
            else animate();
        });
    }

    // === Active Nav Highlight ===
    const sections = document.querySelectorAll('section[id]');
    const navLinkElements = document.querySelectorAll('.nav-links a');

    function updateActiveLink() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 120;
            if (window.scrollY >= sectionTop) current = section.getAttribute('id');
        });
        navLinkElements.forEach(link => {
            link.classList.remove('active-link');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active-link');
            }
        });
    }
    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();

    // === Project Modal Logic ===
    const modalOverlays = document.querySelectorAll('.project-modal-overlay');
    const viewDetailsBtns = document.querySelectorAll('.project-view-btn');
    const projectCards = document.querySelectorAll('.project-showcase-card');

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) { modal.classList.add('active'); document.body.style.overflow = 'hidden'; }
    }
    function closeModal(overlay) { overlay.classList.remove('active'); document.body.style.overflow = ''; }
    function closeAllModals() { modalOverlays.forEach(overlay => closeModal(overlay)); }

    viewDetailsBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            openModal(btn.getAttribute('data-modal'));
        });
    });

    projectCards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.closest('.project-download-btn')) return;
            if (e.target.closest('.project-view-btn')) return;
            openModal('modal-' + card.getAttribute('data-project'));
        });
    });

    document.querySelectorAll('.modal-close-btn').forEach(btn => {
        btn.addEventListener('click', (e) => { e.stopPropagation(); closeModal(btn.closest('.project-modal-overlay')); });
    });
    document.querySelectorAll('.modal-close-action').forEach(btn => {
        btn.addEventListener('click', (e) => { e.stopPropagation(); closeModal(btn.closest('.project-modal-overlay')); });
    });
    modalOverlays.forEach(overlay => {
        overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(overlay); });
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeAllModals(); });
    document.querySelectorAll('.project-download-btn').forEach(btn => {
        btn.addEventListener('click', (e) => e.stopPropagation());
    });

    // === Newsletter Form ===
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('newsletter-email').value;
            if (email) {
                const btn = document.getElementById('newsletter-submit');
                btn.innerHTML = '<i class="fas fa-check"></i> Subscribed!';
                btn.style.pointerEvents = 'none';
                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-arrow-right"></i> Subscribe';
                    btn.style.pointerEvents = '';
                    document.getElementById('newsletter-email').value = '';
                }, 3000);
            }
        });
    }
});

// === Contact Form Handler ===
function handleContactForm(e) {
    e.preventDefault();
    const form = document.getElementById('contact-form');
    const successEl = document.getElementById('contact-success');
    const submitBtn = document.getElementById('contact-submit');

    const name    = document.getElementById('contact-name').value.trim();
    const email   = document.getElementById('contact-email-field').value.trim();
    const subject = document.getElementById('contact-subject').value.trim();
    const message = document.getElementById('contact-message').value.trim();

    // Animate button
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Sending...</span>';
    submitBtn.disabled = true;

    setTimeout(() => {
        // Open mailto as fallback to send the message
        const mailtoLink = `mailto:business@reearthtech.in?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\n${message}`)}`;
        window.location.href = mailtoLink;

        // Show success
        successEl.classList.add('show');
        form.reset();

        // Reset button
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i><span>Send Message</span>';
        submitBtn.disabled = false;

        // Hide success after 5s
        setTimeout(() => successEl.classList.remove('show'), 5000);
    }, 900);

    return false;
}
