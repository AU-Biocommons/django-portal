// Generic forms logic

$(document).ready(scrollToErrors);

function scrollToErrors() {
  const errors = $('.errorlist');
  if (errors.length) {
    const top = errors.offset().top;
    $('html, body').animate({scrollTop: top - 80}, 500);
  }
}


$(document).ready(function() {
  $('label').each( (i, label) => {
    // Add * char to required labels
    if (
      $(label).siblings('input')
        .not('[type="radio"], [type="checkbox"]')
        .attr('required')
      || $(label).siblings('textarea')
        .attr('required')
    ) {
      const html = $(label).html() + '&nbsp;*';
      $(label).html(html);
    }
  })
});

$('form').submit( () => {
  const hard_width = $('button[type="submit"]').outerWidth();
  $('button[type="submit"]').prop('disabled', true);
  $('button[type="submit"]').css('min-width', hard_width);
  $('button[type="submit"]').html('<i class="fas fa-sync-alt fa-spin"></i>');
});
