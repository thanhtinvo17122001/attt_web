$(document).ready(function () {
  $('.toggle-menu').on('click', function() {
    $('.header').css('display', 'block');
    $('.header-overlay').css('display', 'block');
    $('html, body').css({
      overflow: 'hidden',
        height: '100%'
    });
  })
  function closeMenu() {
    $('.header').css('display', 'none');
    $('.header-overlay').css('display', 'none');
    $('html, body').css({
        overflow: 'auto',
        height: 'auto'
    });
  }
  $('.header-overlay').on('click', function() {
    closeMenu();
  })
  $('.close-menu').on('click', function(e) {
    e.preventDefault();
    closeMenu();
  })
});