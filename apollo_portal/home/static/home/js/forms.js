// Generic forms logic

$(document).ready(scrollToErrors);

function scrollToErrors() {
  const errors = $('.errorlist');
  if (errors.length) {
    const top = errors.offset().top;
    $('html, body').animate({scrollTop: top - 80}, 500);
  }
}

// $('form').submit( () => {
//   $('button[type="submit"]').prop('disabled', true);
//   $('button[type="submit"]').html('<i class="fas fa-sync-alt fa-spin"></i>');
// });
