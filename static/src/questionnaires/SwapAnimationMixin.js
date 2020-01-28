/**
 * DON'T FORGET TO IMPORT THE CSS FILE : SwapAnimationMixin.js
 *
 * Helper for handling the animation when swapping two elements.
 * We call "selected element" the element that has been clicked to trigger the move. It should stay
 * in front during the animation.
 *
 * Step 0 : elements are originally like this :
 * <element 1>
 * <element 2>
 *
 * Step 1 : one element gets clicked. The positions are swapped by changing the underlying vuex
 * array, without any animation : (This step happens too fast to be seen by the user)
 * <element 2>
 * <element 1>
 *
 * Step 2 : the CSS animation is played : it changes the positions to the original ones (from step
 * 0), then slides them gradually to the new positions (from step 1).
 */
const questionSwapMixin = {
  methods: {
    // Move an element in an array from one index to the other.
    moveArrayElement(array, fromIndex, toIndex) {
      if (toIndex < 0 || toIndex > array.length - 1) {
        console.error('Cannot move the element to position', toIndex)
        return
      }
      if (fromIndex < 0 || fromIndex > array.length - 1) {
        console.error('Cannot move the element from position', fromIndex)
        return
      }
      const movingElement = array.splice(fromIndex, 1)[0]
      array.splice(toIndex, 0, movingElement)
    },
    // For the swapping animation, set the distance that each element should travel, in the CSS
    // sheet.
    _setAnimationDistances({ selectedElementDistancePx, neighborElementDistancePx }) {
      const getStyleSheet = () => {
        for (let i = 0; i < document.styleSheets.length; i++) {
          const sheet = document.styleSheets[i]
          if (sheet.href && sheet.href.includes('questionnaire-create')) {
            return sheet
          }
        }
      }
      const getAnimationRule = (sheet, ruleName) => {
        for (let i = 0; i < sheet.cssRules.length; i++) {
          if (sheet.cssRules[i].name && sheet.cssRules[i].name === ruleName) {
            return sheet.cssRules[i]
          }
        }
      }
      const setSelectedElementDistance = (sheet, ruleName, distancePx) => {
        const rule = getAnimationRule(sheet, ruleName)
        rule.cssRules[0].style.setProperty('transform', 'translateY(' + distancePx + 'px)')
      }

      const sheet = getStyleSheet()
      setSelectedElementDistance(sheet, 'moveSelectedElement', selectedElementDistancePx)
      setSelectedElementDistance(sheet, 'moveNeighborElement', neighborElementDistancePx)
    },
    // Given two jquery dom elements', find the distances that they need to move for the swap.
    _computeSwapDistances(fromElement, toElement) {
      const from = {
        top: fromElement[0].getBoundingClientRect().top + window.scrollY,
        bottom: fromElement[0].getBoundingClientRect().bottom + window.scrollY,
      }
      const to = {
        top: toElement[0].getBoundingClientRect().top + window.scrollY,
        bottom: toElement[0].getBoundingClientRect().bottom + window.scrollY,
      }
      if (from.top < to.top) {
        // Selected element is moving down
        return {
          selectedElementDistancePx: from.bottom - to.bottom,
          neighborElementDistancePx: to.top - from.top,
        }
      } else {
        // Selected element is moving up
        return {
          selectedElementDistancePx: from.top - to.top,
          neighborElementDistancePx: to.bottom - from.bottom,
        }
      }
    },
    _runAnimation(jQueryElement, animationClass) {
      // Setup listener to remove the animation class once the animation is done.
      jQueryElement.on(
        'animationend msAnimationEnd webkitAnimationEnd oanimationend',
        function() {
          $(this).removeClass(animationClass)
        },
      )
      // Add the animation class to start the animation
      jQueryElement.addClass(animationClass)
    },
    // Run the animation for when two questions have been swapped. This should be run after the
    // state has been modified in vuex.
    animateQuestionSwap(fromElement, toElement, isMoveUp) {
      const distances = this._computeSwapDistances(fromElement, toElement)
      this._setAnimationDistances(distances)

      this._runAnimation(fromElement, 'move-neighbor')
      this._runAnimation(toElement, 'move-selected')
    },
  },
}

export default questionSwapMixin
