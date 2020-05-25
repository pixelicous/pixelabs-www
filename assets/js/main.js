
function colorful_full_screen() {

  // var psychedelic_enabled = document.getElementById("pschedelic_gallery")

  // if ( psychedelic_enabled.checked) {

    var photo = document.getElementsByTagName('img');
  
    const COLORS = [
      'purple',
      'green',
      'red',
    ];
  
    var duotoneColor = COLORS[Math.floor(Math.random() * COLORS.length)]
    var duotheme = photo.dataset.duotheme;
    photo.dataset.duotheme = duotoneColor;
  // }
}

$( document ).ready(function() {
  "use strict"; // Start of use strict

  document.getElementById("pschedelic_gallery").onclick = function () {
    var photos = document.querySelectorAll('[id^=color-gallery]');

    for(var i in photos) {
      
      if ( this.checked ) {
        const COLORS = [
          'purple',
          'green',
          'red',
        ];
        var duotoneColor = COLORS[Math.floor(Math.random() * COLORS.length)]
      }
      else {
        var duotoneColor = 'blackWhite'
      }

      var duotheme = photos[i].dataset.duotheme;
      photos[i].dataset.duotheme = duotoneColor;
  }
  }

  // Change gallery thumbnails to colorful randomness in case IDed that way

  // var fruitCount = plant.getAttribute('data-fruit'); // fruitCount = '12'

  // $('#color-gallery').each(function() {
  //   var number = this.id.split('_').pop();
  //   var randomColor = COLORS[Math.floor(Math.random() * COLORS.length)];
  //   this.duotone-theme = randomColor;
  // });



  $(window).scroll(function() {
    var height = $(this).scrollTop();
    if (height > 100) {
        $('.scroll-to-top').fadeIn();
    } else {
        $('.scroll-to-top').fadeOut();
    }
  });

    // Collapse Navbar
    var navbarCollapse = function () {
      if ($("#mainNav").offset().top > 100) {
          $("#mainNav").addClass("navbar-shrink");
      } else {
          $("#mainNav").removeClass("navbar-shrink");
      }
  };

  //var colors = ['red', 'blue', 'green', 'gray', 'black', 'yellow'];

  // $(document).ready(function(){
     
  // });

  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);
  
})(jQuery);

// $(pschedelic_gallery).click(function() {
  
//   "use strict"; // Start of use strict

// var photos = document.querySelectorAll('[id^=color-gallery]');
// var randomColor = 'gold';

// for(var i in photos){
//   var randomColor = COLORS[Math.floor(Math.random() * COLORS.length)]
//   var duotheme = photos[i].dataset.duotheme;
//   photos[i].dataset.duotheme = randomColor;
// }

// })(jQuery);