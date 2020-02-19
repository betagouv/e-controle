export default {
  methods: {
    stickyBottom_makeStickyBottom(elementId, bottomOffsetPx) {
      const stickySupport = this.stickyBottom_isPositionStickySupported()
      console.log('stickySupport', stickySupport)

      if (!stickySupport) {
        this.stickyBottom_makeStickyByHand(elementId, bottomOffsetPx)
      }
    },
    stickyBottom_isPositionStickySupported() {
      const prefix = ['', '-o-', '-webkit-', '-moz-', '-ms-']
      const test = document.head.style

      for (let i = 0; i < prefix.length; i += 1) {
        test.position = `${prefix[i]}sticky`
      }

      return test.position === 'sticky'
    },
    stickyBottom_makeStickyByHand(elementId, bottomOffsetPx) {
      const element = document.getElementById(elementId)
      const elementHeightPx = element.offsetHeight

      // Create a placeholder element of the same height as the fixed element.
      const placeholderElement = document.createElement('div')
      $(placeholderElement).css('min-height', elementHeightPx + 'px')
      element.parentNode.insertBefore(placeholderElement, element)

      // Position the element on top of the placeholder.
      const stickyMenu = $('#' + elementId)
      stickyMenu.css('position', 'absolute')
      stickyMenu.css('bottom', bottomOffsetPx + 'px')
      stickyMenu.css('z-index', 1020)

      // Depending on how far we have scrolled, position the element fixed or absolute.
      const positionElement = () => {
        const scrollDistance = $(document).scrollTop()
        const viewPortHeight = $(window).height()
        const stickyMenu = $('#' + elementId)
        if ((scrollDistance + viewPortHeight) <= ($(document).height() - bottomOffsetPx)) {
          stickyMenu.css('position', 'fixed')
          stickyMenu.css('bottom', '0')
        } else {
          stickyMenu.css('position', 'absolute')
          stickyMenu.css('bottom', bottomOffsetPx + 'px')
        }
      }

      // Listen to scroll event, to reposition element all the time.
      $(document).scroll(positionElement)

      // Trigger the positioning every so often.
      // Ideally we would want to trigger only when the document height changes, but we don't have
      // an easy way to do that.
      const repositionPeriodMs = 300
      setInterval(positionElement, repositionPeriodMs)
    },
  },
}
