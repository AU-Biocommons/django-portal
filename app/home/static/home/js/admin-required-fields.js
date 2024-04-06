// Mark required and optional fields in admin forms

const TAGS = ['input', 'textarea'];

($ => {
  $(document).ready( () => {

    TAGS.forEach( (tag) => {
      // Create a 'required' label to place beneath fields
      const margin = 10 + $(`${tag}[required]`).first().siblings('label').width();
      const label = tag === 'textarea' ?
        $(`<small style="color: #ffb042; line-height: 3; margin-left: ${margin}px;"><em>Required</em></small>`)
        : $('<small style="color: #ffb042; line-height: 3;"><em>Required</em></small>');

      // Append label to required elements for each tag
      $(`${tag}[required]`).after(label);
      $(`${tag}[required]`).after($('<br>')[0]);
    })
  });
})(django.jQuery);
