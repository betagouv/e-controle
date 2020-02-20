const ANIMATION_DURATION_SECONDS = 1

export default {
  methods: {
    swapMixin_moveItemUp(array, index, selectedJqueryElement) {
      if (index <= 0) {
        console.error('Cannot moveItemUp from index', index)
        return
      }
      this.$_swapMixin_swapItems(array, index, index - 1, selectedJqueryElement)
      this.swapMixin_updateOrderFields(array)
    },
    swapMixin_moveItemDown(array, index, selectedJqueryElement) {
      if (index >= (array.length - 1)) {
        console.error('Cannot moveItemDown from index', index)
        return
      }
      this.$_swapMixin_swapItems(array, index, index + 1, selectedJqueryElement)
    },
    $_swapMixin_swapItems(array, indexFrom, indexTo, selectedJqueryElement) {
      // Set CSS class on the moving element
      selectedJqueryElement.addClass('selected')
      setTimeout(
        () => {
          selectedJqueryElement.removeClass('selected')
        },
        ANIMATION_DURATION_SECONDS * 1000)

      // Move the elements in the vuex array
      const movingElement = array.splice(indexFrom, 1)[0]
      array.splice(indexTo, 0, movingElement)
    },
    // For all items in array, set the 'order' field to match with the
    // order in the array.
    swapMixin_updateOrderFields(array) {
      array.map((item, index) => {
        item.order = index
      })
    },
  },
}
