// Control display of notices in the notice bar

const PAUSE_MS = 4000;
const FADE_MS = 500;
const INTERVAL_MS = 250;
const notices = $('#notice-bar .notice');
let ix = 0;
let next;
let changeNotice = false;

// console.log(notices.length + " notices to rotate");

const fadeAnimateNotices = () => {
  // console.log(`fadeAnimateNotices (ix = ${ix})`);
  const current = notices[ix];
  next = notices[ix + 1];

  // Defer cycle if user has just changed manually
  if ( changeNotice ) {
    // console.log("Deferring cycle due to user change");
    changeNotice = false;
    return setTimeout(fadeAnimateNotices, PAUSE_MS);
  }

  changeNotice = false;

  // Defer cycle if user is hovering
  if ( $('#notice-bar:hover').length || $('.notice-control:hover').length ) {
    // console.log("Deferring cycle due to mouse hover");
    // console.log("#notice-bar length: " + $('#notice-bar:hover').length);
    // console.log(".notice-control length: " + $('.notice-control:hover').length);
    return setTimeout(fadeAnimateNotices, PAUSE_MS);
  }

  if (ix + 1 >= notices.length) {
    // console.log("Reset notice ix")
    ix = -1;
    next = notices[0];
  } else if (ix < 0) {
    ix = notices.length - 1;
  }

  $(current).fadeOut(FADE_MS, () => {
    // console.log("Fading to notice " + (ix + 1));
    $(next).fadeIn(FADE_MS);
    setTimeout(fadeAnimateNotices, PAUSE_MS );
    ix++;
  });
};

// Debounce clicks to _moveNotice to prevent rapid clicking
const moveNotice = (d) => _.debounce(
    () => _moveNotice(d),
    FADE_MS,
    { 'leading': true, 'trailing': false },
)();

const _moveNotice = (direction) => {
  // console.log("MoveNotice " + direction);
  changeNotice = true;
  $(notices[ix]).fadeOut(150, () => {
    if (direction === 'left') {
      ix--;
    } else {
      ix++;
    }
    if (ix < 0) {
      ix = notices.length - 1;
    }
    if (ix > notices.length - 1) {
      ix = 0;
    }
    $(notices[ix]).fadeIn(100);
  });
}


// Make request for persistent (session) notice dismissal
const requestDismissNotice = (dtm) => fetch('/notice/dismiss', {
  method: 'POST',
  body: JSON.stringify({ datetime_modified: dtm }),
  headers: {
    'X-CSRFToken': Cookies.get('csrftoken'),
    'Content-Type': 'application/json',
  },
});


$(document).ready( () => {
  // Rotate low-priority notices
  notices.length > 1 && setTimeout(fadeAnimateNotices, PAUSE_MS);
})
