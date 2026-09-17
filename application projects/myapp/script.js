/* =============================================
   SANKALP JADHAV - 3D PORTFOLIO ENGINE
   Three.js + GSAP-style Animations
   ============================================= */

// ─── Utility Functions ───
const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (val, min, max) => Math.min(Math.max(val, min), max);

// ─── Mouse Tracking ───
const mouse = { x: 0, y: 0, smoothX: 0, smoothY: 0 };

document.addEventListener('mousemove', (e) => {
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

    // Cursor glow
    const glow = document.getElementById('cursor-glow');
    if (glow) {
        glow.style.left = e.clientX + 'px';
        glow.style.top = e.clientY + 'px';
    }
});

// ─── Three.js 3D Scene ───
class ParticleUniverse {
    constructor() {
        this.canvas = document.getElementById('three-canvas');
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: true
        });
        this.clock = new THREE.Clock();
        this.particles = null;
        this.geometricShapes = [];
        this.floatingOrbs = [];

        this.init();
    }

    init() {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.setClearColor(0x000000, 0);
        this.camera.position.z = 5;

        this.createParticleField();
        this.createGeometricShapes();
        this.createFloatingOrbs();
        this.createAmbientLight();

        window.addEventListener('resize', () => this.onResize());
        this.animate();
    }

    createParticleField() {
        const count = 2000;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(count * 3);
        const sizes = new Float32Array(count);
        const colors = new Float32Array(count * 3);

        const palette = [
            new THREE.Color(0x6366f1), // Indigo
            new THREE.Color(0x8b5cf6), // Violet
            new THREE.Color(0xa78bfa), // Light Violet
            new THREE.Color(0xc084fc), // Purple
            new THREE.Color(0xe879f9), // Pink
        ];

        for (let i = 0; i < count; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 20;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
            sizes[i] = Math.random() * 3 + 0.5;

            const color = palette[Math.floor(Math.random() * palette.length)];
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.02,
            vertexColors: true,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending,
            depthWrite: false,
        });

        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);
    }

    createGeometricShapes() {
        const createShape = (geometry, position, color, scale = 1) => {
            const material = new THREE.MeshPhongMaterial({
                color: color,
                transparent: true,
                opacity: 0.08,
                wireframe: true,
                side: THREE.DoubleSide,
            });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(...position);
            mesh.scale.setScalar(scale);
            mesh.userData = {
                rotSpeed: {
                    x: (Math.random() - 0.5) * 0.005,
                    y: (Math.random() - 0.5) * 0.005,
                    z: (Math.random() - 0.5) * 0.005,
                },
                floatSpeed: Math.random() * 0.5 + 0.3,
                floatAmp: Math.random() * 0.3 + 0.1,
                initialY: position[1],
            };
            this.scene.add(mesh);
            this.geometricShapes.push(mesh);
        };

        // Icosahedron
        createShape(
            new THREE.IcosahedronGeometry(1, 1),
            [-4, 2, -3],
            0x6366f1,
            0.8
        );

        // Torus
        createShape(
            new THREE.TorusGeometry(0.8, 0.3, 16, 32),
            [4, -1, -4],
            0x8b5cf6,
            0.7
        );

        // Octahedron
        createShape(
            new THREE.OctahedronGeometry(0.7, 0),
            [-3, -2, -2],
            0xc084fc,
            0.6
        );

        // Dodecahedron
        createShape(
            new THREE.DodecahedronGeometry(0.6, 0),
            [3, 3, -5],
            0xe879f9,
            0.5
        );

        // Torus Knot
        createShape(
            new THREE.TorusKnotGeometry(0.5, 0.15, 64, 8),
            [5, 1, -6],
            0xa78bfa,
            0.4
        );
    }

    createFloatingOrbs() {
        for (let i = 0; i < 5; i++) {
            const geometry = new THREE.SphereGeometry(0.1, 16, 16);
            const material = new THREE.MeshBasicMaterial({
                color: [0x6366f1, 0x8b5cf6, 0xa78bfa, 0xc084fc, 0xe879f9][i],
                transparent: true,
                opacity: 0.3,
            });
            const orb = new THREE.Mesh(geometry, material);
            orb.position.set(
                (Math.random() - 0.5) * 10,
                (Math.random() - 0.5) * 10,
                (Math.random() - 0.5) * 5 - 3
            );
            orb.userData = {
                speed: Math.random() * 0.3 + 0.2,
                radius: Math.random() * 2 + 1,
                offset: Math.random() * Math.PI * 2,
            };
            this.scene.add(orb);
            this.floatingOrbs.push(orb);
        }
    }

    createAmbientLight() {
        const ambientLight = new THREE.AmbientLight(0x6366f1, 0.3);
        this.scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0x8b5cf6, 0.5, 20);
        pointLight1.position.set(5, 5, 5);
        this.scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0xe879f9, 0.3, 20);
        pointLight2.position.set(-5, -3, 3);
        this.scene.add(pointLight2);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        const elapsed = this.clock.getElapsedTime();

        // Smooth mouse tracking
        mouse.smoothX = lerp(mouse.smoothX, mouse.x, 0.05);
        mouse.smoothY = lerp(mouse.smoothY, mouse.y, 0.05);

        // Rotate particle field
        if (this.particles) {
            this.particles.rotation.y = elapsed * 0.05 + mouse.smoothX * 0.3;
            this.particles.rotation.x = elapsed * 0.03 + mouse.smoothY * 0.2;
        }

        // Animate geometric shapes
        this.geometricShapes.forEach((shape) => {
            shape.rotation.x += shape.userData.rotSpeed.x;
            shape.rotation.y += shape.userData.rotSpeed.y;
            shape.rotation.z += shape.userData.rotSpeed.z;
            shape.position.y =
                shape.userData.initialY +
                Math.sin(elapsed * shape.userData.floatSpeed) * shape.userData.floatAmp;
        });

        // Animate floating orbs
        this.floatingOrbs.forEach((orb) => {
            const { speed, radius, offset } = orb.userData;
            orb.position.x += Math.sin(elapsed * speed + offset) * 0.005;
            orb.position.y += Math.cos(elapsed * speed * 0.7 + offset) * 0.005;
        });

        // Camera parallax
        this.camera.position.x = lerp(this.camera.position.x, mouse.smoothX * 0.5, 0.02);
        this.camera.position.y = lerp(this.camera.position.y, mouse.smoothY * 0.3, 0.02);
        this.camera.lookAt(this.scene.position);

        this.renderer.render(this.scene, this.camera);
    }

    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// ─── Smooth Scroll Observer ───
