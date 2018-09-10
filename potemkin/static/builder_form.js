"use strict";

window.addEventListener("load", function() {
  /**
   * Sign the LTI launch form when the Sign button is clicked.
   */
  function addSignButtonListener() {
    const signButton = document.getElementById("sign_button");
    signButton.addEventListener("click", function(event) {
      event.preventDefault();
      const form = document.getElementById("lti_launch_parameters");
      const formData = new FormData(form);
      const xhr = new XMLHttpRequest();
      xhr.open("POST", signButton.formAction);
      xhr.addEventListener("load", function() {
        form.oauth_signature.value = JSON.parse(this.responseText).oauth_signature;
      });
      const response = xhr.send(formData);
    });
  }

  addSignButtonListener();
});
