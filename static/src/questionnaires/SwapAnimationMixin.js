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
    setAnimationDistance({ slideUpDistancePx, slideDownDistancePx }) {
      const getStyleSheet = () => {
        for (let i = 0; i < document.styleSheets.length; i++) {
          const sheet = document.styleSheets[i]
          if (sheet.href && sheet.href.includes('questionnaire-create')) {
            return sheet
          }
        }
      }
      const getAnimationRule = (sheet, ruleName) => {
        for (let i = 0; i < sheet.rules.length; i++) {
          if (sheet.rules[i].name && sheet.rules[i].name === ruleName) {
            return sheet.rules[i]
          }
        }
      }
      const setDistanceFrom = (rule, distancePx) => {
        const fromRule = rule.cssRules[0]
        fromRule.style.setProperty('transform', 'translateY(' + distancePx + 'px)')
      }
      const setSlideUpDistance = (sheet, distancePx) => {
        const rule = getAnimationRule(sheet, 'slideUp')
        setDistanceFrom(rule, -1 * distancePx)
      }
      const setSlideDownDistance = (sheet, distancePx) => {
        const rule = getAnimationRule(sheet, 'slideDown')
        setDistanceFrom(rule, distancePx)
      }
      const sheet = getStyleSheet()
      setSlideUpDistance(sheet, slideUpDistancePx)
      setSlideDownDistance(sheet, slideDownDistancePx)
    },
    // Run the animation for when two questions have been swapped. This should be run after the
    // state has been modified in vuex.
    animateQuestionSwap(themeIndex, fromQIndex, toQIndex) {
      if (fromQIndex === toQIndex) {
        console.error('Cannot swap question with itself! ', fromQIndex)
        return
      }

      const runAnimation = (jQuerySelector, animationClass) => {
        // Setup listener to remove the animation class once the animation is done.
        $(jQuerySelector).on(
          'animationend msAnimationEnd webkitAnimationEnd oanimationend',
          function() {
            $(this).removeClass(animationClass)
            $(this).css('z-index', 'auto')
            $(this).removeClass('bg-azure-lightest')
          },
        )
        // Add the animation class to start the animation
        $(jQuerySelector).addClass(animationClass)
      }

      if (fromQIndex > toQIndex) {
        // Selected question moves upwards
        runAnimation('#theme-' + themeIndex + '-question-' + fromQIndex, 'move-up')
        runAnimation('#theme-' + themeIndex + '-question-' + toQIndex, 'move-down')
      } else {
        // Selected question moves downwards
        runAnimation('#theme-' + themeIndex + '-question-' + toQIndex, 'move-up')
        runAnimation('#theme-' + themeIndex + '-question-' + fromQIndex, 'move-down')
      }
      // Display selected question on top during movement
      $('#theme-' + themeIndex + '-question-' + toQIndex).css('z-index', '999')
      $('#theme-' + themeIndex + '-question-' + toQIndex).addClass('bg-azure-lightest')
    },
  },
}

export default questionSwapMixin
