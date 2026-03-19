/**
 * PlayReward — App principale
 * Vanilla JS, zero dipendenze
 */

(function() {
    'use strict';

    // === Mobile Menu ===
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.getElementById('mobileMenu');

    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', function() {
            const isOpen = mobileMenu.classList.toggle('active');
            hamburger.setAttribute('aria-expanded', isOpen);
            hamburger.setAttribute('aria-label', isOpen ? 'Chiudi menu' : 'Apri menu');
        });

        // Chiudi menu quando si clicca un link
        mobileMenu.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                hamburger.setAttribute('aria-label', 'Apri menu');
            });
        });
    }

    // === FAQ Accordion ===
    document.querySelectorAll('.faq-q').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var item = this.closest('.faq-item');
            var isOpen = item.classList.contains('active');

            // Chiudi tutti
            document.querySelectorAll('.faq-item.active').forEach(function(openItem) {
                openItem.classList.remove('active');
                openItem.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
            });

            // Apri quello cliccato (se non era gia' aperto)
            if (!isOpen) {
                item.classList.add('active');
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // === Smooth Scroll per link interni ===
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var targetId = this.getAttribute('href');
            if (targetId === '#') return;
            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // === Nav background on scroll ===
    var nav = document.querySelector('.nav');
    if (nav) {
        var lastScroll = 0;
        window.addEventListener('scroll', function() {
            var currentScroll = window.pageYOffset;
            if (currentScroll > 50) {
                nav.style.background = 'rgba(26, 26, 46, 0.98)';
            } else {
                nav.style.background = 'rgba(26, 26, 46, 0.95)';
            }
            lastScroll = currentScroll;
        }, { passive: true });
    }

})();
