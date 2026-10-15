import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const profileDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const timeoutSource = fs.readFileSync(path.join(profileDir, 'env', 'timer', 'timeout.js'), 'utf8');

function createHost() {
  const context = vm.createContext({ Map, Date, Array, Promise, console });
  context.globalThis = context;
  context.window = context;
  return context;
}

function loadTimeout(context) {
  vm.runInContext(timeoutSource, context, { filename: 'timeout.js' });
}

{
  const host = createHost();
  loadTimeout(host);
  vm.runInContext('globalThis.__ran = false;', host);
  const id = vm.runInContext('setTimeout(function () { globalThis.__ran = true; }, 0)', host);
  assert.equal(typeof id, 'number');
  assert.notEqual(id, 0);
  assert.equal(vm.runInContext('globalThis.__ran', host), false);
  assert.equal(vm.runInContext('__drainTimers__(10)', host), 1);
  assert.equal(vm.runInContext('globalThis.__ran', host), true);
}

{
  const host = createHost();
  vm.runInContext(
    'setTimeout = function (fn) { fn(); return 1; }; setInterval = function (fn) { fn(); return 1; };',
    host,
  );
  loadTimeout(host);
  vm.runInContext('globalThis.__count = 0;', host);
  const ids = vm.runInContext(
    `(function () {
      function boom() {
        globalThis.__count += 1;
        if (globalThis.__count > 20) throw new Error('sync setTimeout recurse');
        setTimeout(boom, 0);
      }
      return {
        timeoutId: setTimeout(boom, 0),
        intervalId: setInterval(function () { globalThis.__count += 100; }, 0),
        countBeforeDrain: globalThis.__count,
      };
    })()`,
    host,
  );
  assert.equal(ids.countBeforeDrain, 0);
  assert.equal(ids.intervalId, 0);
  const drained = vm.runInContext('__drainTimers__(5)', host);
  assert.ok(drained >= 1);
  const count = vm.runInContext('globalThis.__count', host);
  assert.ok(count >= 1);
  assert.ok(count < 100);
}

{
  const host = createHost();
  loadTimeout(host);
  vm.runInContext(
    'globalThis.__ran1 = false; globalThis.__ran2 = false; setTimeout(function () { globalThis.__ran1 = true; setTimeout(function () { globalThis.__ran2 = true; }, 0); }, 0);',
    host,
  );
  assert.equal(vm.runInContext('globalThis.__ran1', host), false);
  assert.equal(vm.runInContext('__drainTimers__(10)', host), 2);
  assert.equal(vm.runInContext('globalThis.__ran1 && globalThis.__ran2', host), true);
}

{
  const host = createHost();
  loadTimeout(host);
  assert.equal(vm.runInContext('setInterval(function () {}, 10)', host), 0);
}

{
  const host = createHost();
  loadTimeout(host);
  vm.runInContext(
    'globalThis.__ran = false; globalThis.__id = setTimeout(function () { globalThis.__ran = true; }, 0); clearTimeout(globalThis.__id);',
    host,
  );
  assert.equal(vm.runInContext('__drainTimers__(10)', host), 0);
  assert.equal(vm.runInContext('globalThis.__ran', host), false);
}

console.log('timer queue: ok');
