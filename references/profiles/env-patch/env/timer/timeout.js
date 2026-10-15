/**
 * @env-module Timer
 * @description Macro-task timer queue. Never runs the callback synchronously.
 * @compatibility Chrome 80+, Firefox 75+, Edge 79+
 * @note On hosts without a native event loop, drive the queue with __drainTimers__.
 *       setInterval is a no-op (returns 0) when no native interval exists.
 */

(function () {
    const host = typeof window !== 'undefined' ? window : globalThis;
    const originalSetTimeout = host.setTimeout;
    const originalClearTimeout = host.clearTimeout;
    const originalSetInterval = host.setInterval;
    const originalClearInterval = host.clearInterval;

    let timerId = 0;
    const timers = new Map();
    let scheduling = false;

    function isUsableNative(fn) {
        return typeof fn === 'function';
    }

    function runTimer(id) {
        const timer = timers.get(id);
        if (!timer || timer.cleared) {
            return false;
        }
        timers.delete(id);
        try {
            timer.callback.apply(host, timer.args);
        } catch (err) {
            if (typeof host.console === 'object' && host.console && typeof host.console.error === 'function') {
                host.console.error(err);
            }
        }
        return true;
    }

    function scheduleNative(id, delay) {
        if (!isUsableNative(originalSetTimeout)) {
            return undefined;
        }
        let ranSync = false;
        scheduling = true;
        let realId;
        try {
            realId = originalSetTimeout.call(host, function () {
                if (scheduling) {
                    ranSync = true;
                    return;
                }
                runTimer(id);
            }, delay);
        } finally {
            scheduling = false;
        }
        if (ranSync) {
            return undefined;
        }
        return realId;
    }

    host.setTimeout = function (callback, delay) {
        const args = Array.prototype.slice.call(arguments, 2);
        let fn = callback;
        if (typeof fn !== 'function') {
            const code = String(callback);
            fn = function () {
                (0, eval)(code);
            };
        }
        const id = ++timerId;
        const timer = {
            callback: fn,
            delay: delay || 0,
            args: args,
            createdAt: Date.now(),
            cleared: false,
            realId: undefined,
        };
        timers.set(id, timer);
        timer.realId = scheduleNative(id, timer.delay);
        return id;
    };

    host.clearTimeout = function (id) {
        const timer = timers.get(id);
        if (!timer) {
            if (isUsableNative(originalClearTimeout)) {
                originalClearTimeout.call(host, id);
            }
            return;
        }
        timer.cleared = true;
        timers.delete(id);
        if (timer.realId !== undefined && isUsableNative(originalClearTimeout)) {
            originalClearTimeout.call(host, timer.realId);
        }
    };

    host.setInterval = function (callback, delay) {
        const args = Array.prototype.slice.call(arguments, 2);
        if (!isUsableNative(originalSetInterval)) {
            return 0;
        }
        let fn = callback;
        if (typeof fn !== 'function') {
            const code = String(callback);
            fn = function () {
                (0, eval)(code);
            };
        }
        let ranSync = false;
        scheduling = true;
        let realId;
        try {
            realId = originalSetInterval.call(host, function () {
                if (scheduling) {
                    ranSync = true;
                    return;
                }
                try {
                    fn.apply(host, args);
                } catch (err) {
                    if (typeof host.console === 'object' && host.console && typeof host.console.error === 'function') {
                        host.console.error(err);
                    }
                }
            }, delay || 0);
        } finally {
            scheduling = false;
        }
        if (ranSync) {
            return 0;
        }
        return realId;
    };

    host.clearInterval = function (id) {
        if (isUsableNative(originalClearInterval)) {
            originalClearInterval.call(host, id);
        }
    };

    host.queueMicrotask = host.queueMicrotask || function (callback) {
        Promise.resolve().then(callback);
    };

    host.__getActiveTimers__ = function () {
        return {
            timeouts: Array.from(timers.entries()).map(([id, t]) => ({
                id: id,
                delay: t.delay,
                age: Date.now() - t.createdAt,
            })),
            intervals: [],
        };
    };

    host.__clearAllTimers__ = function () {
        Array.from(timers.keys()).forEach(function (id) {
            host.clearTimeout(id);
        });
    };

    host.__drainTimers__ = function (limit) {
        const max = limit == null ? 20000 : limit;
        let n = 0;
        while (timers.size && n < max) {
            const id = timers.keys().next().value;
            if (runTimer(id)) {
                n += 1;
            } else {
                timers.delete(id);
            }
        }
        return n;
    };
})();
