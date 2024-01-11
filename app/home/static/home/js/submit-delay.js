// Frontend logic for spam-filtering with a hidden input field

const initTime = new Date();

const setSubmitDelay = () => {
  const submitDelaySeconds = (new Date() - initTime) / 1000;
  const submitDelayInput = $(
    `<input
      type="hidden"
      name="submit_delay_seconds"
      value="${submitDelaySeconds}"
    >`);
  $('form').append(submitDelayInput);
}

$('form').submit(setSubmitDelay);
