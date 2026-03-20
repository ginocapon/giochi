/**
 * PlayReward — Sistema Punti Avanzato
 * Streaks, Tier System, Referral — localStorage
 */

var PlayRewardPoints = (function() {
    'use strict';

    var STORAGE_KEY = 'playreward_points';
    var HISTORY_KEY = 'playreward_history';
    var STREAK_KEY = 'playreward_streak';
    var REFERRAL_KEY = 'playreward_referral';
    var CHECKPOINTS_KEY = 'playreward_checkpoints';

    // --- Tier System ---
    var TIERS = [
        { name: 'bronze',   min: 0,     max: 999,    multiplier: 1.0 },
        { name: 'silver',   min: 1000,  max: 4999,   multiplier: 1.2 },
        { name: 'gold',     min: 5000,  max: 14999,  multiplier: 1.5 },
        { name: 'platinum', min: 15000, max: 39999,  multiplier: 2.0 },
        { name: 'diamond',  min: 40000, max: Infinity, multiplier: 3.0 }
    ];

    // --- Streak Bonuses ---
    var STREAK_BONUSES = [
        { days: 30, multiplier: 3.0 },
        { days: 14, multiplier: 2.0 },
        { days: 7,  multiplier: 1.5 },
        { days: 3,  multiplier: 1.2 },
        { days: 1,  multiplier: 1.0 }
    ];

    // --- Points ---
    function getPoints() {
        var stored = localStorage.getItem(STORAGE_KEY);
        return stored ? parseInt(stored, 10) : 0;
    }

    function addPoints(amount, source) {
        var current = getPoints();
        var newTotal = current + amount;
        localStorage.setItem(STORAGE_KEY, newTotal.toString());
        addToHistory({
            amount: amount,
            source: source || 'gioco',
            date: new Date().toISOString(),
            total: newTotal
        });
        return newTotal;
    }

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

    // --- History ---
    function getHistory() {
        var stored = localStorage.getItem(HISTORY_KEY);
        return stored ? JSON.parse(stored) : [];
    }

    function addToHistory(entry) {
        var history = getHistory();
        history.unshift(entry);
        if (history.length > 100) history = history.slice(0, 100);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    }

    // --- Tier ---
    function getTier() {
        var pts = getPoints();
        for (var i = TIERS.length - 1; i >= 0; i--) {
            if (pts >= TIERS[i].min) return TIERS[i];
        }
        return TIERS[0];
    }

    function getTierMultiplier() {
        return getTier().multiplier;
    }

    // --- Streak ---
    function getStreakData() {
        var stored = localStorage.getItem(STREAK_KEY);
        if (!stored) return { count: 0, lastDate: null, history: [] };
        return JSON.parse(stored);
    }

    function updateStreak() {
        var data = getStreakData();
        var today = new Date().toISOString().split('T')[0];

        if (data.lastDate === today) return data;

        var yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        var yesterdayStr = yesterday.toISOString().split('T')[0];

        if (data.lastDate === yesterdayStr) {
            data.count += 1;
        } else {
            data.count = 1;
        }

        data.lastDate = today;

        // Mantieni storico ultimi 30 giorni
        if (!data.history) data.history = [];
        if (data.history.indexOf(today) === -1) {
            data.history.push(today);
        }
        if (data.history.length > 30) {
            data.history = data.history.slice(-30);
        }

        localStorage.setItem(STREAK_KEY, JSON.stringify(data));
        return data;
    }

    function getStreakMultiplier() {
        var data = getStreakData();
        for (var i = 0; i < STREAK_BONUSES.length; i++) {
            if (data.count >= STREAK_BONUSES[i].days) {
                return STREAK_BONUSES[i].multiplier;
            }
        }
        return 1.0;
    }

    // --- Checkpoints ---
    function getCheckpoints() {
        var stored = localStorage.getItem(CHECKPOINTS_KEY);
        return stored ? JSON.parse(stored) : {};
    }

    function addCheckpoint(game) {
        var cp = getCheckpoints();
        if (!cp[game]) cp[game] = 0;
        cp[game] += 1;
        localStorage.setItem(CHECKPOINTS_KEY, JSON.stringify(cp));
        return cp[game];
    }

    function getGameCheckpoint(game) {
        var cp = getCheckpoints();
        return cp[game] || 0;
    }

    // --- Referral ---
    function getReferralCode() {
        var code = localStorage.getItem(REFERRAL_KEY);
        if (!code) {
            var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
            code = 'PR-';
            for (var i = 0; i < 6; i++) {
                code += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            localStorage.setItem(REFERRAL_KEY, code);
        }
        return code;
    }

    function isReferralUnlocked() {
        return getPoints() >= 1000; // Silver tier
    }

    // --- Reset ---
    function reset() {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(HISTORY_KEY);
        localStorage.removeItem(STREAK_KEY);
        localStorage.removeItem(REFERRAL_KEY);
        localStorage.removeItem(CHECKPOINTS_KEY);
    }

    return {
        getPoints: getPoints,
        addPoints: addPoints,
        spendPoints: spendPoints,
        getHistory: getHistory,
        getTier: getTier,
        getTierMultiplier: getTierMultiplier,
        getStreakData: getStreakData,
        updateStreak: updateStreak,
        getStreakMultiplier: getStreakMultiplier,
        getCheckpoints: getCheckpoints,
        addCheckpoint: addCheckpoint,
        getGameCheckpoint: getGameCheckpoint,
        getReferralCode: getReferralCode,
        isReferralUnlocked: isReferralUnlocked,
        reset: reset,
        TIERS: TIERS
    };

})();
