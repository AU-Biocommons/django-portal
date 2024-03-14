// Add markdown editor to the "body" field in django admin

(function($) {
  $(document).ready( () => {
    new SimpleMDE({
      element: document.getElementById("id_body_markdown")
    });
  });
})(django.jQuery);
