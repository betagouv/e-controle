
export default {
  assertHasEmmitted: function(obj, eventName, numTimes) {
    expect(obj.emitted()).toHaveProperty(eventName)
    expect(obj.emitted()[eventName].length).toEqual(numTimes)
  },
  assertNothingEmitted: function(obj) {
    expect(obj.emitted()).toEqual({})
  },
}