class ScrollAnimator {
    constructor() {
        this.init();
    }

    init() {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');

                        // Animate skill bars
                        if (entry.target.closest('.skills-section')) {
                            this.animateSkillBars(entry.target);
                        }
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px',
            }
        );

        document.querySelectorAll('.animate-on-scroll').forEach((el) => {
            observer.observe(el);
        });
    }

    animateSkillBars(container) {
        const bars = container.querySelectorAll('.skill-bar-fill');
        bars.forEach((bar, index) => {
            setTimeout(() => {
                bar.style.width = bar.dataset.width + '%';
            }, index * 150);
        });
    }
}

// ─── 3D Tilt Cards ───
class TiltEffect {
    constructor() {
        this.cards = document.querySelectorAll('.tilt-card');
        this.init();
    }

    init() {
        this.cards.forEach((card) => {
            card.addEventListener('mousemove', (e) => this.handleMove(e, card));
            card.addEventListener('mouseleave', (e) => this.handleLeave(e, card));
            card.addEventListener('mouseenter', (e) => this.handleEnter(e, card));
        });
    }

    handleMove(e, card) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -8;
        const rotateY = ((x - centerX) / centerX) * 8;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;

        // Shine effect
        const shine = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.06) 0%, transparent 60%)`;
        card.style.backgroundImage = shine;
    }

    handleLeave(e, card) {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        card.style.backgroundImage = 'none';
        card.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    }

    handleEnter(e, card) {
        card.style.transition = 'none';
    }
}

// ─── Navigation ───
class Navigation {
    constructor() {
        this.nav = document.getElementById('main-nav');
        this.toggle = document.getElementById('nav-toggle');
        this.mobileMenu = document.getElementById('mobile-menu');
        this.navLinks = document.querySelectorAll('.nav-link, .mobile-link');
        this.sections = document.querySelectorAll('.section');
        this.init();
    }

    init() {
        // Scroll effect
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                this.nav.classList.add('scrolled');
            } else {
                this.nav.classList.remove('scrolled');
            }
            this.updateActiveLink();
        });

        // Mobile toggle
        this.toggle.addEventListener('click', () => {
            this.toggle.classList.toggle('active');
            this.mobileMenu.classList.toggle('open');
        });

        // Smooth scroll
        this.navLinks.forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                    this.toggle.classList.remove('active');
                    this.mobileMenu.classList.remove('open');
                }
            });
        });
    }

    updateActiveLink() {
        let current = '';
        this.sections.forEach((section) => {
            const sectionTop = section.offsetTop - 100;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        this.navLinks.forEach((link) => {
            link.classList.remove('active');
            if (link.dataset.section === current) {
                link.classList.add('active');
            }
        });
    }
}

// ─── Counter Animation ───
class CounterAnimator {
    constructor() {
        this.init();
    }

    init() {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        this.animateCounters(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.5 }
        );

        const statsContainer = document.querySelector('.hero-stats');
        if (statsContainer) {
            observer.observe(statsContainer);
        }
    }

    animateCounters(container) {
        const counters = container.querySelectorAll('.stat-number');
        counters.forEach((counter) => {
            const target = parseInt(counter.dataset.count);
            const duration = 1500;
            const start = performance.now();

            const update = (timestamp) => {
                const elapsed = timestamp - start;
                const progress = Math.min(elapsed / duration, 1);

                // Easing
                const eased = 1 - Math.pow(1 - progress, 3);
                counter.textContent = Math.round(target * eased);

                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            };

            requestAnimationFrame(update);
        });
    }
}

// ─── Magnetic Buttons ───
class MagneticButtons {
    constructor() {
        this.buttons = document.querySelectorAll('.btn');
        this.init();
    }

    init() {
        this.buttons.forEach((btn) => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translate(0, 0)';
                btn.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            });

            btn.addEventListener('mouseenter', () => {
                btn.style.transition = 'none';
            });
        });
    }
}

// ─── Smooth Text Reveal ───
class TextReveal {
    constructor() {
        this.init();
    }

    init() {
        // Split hero title into characters for animation
        const titleName = document.querySelector('.title-name');
        if (titleName) {
            const text = titleName.textContent;
            titleName.innerHTML = '';
            [...text].forEach((char, i) => {
                const span = document.createElement('span');
                span.textContent = char === ' ' ? '\u00A0' : char;
                span.style.display = 'inline-block';
                span.style.animationDelay = `${0.5 + i * 0.04}s`;
                span.classList.add('char-reveal');
                titleName.appendChild(span);
            });
        }
    }
}

// ─── Preloader ───
class Preloader {
    constructor() {
        this.preloader = document.getElementById('preloader');
        this.init();
    }

    init() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.preloader.classList.add('loaded');
            }, 1200);
        });
    }
}

// ─── Parallax Sections ───
class SectionParallax {
    constructor() {
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            const hero = document.querySelector('.hero-content');
            if (hero) {
                hero.style.transform = `translateY(${scrollY * 0.15}px)`;
                hero.style.opacity = 1 - scrollY / 800;
            }

            const scrollInd = document.querySelector('.scroll-indicator');
            if (scrollInd) {
                scrollInd.style.opacity = 1 - scrollY / 300;
            }
        });
    }
}

// ─── Initialize Everything ───
document.addEventListener('DOMContentLoaded', () => {
    // Core systems
    new Preloader();
    new ParticleUniverse();
    new Navigation();

    // Animations
    new ScrollAnimator();
    new TiltEffect();
    new CounterAnimator();
    new MagneticButtons();
    new TextReveal();
    new SectionParallax();

    // Add char-reveal animation
    const style = document.createElement('style');
    style.textContent = `
        .char-reveal {
            opacity: 0;
            transform: translateY(30px) rotateX(-40deg);
            animation: charReveal 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        }
        @keyframes charReveal {
            to {
                opacity: 1;
                transform: translateY(0) rotateX(0deg);
            }
        }
    `;
    document.head.appendChild(style);
});
