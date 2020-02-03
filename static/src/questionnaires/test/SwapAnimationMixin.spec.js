import SwapAnimationMixin from '../SwapAnimationMixin'

describe('SwapAnimationMixin', () => {
  test('moveArrayElement moves an element to a given index', () => {
    const array = ['0', '1', '2', '3']
    SwapAnimationMixin.methods.moveArrayElement(array, 1, 3)
    expect(array).toEqual(['0', '2', '3', '1'])
  })

  test('moveArrayElement does nothing if fromIndex is out of bounds', () => {
    const array = ['0', '1', '2', '3']
    SwapAnimationMixin.methods.moveArrayElement(array, 4, 3)
    expect(array).toEqual(['0', '1', '2', '3'])
    SwapAnimationMixin.methods.moveArrayElement(array, -1, 3)
    expect(array).toEqual(['0', '1', '2', '3'])
  })

  test('moveArrayElement does nothing if toIndex is out of bounds', () => {
    const array = ['0', '1', '2', '3']
    SwapAnimationMixin.methods.moveArrayElement(array, 2, 4)
    expect(array).toEqual(['0', '1', '2', '3'])
    SwapAnimationMixin.methods.moveArrayElement(array, 2, -1)
    expect(array).toEqual(['0', '1', '2', '3'])
  })
})
