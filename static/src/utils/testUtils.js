
const assertNotEmitted = (obj, eventName) => {
  expect(obj.emitted()).not.toHaveProperty(eventName)
}

const assertHasEmmitted = (obj, eventName, numTimes) => {
  if (numTimes === 0) {
    return assertNotEmitted(obj, eventName)
  }
  expect(obj.emitted()).toHaveProperty(eventName)
  expect(obj.emitted()[eventName]).toHaveLength(numTimes)
}

const assertNothingEmitted = function(obj) {
  expect(obj.emitted()).toEqual({})
}

const assertLastEmit = (obj, eventName, emittedObject) => {
  expect(obj.emitted()).toHaveProperty(eventName)
  expect(obj.emitted()[eventName][0][0]).toEqual(emittedObject)
}

const isModalShowing = function(wrapper, elementId) {
  return wrapper.find(elementId).classes('show')
}

export default {
  assertHasEmmitted: assertHasEmmitted,
  assertLastEmit: assertLastEmit,
  assertNotEmitted: assertNotEmitted,
  assertNothingEmitted: assertNothingEmitted,
  isModalShowing: isModalShowing,
}
