import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const profileDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const fixturePath = path.join(profileDir, 'tests', 'fixtures', 'runtime-state-target.js');
const fixtureSource = fs.readFileSync(fixturePath, 'utf8');

function createWorld() {
  const context = vm.createContext({});
  context.globalThis = context;
  vm.runInContext(fixtureSource, context, { filename: 'runtime-state-target.js' });
  return context;
}

function call(context, tag, counter) {
  return vm.runInContext(
    `runtimeStateTarget.mint({ tag: ${JSON.stringify(tag)}, counter: ${JSON.stringify(counter)} })`,
    context,
  );
}

function passesProgression(values) {
  return values.every((value, index) => value === `page-${index + 1}:${index + 1}`);
}

const persistent = createWorld();
const persistentValues = [
  call(persistent, 'page-1', 0),
  call(persistent, 'page-2', 0),
];
assert.deepEqual(persistentValues, ['page-1:1', 'page-2:2']);
assert.equal(passesProgression(persistentValues), true);

const freshValues = [
  call(createWorld(), 'page-1', 0),
  call(createWorld(), 'page-2', 0),
];
assert.deepEqual(freshValues, ['page-1:1', 'page-2:1']);
assert.equal(passesProgression(freshValues), false);

// Resetting the visible counter does not recreate the hidden runtime state.
assert.equal(freshValues[1], 'page-2:1');
console.log('runtime state continuity: ok');
