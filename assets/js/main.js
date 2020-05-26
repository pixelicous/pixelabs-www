function return_random_color() {
  const COLORS = [
    'purple',
    'green',
    'red',
    'blue',
    'vintage',
  ];

  do {
    var duotoneColor = COLORS[Math.floor(Math.random() * COLORS.length)];
  }
  while (duotoneColor == window.last_color)
  window.last_color = duotoneColor;
  return duotoneColor
}

function colorful_full_screen(currentIndex) {

  // var psychedelic_enabled = document.getElementById("pschedelic_gallery")

  // if ( psychedelic_enabled.checked) {

    var photo = document.querySelectorAll('[id^=fullsize_gallery]');
      photo[0].setAttribute('data-duotheme', return_random_color());
    //}
}

jQuery(document).ready(function() {
  "use strict"; // Start of use strict

  document.getElementById("pschedelic_gallery").onclick = function () {
    // query html galleries for this id, color effects will be enabled on those photos
    var photos = document.querySelectorAll('[id^=color-gallery]');
    if ( this.checked ) {
      window.fullsize_class_name = "fullsize_colorful"
    }
    else {
      window.fullsize_class_name = "baguetteBox-open"
    }

    // reset baguettebox to reset bodyclass - todo: simplify bodyclass variable refresh
    baguetteBox.run('.photo_gallery', {
      fullScreen: false,
      preload: 2,
      bodyClass: fullsize_class_name,
      //animation: 'fadeIn',
      overlayBackgroundColor: 'rgba(255, 255, 255 , 0.8)',
      //onChange: colorful_full_screen,
    });


    for (let i = 0; i < photos.length; i++) {
      var photo_object = photos[i];

      // if psy input button is checked (detected above)
      if ( this.checked ) {
        // get random color from list
        var duotoneColor = return_random_color()
      }
      else {
        // specific bw dataset if not psy gallery not requested
        var duotoneColor = 'blackWhite'
      }

      // todo: fix console errors
      photo_object.setAttribute('data-duotheme', duotoneColor);
  }
  }
  
});