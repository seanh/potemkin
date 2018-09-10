"use strict";

window.addEventListener("load", function() {

  /**
   * Receive the LTI launch params over postMessage and construct and submit
   * the launch form.
   */
  window.addEventListener("message", function(message) {
    const form = document.getElementById("form");
    const params = JSON.parse(message.data);

    // The LTI launch URL isn't part of the form itself, it's the URL that the
    // form is submitted to.
    form.action = params.lti_launch_url;
    delete params.lti_launch_url;

    // Create the elements of the LTI launch form from the params received over
    // postMessage.
    for (const param in params) {
      const input = document.createElement("input");
      input.type = "text";
      input.name = param;
      input.value = params[param]
      form.appendChild(input);
    }

    // Automatically submit the form.
    form.submit();
  });

});
