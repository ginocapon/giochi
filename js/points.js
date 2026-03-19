/**
 * PlayReward — Sistema Punti
 * Gestione punti utente con localStorage
 */

var PlayRewardPoints = (function() {
    'use strict';

    var STORAGE_KEY = 'playreward_points';
    var HISTORY_KEY = 'playreward_history';

    // Leggi punti correnti
    function getPoints() {
        var stored = localStorage.getItem(STORAGE_KEY);
        return stored ? parseInt(stored, 10) : 0;
    }

    // Aggiungi punti
    function addPoints(amount, source) {
        var current = getPoints();
        var newTotal = current + amount;
        localStorage.setItem(STORAGE_KEY, newTotal.toString());

        // Registra in storico
        addToHistory({
            amount: amount,
            source: source || 'gioco',
            date: new Date().toISOString(),
            total: newTotal
        });

        return newTotal;
    }

    // Sottrai punti (per riscatto premi)
    function spendPoints(amount, prize) {
        var current = getPoints();
        if (current < amount) return false;

        var newTotal = current - amount;
        localStorage.setItem(STORAGE_KEY, newTotal.toString());

        addToHistory({
            amount: -amount,
            source: 'riscatto: ' + (prize || 'premio'),
            date: new Date().toISOString(),
            total: newTotal
        });

        return newTotal;
    }

    // Storico transazioni
    function getHistory() {
        var stored = localStorage.getItem(HISTORY_KEY);
        return stored ? JSON.parse(stored) : [];
    }

    function addToHistory(entry) {
        var history = getHistory();
        history.unshift(entry); // Piu' recente in cima
        // Mantieni solo le ultime 100 transazioni
        if (history.length > 100) history = history.slice(0, 100);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    }

    // Reset (per debug)
    function reset() {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(HISTORY_KEY);
    }

    return {
        getPoints: getPoints,
        addPoints: addPoints,
        spendPoints: spendPoints,
        getHistory: getHistory,
        reset: reset
    };

})();
