(() => {
  // The hidden sequence models closure/module state that is not present in the
  // explicit input. A browser-shaped caller expects one world across calls.
  let hiddenSequence = 0;

  globalThis.runtimeStateTarget = {
    mint(input) {
      if (!input || typeof input.tag !== 'string') {
        throw new TypeError('tag is required');
      }
      hiddenSequence += 1;
      return `${input.tag}:${hiddenSequence}`;
    },
  };
})();
