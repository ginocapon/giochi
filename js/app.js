/**
 * PlayReward — App Principale
 * Vanilla JS, zero dipendenze
 * Streaks, Tiers, Chat, i18n, 3D tilt, Social Proof
 */

(function() {
    'use strict';

    // ======================
    // Translations (IT / EN)
    // ======================
    var LANG_KEY = 'playreward_lang';

    var translations = {
        it: {
            skipNav: 'Vai al contenuto principale',
            navGames: 'Giochi',
            navHow: 'Come Funziona',
            navPrizes: 'Premi',
            navTiers: 'Livelli',
            navReferral: 'Invita Amici',
            navSponsor: 'Per Sponsor',
            navCta: 'Gioca Ora',
            socialProof: '<span id="socialProofCount">12,450</span>\u20AC distribuiti ai giocatori',
            heroBadge: '100% Gratuito \u2014 Premi Veri \u2014 Zero Pubblicita\' Invasive',
            heroTitle: 'Gioca, Accumula Punti,<br><span class="highlight">Vinci Premi Veri</span>',
            heroSub: 'Mini-giochi 3D gratuiti con premi reali. Quiz, trivia, puzzle e molto altro. Gioca dal browser, senza scaricare nulla.',
            heroCta: 'Inizia a Giocare \u25B6',
            heroCtaSecondary: 'Scopri Come Funziona',
            statGames: 'Mini-Giochi',
            statFree: 'Sempre Gratis',
            statTransparency: 'Valore Trasparente',
            streakLabel: 'Giorni consecutivi di gioco',
            streakBonus: 'Bonus attuale: x1.0',
            gamesTag: 'GIOCHI',
            gamesTitle: 'I Nostri <span class="gradient-text">Mini-Giochi</span>',
            gamesSub: 'Scegli il tuo gioco preferito e inizia a guadagnare punti',
            game1Title: 'Quiz Cultura',
            game1Desc: 'Metti alla prova le tue conoscenze con domande di cultura generale.',
            game2Title: 'Trivia Challenge',
            game2Desc: 'Sfide a tempo su sport, cinema, musica e scienza.',
            game3Title: 'Puzzle Logici',
            game3Desc: 'Rompicapi e giochi di logica per allenare la mente.',
            game4Title: 'Memory Match',
            game4Desc: 'Trova le coppie il piu\' velocemente possibile.',
            game5Title: 'Speed Click',
            game5Desc: 'Riflessi fulminei. Clicca i bersagli prima che spariscano.',
            diffEasy: 'Facile',
            diffMedium: 'Media',
            diffHard: 'Difficile',
            checkpoint: 'Checkpoint',
            howTag: 'COME FUNZIONA',
            howTitle: 'Tre Passi per <span class="gradient-text">Vincere</span>',
            howSub: 'Inizia subito a guadagnare premi reali giocando',
            step1Title: 'Scegli un Gioco',
            step1Desc: 'Esplora il catalogo di mini-giochi: quiz, trivia, puzzle, memory e speed click. Tutti gratuiti e giocabili dal browser.',
            step2Title: 'Accumula Punti',
            step2Desc: 'Ogni partita completata ti assegna punti. Piu\' alto il punteggio, piu\' punti guadagni. Bonus streak giornaliero fino a x3.',
            step3Title: 'Riscatta i Premi',
            step3Desc: 'Converti i tuoi punti in gift card, buoni sconto, cashback e chiavi di gioco. 1 punto = 0,01\u20AC \u2014 sempre trasparente.',
            tiersTag: 'LIVELLI',
            tiersTitle: 'Scala i <span class="gradient-text">Livelli</span>',
            tiersSub: 'Piu\' giochi, piu\' guadagni. Ogni livello sblocca bonus esclusivi.',
            tierBronze: 'Bronze',
            tierSilver: 'Silver',
            tierGold: 'Gold',
            tierPlatinum: 'Platinum',
            tierDiamond: 'Diamond',
            rewardsTag: 'PREMI',
            rewardsTitle: 'Catalogo <span class="gradient-text">Premi</span>',
            rewardsSub: 'Converti i tuoi punti in premi reali \u2014 valore trasparente, sempre',
            cashNote: 'Valore fisso e trasparente. 1.000 punti = 10\u20AC di premi reali.',
            reward1: 'Gift Card Amazon',
            reward2: 'Cashback PayPal',
            reward3: 'Chiave Steam',
            reward4: 'Buoni Sconto',
            reward5: 'Credito App Store',
            reward6: 'Premi Esclusivi',
            reward7: 'Gift Card Spotify',
            reward8: 'Gift Card Netflix',
            rewardVal1: 'Valore: 50\u20AC',
            rewardVal2: 'Valore: 30\u20AC',
            rewardVal3: 'Valore: 20\u20AC',
            rewardVal4: 'Valore: 10\u20AC',
            rewardVal5: 'Valore: 15\u20AC',
            rewardVal6: 'Valore: 100\u20AC+',
            rewardVal7: 'Valore: 10\u20AC',
            rewardVal8: 'Valore: 25\u20AC',
            referralTag: 'INVITA',
            referralTitle: 'Invita Amici, <span class="gradient-text">Guadagna Punti</span>',
            referralSub: 'Ogni amico che si iscrive ti regala 500 punti bonus',
            referralLock: 'Raggiungi il livello Silver (1.000 pt) per sbloccare',
            referralCardTitle: 'Il Tuo Codice Referral',
            referralCardDesc: 'Condividi il tuo codice con gli amici. 500 punti per te + 200 punti per loro!',
            referralCopy: 'Copia',
            referralCopied: 'Copiato!',
            faqTitle: 'Domande <span class="gradient-text">Frequenti</span>',
            faqSub: 'Tutto quello che devi sapere su PlayReward',
            faq1q: 'Come funziona PlayReward?',
            faq1a: 'Giochi a mini-giochi gratuiti (quiz, trivia, puzzle), accumuli punti ad ogni partita completata, e converti i punti in premi reali come gift card, sconti e cashback.',
            faq2q: 'PlayReward e\' davvero gratuito?',
            faq2a: 'Si, giocare e\' completamente gratuito. I premi sono finanziati dai brand sponsor che pagano per raggiungere i nostri utenti attraverso la piattaforma.',
            faq3q: 'Quali premi posso vincere?',
            faq3a: 'Gift card Amazon, buoni sconto, cashback PayPal, chiavi Steam, credito App Store, abbonamenti Spotify/Netflix e premi esclusivi.',
            faq4q: 'Come si accumulano i punti?',
            faq4a: 'Ogni mini-gioco completato ti assegna punti in base al punteggio. Bonus streak giornaliero (fino a x3), quiz sponsorizzati e programma referral da 500 punti per invito.',
            faq5q: 'Posso giocare da mobile?',
            faq5a: 'Si, PlayReward e\' progettato mobile-first. Funziona perfettamente su smartphone, tablet e desktop senza bisogno di scaricare app.',
            faq6q: 'Come funziona la streak giornaliera?',
            faq6a: 'Giocando ogni giorno accumuli una streak. Il bonus cresce: giorno 3 = x1.2, giorno 7 = x1.5, giorno 14 = x2.0, giorno 30 = x3.0. Se salti un giorno, la streak si resetta.',
            footerDesc: 'La piattaforma italiana di mini-giochi con premi reali. Gioca gratis, accumula punti, vinci premi. Finanziata da brand sponsor.',
            footerPlatform: 'Piattaforma',
            footerLegal: 'Legale',
            footerTerms: 'Termini di Servizio',
            footerRights: 'Tutti i diritti riservati.',
            chatOnline: 'Online',
            chatWelcome: 'Ciao! Sono PlayBot, il tuo assistente. Come posso aiutarti?',
            chatQ1: 'Come funziona?',
            chatQ2: 'Quali premi ci sono?',
            chatQ3: 'Cos\'e\' la streak?',
            chatQ4: 'Programma referral'
        },
        en: {
            skipNav: 'Skip to main content',
            navGames: 'Games',
            navHow: 'How It Works',
            navPrizes: 'Prizes',
            navTiers: 'Tiers',
            navReferral: 'Invite Friends',
            navSponsor: 'For Sponsors',
            navCta: 'Play Now',
            socialProof: '<span id="socialProofCount">12,450</span>\u20AC distributed to players',
            heroBadge: '100% Free \u2014 Real Prizes \u2014 Zero Invasive Ads',
            heroTitle: 'Play, Earn Points,<br><span class="highlight">Win Real Prizes</span>',
            heroSub: 'Free 3D mini-games with real prizes. Quiz, trivia, puzzle and more. Play from your browser, no download needed.',
            heroCta: 'Start Playing \u25B6',
            heroCtaSecondary: 'Learn How It Works',
            statGames: 'Mini-Games',
            statFree: 'Always Free',
            statTransparency: 'Transparent Value',
            streakLabel: 'Consecutive days played',
            streakBonus: 'Current bonus: x1.0',
            gamesTag: 'GAMES',
            gamesTitle: 'Our <span class="gradient-text">Mini-Games</span>',
            gamesSub: 'Choose your favorite game and start earning points',
            game1Title: 'Culture Quiz',
            game1Desc: 'Test your knowledge with general culture questions.',
            game2Title: 'Trivia Challenge',
            game2Desc: 'Timed challenges on sports, cinema, music and science.',
            game3Title: 'Logic Puzzles',
            game3Desc: 'Brain teasers and logic games to train your mind.',
            game4Title: 'Memory Match',
            game4Desc: 'Find matching pairs as quickly as possible.',
            game5Title: 'Speed Click',
            game5Desc: 'Lightning reflexes. Click targets before they disappear.',
            diffEasy: 'Easy',
            diffMedium: 'Medium',
            diffHard: 'Hard',
            checkpoint: 'Checkpoint',
            howTag: 'HOW IT WORKS',
            howTitle: 'Three Steps to <span class="gradient-text">Win</span>',
            howSub: 'Start earning real prizes by playing right now',
            step1Title: 'Choose a Game',
            step1Desc: 'Explore our mini-game catalog: quiz, trivia, puzzle, memory and speed click. All free and playable from your browser.',
            step2Title: 'Earn Points',
            step2Desc: 'Every completed game awards points. Higher score means more points. Daily streak bonus up to x3.',
            step3Title: 'Redeem Prizes',
            step3Desc: 'Convert your points into gift cards, coupons, cashback and game keys. 1 point = \u20AC0.01 \u2014 always transparent.',
            tiersTag: 'TIERS',
            tiersTitle: 'Climb the <span class="gradient-text">Ranks</span>',
            tiersSub: 'Play more, earn more. Each tier unlocks exclusive bonuses.',
            tierBronze: 'Bronze',
            tierSilver: 'Silver',
            tierGold: 'Gold',
            tierPlatinum: 'Platinum',
            tierDiamond: 'Diamond',
            rewardsTag: 'PRIZES',
            rewardsTitle: 'Prize <span class="gradient-text">Catalog</span>',
            rewardsSub: 'Convert your points into real prizes \u2014 transparent value, always',
            cashNote: 'Fixed and transparent value. 1,000 points = \u20AC10 of real prizes.',
            reward1: 'Amazon Gift Card',
            reward2: 'PayPal Cashback',
            reward3: 'Steam Key',
            reward4: 'Discount Coupons',
            reward5: 'App Store Credit',
            reward6: 'Exclusive Prizes',
            reward7: 'Spotify Gift Card',
            reward8: 'Netflix Gift Card',
            rewardVal1: 'Value: \u20AC50',
            rewardVal2: 'Value: \u20AC30',
            rewardVal3: 'Value: \u20AC20',
            rewardVal4: 'Value: \u20AC10',
            rewardVal5: 'Value: \u20AC15',
            rewardVal6: 'Value: \u20AC100+',
            rewardVal7: 'Value: \u20AC10',
            rewardVal8: 'Value: \u20AC25',
            referralTag: 'INVITE',
            referralTitle: 'Invite Friends, <span class="gradient-text">Earn Points</span>',
            referralSub: 'Every friend who signs up gives you 500 bonus points',
            referralLock: 'Reach Silver tier (1,000 pt) to unlock',
            referralCardTitle: 'Your Referral Code',
            referralCardDesc: 'Share your code with friends. 500 points for you + 200 points for them!',
            referralCopy: 'Copy',
            referralCopied: 'Copied!',
            faqTitle: 'Frequently <span class="gradient-text">Asked Questions</span>',
            faqSub: 'Everything you need to know about PlayReward',
            faq1q: 'How does PlayReward work?',
            faq1a: 'Play free mini-games (quiz, trivia, puzzle), earn points with every completed game, and convert points into real prizes like gift cards, coupons and cashback.',
            faq2q: 'Is PlayReward really free?',
            faq2a: 'Yes, playing is completely free. Prizes are funded by brand sponsors who pay to reach our users through the platform.',
            faq3q: 'What prizes can I win?',
            faq3a: 'Amazon gift cards, coupons, PayPal cashback, Steam keys, App Store credit, Spotify/Netflix subscriptions and exclusive prizes.',
            faq4q: 'How do I earn points?',
            faq4a: 'Every completed mini-game awards points based on your score. Daily streak bonus (up to x3), sponsored quizzes and referral program worth 500 points per invite.',
            faq5q: 'Can I play on mobile?',
            faq5a: 'Yes, PlayReward is designed mobile-first. It works on smartphone, tablet and desktop without any app download.',
            faq6q: 'How does the daily streak work?',
            faq6a: 'Playing every day builds your streak. Bonus grows: day 3 = x1.2, day 7 = x1.5, day 14 = x2.0, day 30 = x3.0. Miss a day and the streak resets.',
            footerDesc: 'The Italian mini-game platform with real prizes. Play free, earn points, win prizes. Funded by brand sponsors.',
            footerPlatform: 'Platform',
            footerLegal: 'Legal',
            footerTerms: 'Terms of Service',
            footerRights: 'All rights reserved.',
            chatOnline: 'Online',
            chatWelcome: 'Hi! I\'m PlayBot, your assistant. How can I help you?',
            chatQ1: 'How does it work?',
            chatQ2: 'What prizes are there?',
            chatQ3: 'What\'s the streak?',
            chatQ4: 'Referral program'
        }
    };

    var currentLang = localStorage.getItem(LANG_KEY) || 'it';

    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem(LANG_KEY, lang);
        document.documentElement.lang = lang;

        var t = translations[lang];
        document.querySelectorAll('[data-i18n]').forEach(function(el) {
            var key = el.getAttribute('data-i18n');
            if (t[key] !== undefined) {
                el.innerHTML = t[key];
            }
        });

        // Update lang toggle buttons
        document.querySelectorAll('.lang-btn').forEach(function(btn) {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
        });

        // Re-animate social proof counter
        animateSocialProof();
    }

    // ======================
    // Mobile Menu
    // ======================
    var hamburger = document.querySelector('.hamburger');
    var mobileMenu = document.getElementById('mobileMenu');

    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', function() {
            var isOpen = mobileMenu.classList.toggle('active');
            hamburger.classList.toggle('active', isOpen);
            hamburger.setAttribute('aria-expanded', isOpen);
        });

        mobileMenu.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // ======================
    // Language Toggle
    // ======================
    document.querySelectorAll('.lang-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setLanguage(this.getAttribute('data-lang'));
        });
    });

    // ======================
    // FAQ Accordion
    // ======================
    document.querySelectorAll('.faq-q').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var item = this.closest('.faq-item');
            var isOpen = item.classList.contains('active');

            document.querySelectorAll('.faq-item.active').forEach(function(openItem) {
                openItem.classList.remove('active');
                openItem.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
            });

            if (!isOpen) {
                item.classList.add('active');
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // ======================
    // Smooth Scroll
    // ======================
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var targetId = this.getAttribute('href');
            if (targetId === '#') return;
            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                var offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 64;
                var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
        });
    });

    // ======================
    // Nav Background on Scroll
    // ======================
    var nav = document.querySelector('.nav');
    if (nav) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                nav.style.background = 'rgba(7, 7, 15, 0.97)';
                nav.style.borderBottomColor = 'rgba(108, 99, 255, 0.2)';
            } else {
                nav.style.background = 'rgba(7, 7, 15, 0.85)';
                nav.style.borderBottomColor = 'rgba(108, 99, 255, 0.12)';
            }
        }, { passive: true });
    }

    // ======================
    // Social Proof Counter Animation
    // ======================
    function animateSocialProof() {
        var el = document.getElementById('socialProofCount');
        if (!el) return;

        var target = 12450;
        var duration = 2000;
        var start = 0;
        var startTime = null;

        function tick(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
            var current = Math.floor(start + (target - start) * eased);
            el.textContent = current.toLocaleString('it-IT');
            if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    // ======================
    // Daily Streak UI
    // ======================
    function renderStreak() {
        if (typeof PlayRewardPoints === 'undefined') return;

        var data = PlayRewardPoints.getStreakData();
        var countEl = document.getElementById('streakCount');
        var daysEl = document.getElementById('streakDays');
        var bonusEl = document.getElementById('streakBonus');

        if (countEl) countEl.textContent = data.count;

        if (daysEl) {
            var html = '';
            var today = new Date();
            var dayLabels = currentLang === 'en'
                ? ['S','M','T','W','T','F','S']
                : ['D','L','M','M','G','V','S'];

            for (var i = 6; i >= 0; i--) {
                var d = new Date(today);
                d.setDate(d.getDate() - i);
                var dateStr = d.toISOString().split('T')[0];
                var dayIndex = d.getDay();
                var isCompleted = data.history && data.history.indexOf(dateStr) !== -1;
                var isToday = i === 0;

                var cls = 'streak-day';
                if (isToday && isCompleted) cls += ' today';
                else if (isCompleted) cls += ' completed';

                html += '<div class="' + cls + '">' + dayLabels[dayIndex] + '</div>';
            }
            daysEl.innerHTML = html;
        }

        if (bonusEl) {
            var mult = PlayRewardPoints.getStreakMultiplier();
            bonusEl.textContent = (currentLang === 'en' ? 'Current bonus: x' : 'Bonus attuale: x') + mult.toFixed(1);
        }
    }

    // ======================
    // Tier UI
    // ======================
    function renderTiers() {
        if (typeof PlayRewardPoints === 'undefined') return;

        var currentTier = PlayRewardPoints.getTier();
        document.querySelectorAll('.tier-card').forEach(function(card) {
            var tierName = card.getAttribute('data-tier');
            card.classList.remove('active', 'locked');

            // Remove old badge
            var oldBadge = card.querySelector('.tier-current-badge');
            if (oldBadge) oldBadge.remove();

            if (tierName === currentTier.name) {
                card.classList.add('active');
                var badge = document.createElement('span');
                badge.className = 'tier-current-badge';
                badge.textContent = currentLang === 'en' ? 'YOU' : 'TU';
                card.appendChild(badge);
            } else {
                var tierObj = PlayRewardPoints.TIERS.find(function(t) { return t.name === tierName; });
                if (tierObj && tierObj.min > PlayRewardPoints.getPoints()) {
                    card.classList.add('locked');
                }
            }
        });
    }

    // ======================
    // Nav Points Counter
    // ======================
    function renderNavPoints() {
        if (typeof PlayRewardPoints === 'undefined') return;
        var el = document.getElementById('navPointsCount');
        if (el) el.textContent = PlayRewardPoints.getPoints().toLocaleString('it-IT');
    }

    // ======================
    // Checkpoint Progress Bars
    // ======================
    function renderCheckpoints() {
        if (typeof PlayRewardPoints === 'undefined') return;

        var games = ['quiz', 'trivia', 'puzzle', 'memory', 'speed-click'];
        var maxCheckpoint = 5;

        games.forEach(function(game) {
            var cp = PlayRewardPoints.getGameCheckpoint(game);
            var pct = Math.min((cp / maxCheckpoint) * 100, 100);

            var fill = document.querySelector('.progress-fill[data-game="' + game + '"]');
            if (fill) fill.style.width = pct + '%';

            var label = document.querySelector('.progress-value[data-game="' + game + '"]');
            if (label) label.textContent = Math.min(cp, maxCheckpoint) + '/' + maxCheckpoint;
        });
    }

    // ======================
    // Referral UI
    // ======================
    function renderReferral() {
        if (typeof PlayRewardPoints === 'undefined') return;

        var card = document.getElementById('referralCard');
        var codeEl = document.getElementById('referralCode');
        var copyBtn = document.getElementById('referralCopyBtn');

        if (!card) return;

        if (PlayRewardPoints.isReferralUnlocked()) {
            card.classList.remove('locked');
            if (codeEl) codeEl.textContent = PlayRewardPoints.getReferralCode();
        } else {
            card.classList.add('locked');
        }

        if (copyBtn) {
            copyBtn.addEventListener('click', function() {
                var code = PlayRewardPoints.getReferralCode();
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(code);
                }
                var t = translations[currentLang];
                this.textContent = t.referralCopied;
                var btn = this;
                setTimeout(function() {
                    btn.textContent = t.referralCopy;
                }, 2000);
            });
        }
    }

    // ======================
    // Chat Widget
    // ======================
    var chatFab = document.getElementById('chatFab');
    var chatPanel = document.getElementById('chatPanel');
    var chatClose = document.getElementById('chatClose');
    var chatMessages = document.getElementById('chatMessages');
    var chatQuickReplies = document.getElementById('chatQuickReplies');

    var chatResponses = {
        it: {
            'come-funziona': 'Semplice! Scegli un mini-gioco, gioca gratis e accumula punti. Poi converti i punti in premi reali come gift card Amazon, cashback PayPal e chiavi Steam. 1 punto = 0,01\u20AC!',
            'premi': 'Abbiamo un catalogo ricco: Gift Card Amazon, Cashback PayPal, Chiavi Steam, Buoni Sconto, Credito App Store, Gift Card Spotify e Netflix, e premi esclusivi da 100\u20AC+!',
            'streak': 'Giocando ogni giorno costruisci una streak! I bonus crescono: giorno 3 = x1.2, giorno 7 = x1.5, giorno 14 = x2.0, giorno 30 = x3.0. Non saltare neanche un giorno!',
            'referral': 'Raggiungi il livello Silver (1.000 pt) per sbloccare il tuo codice referral. Ogni amico invitato ti regala 500 punti bonus, e lui riceve 200 punti di benvenuto!'
        },
        en: {
            'come-funziona': 'Simple! Choose a mini-game, play for free and earn points. Then convert points into real prizes like Amazon gift cards, PayPal cashback and Steam keys. 1 point = \u20AC0.01!',
            'premi': 'We have a rich catalog: Amazon Gift Cards, PayPal Cashback, Steam Keys, Discount Coupons, App Store Credit, Spotify and Netflix Gift Cards, and exclusive prizes worth \u20AC100+!',
            'streak': 'Playing every day builds your streak! Bonuses grow: day 3 = x1.2, day 7 = x1.5, day 14 = x2.0, day 30 = x3.0. Don\'t skip a single day!',
            'referral': 'Reach Silver tier (1,000 pt) to unlock your referral code. Every invited friend gives you 500 bonus points, and they get 200 welcome points!'
        }
    };

    if (chatFab && chatPanel) {
        chatFab.addEventListener('click', function() {
            chatPanel.classList.toggle('active');
        });
    }

    if (chatClose) {
        chatClose.addEventListener('click', function() {
            chatPanel.classList.remove('active');
        });
    }

    if (chatQuickReplies) {
        chatQuickReplies.addEventListener('click', function(e) {
            var btn = e.target.closest('.chat-quick-btn');
            if (!btn) return;

            var reply = btn.getAttribute('data-reply');
            var userText = btn.textContent;

            // Add user message
            var userMsg = document.createElement('div');
            userMsg.className = 'chat-msg user';
            userMsg.textContent = userText;
            chatMessages.appendChild(userMsg);

            // Add bot response
            setTimeout(function() {
                var botMsg = document.createElement('div');
                botMsg.className = 'chat-msg bot';
                var responses = chatResponses[currentLang] || chatResponses.it;
                botMsg.textContent = responses[reply] || 'Non ho capito. Prova un\'altra domanda!';
                chatMessages.appendChild(botMsg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 500);

            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    // ======================
    // 3D Tilt Effect on Game Cards
    // ======================
    if (window.matchMedia('(hover: hover)').matches) {
        document.querySelectorAll('[data-tilt]').forEach(function(card) {
            card.addEventListener('mousemove', function(e) {
                var rect = card.getBoundingClientRect();
                var x = e.clientX - rect.left;
                var y = e.clientY - rect.top;
                var centerX = rect.width / 2;
                var centerY = rect.height / 2;
                var rotateX = ((y - centerY) / centerY) * -8;
                var rotateY = ((x - centerX) / centerX) * 8;
                card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-4px)';
            });

            card.addEventListener('mouseleave', function() {
                card.style.transform = '';
            });
        });
    }

    // ======================
    // Scroll Reveal (IntersectionObserver)
    // ======================
    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        document.querySelectorAll('.reveal').forEach(function(el) {
            observer.observe(el);
        });
    } else {
        // Fallback: mostra tutto
        document.querySelectorAll('.reveal').forEach(function(el) {
            el.classList.add('visible');
        });
    }

    // ======================
    // Init
    // ======================
    function init() {
        setLanguage(currentLang);
        renderStreak();
        renderTiers();
        renderNavPoints();
        renderCheckpoints();
        renderReferral();
        animateSocialProof();
    }

    // Aspetta che PlayRewardPoints sia disponibile
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
