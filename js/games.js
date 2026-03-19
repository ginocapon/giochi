/**
 * PlayReward — Games Engine
 * Utilities condivise tra tutti i mini-giochi
 */

var PlayRewardGames = (function() {
    'use strict';

    // Timer con callback
    function createTimer(durationSec, onTick, onEnd) {
        var remaining = durationSec;
        var interval = null;

        function start() {
            if (interval) return;
            interval = setInterval(function() {
                remaining--;
                if (onTick) onTick(remaining);
                if (remaining <= 0) {
                    stop();
                    if (onEnd) onEnd();
                }
            }, 1000);
        }

        function stop() {
            if (interval) {
                clearInterval(interval);
                interval = null;
            }
        }

        function getRemaining() {
            return remaining;
        }

        return { start: start, stop: stop, getRemaining: getRemaining };
    }

    // Mescola array (Fisher-Yates)
    function shuffle(arr) {
        var copy = arr.slice();
        for (var i = copy.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var temp = copy[i];
            copy[i] = copy[j];
            copy[j] = temp;
        }
        return copy;
    }

    // Calcola punti in base a prestazione
    function calculatePoints(score, maxScore, basePoints, bonusMultiplier) {
        var ratio = score / maxScore;
        var points = Math.round(basePoints * ratio);
        if (ratio >= 0.9) points = Math.round(points * (bonusMultiplier || 1.5));
        return Math.max(points, 1); // Minimo 1 punto
    }

    // Formatta tempo mm:ss
    function formatTime(seconds) {
        var m = Math.floor(seconds / 60);
        var s = seconds % 60;
        return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    }

    // Mostra schermata risultati
    function showResults(container, data) {
        var html = '<div class="game-results">';
        html += '<h2>' + (data.title || 'Partita Finita!') + '</h2>';
        html += '<p class="result-score">Punteggio: <strong>' + data.score + '</strong></p>';
        html += '<p class="result-points">+ <strong>' + data.points + '</strong> punti guadagnati!</p>';
        if (data.message) html += '<p class="result-message">' + data.message + '</p>';
        html += '<a href="../../giochi.html" class="result-btn">Gioca Ancora</a>';
        html += '</div>';
        container.innerHTML = html;

        // Aggiungi punti
        if (typeof PlayRewardPoints !== 'undefined') {
            PlayRewardPoints.addPoints(data.points, data.source || 'gioco');
        }
    }

    return {
        createTimer: createTimer,
        shuffle: shuffle,
        calculatePoints: calculatePoints,
        formatTime: formatTime,
        showResults: showResults
    };

})();
