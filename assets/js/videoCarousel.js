var tag = document.createElement('script');
tag.id = 'iframe-demo';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
	var elems1 = document.getElementsByClassName('yt-player');
	for(var i = 0; i < elems1.length; i++) {
		
		player = new YT.Player(elems1[i], {
			events: {
				//'onReady': onPlayerReady,
				'onStateChange': onPlayerStateChange
			}
		});
	}
}
function onPlayerReady(event) {
	
}
function handleVideo(playerStatus) {
$('.carousel').carousel('cycle');
	if (playerStatus == -1) {
		// unstarted
		$('#brc18-videos').slick('slickPause');
	} else if (playerStatus == 0) {
		// ended
		$('#brc18-videos').slick('slickPlay');
		$('#brc18-videos').carousel('cycle');
		
		
	} else if (playerStatus == 1) {
		// playing = green                
		$('#brc18-videos').slick('slickPause');                
	} else if (playerStatus == 2) {
		// paused = red
		$('#brc18-videos').slick('slickPlay');
	} else if (playerStatus == 3) {
		// buffering = purple
	} else if (playerStatus == 5) {
		// video cued
	}
}
function onPlayerStateChange(event) {
	if (event.data == YT.PlayerState.ENDED) {
	$('.carousel').carousel('cycle');
	}

	handleVideo(event.data);
}

$(function() {
	$('#brc18-videos').slick({
		slidesToShow: 1,
		slidesToScroll: 0,
		autoplay: true,
		autoplaySpeed: 3000,
		pauseOnFocus: false,
		pauseOnHover: false,
		dots: true,
		infinite: true,
		adaptiveHeight: true,
		arrows: false,
		modestbranding: 1,
		html5: 1,
		rel: 0
	});
	

});

$('#brc18-videos').on('beforeChange', function(event, slick, currentSlide, nextSlide){
	$('.yt-player').each(function(){
		this.contentWindow.postMessage('{"event":"command","func":"' + 'pauseVideo' + '","args":""}', '*')
	});
});

//IF DIRECTIONAL ARROWS ARE CLICKED, PAUSED VIDEO
$(".carousel-control", ".carousel-indicators").click(function() {
player.stopVideo();
$('.carousel').carousel('cycle');
});