"use strict";

window.addEventListener("load", function() {

  /**
   * Fill in the signature field when the Sign button is clicked.
   */
  document.getElementById("signButton").addEventListener("click", function(event) {
    event.preventDefault();
    const form = getBuilderForm();
    const formData = new FormData(form);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", signButton.formAction);
    xhr.addEventListener("load", function() {
      form.oauth_signature.value = JSON.parse(this.responseText).oauth_signature;
    });
    const response = xhr.send(formData);
  });

  /**
   * Send a postMessage command to launch the LTI app when the Launch button is
   * clicked.
   */
  document.getElementById("launchButton").addEventListener("click", function(event) {
    event.preventDefault();

    const params = launchParams();

    // Replace the iframe that the app is launched in with a new one.
    // This is to enable re-launching the app by clicking the Launch button
    // again, without reloading the page: the iframe needs to be reset before
    // the app can be re-launched.
    const newIFrame = document.createElement("iframe");
    newIFrame.id = "iframe";
    newIFrame.src = "http://localhost:6543/launch/form";  // FIXME: Don't hardcode Potemkin's own URL here.
    newIFrame.classList.add("iframe");
    const oldIFrame = document.getElementById("iframe");
    oldIFrame.parentNode.replaceChild(newIFrame, oldIFrame);

    newIFrame.contentWindow.addEventListener("load", function() {
      newIFrame.contentWindow.postMessage(
        JSON.stringify(params),
        "http://localhost:6543",  // FIXME: Don't hardcode Potemkin's own origin here.
      );
    });
  });

  /**
   * Return all the LTI launch params from the builder form.
   */
  function launchParams() {
    const form = getBuilderForm();
    const params = {};
    for (let i = 0; i< form.elements.length; i++) {
      const element = form.elements[i];

      if (element.type === "fieldset") {
        continue;
      }

      // The shared secret is used to sign the form but isn't itself submitted
      // as a parameter in the form. Remove it.
      if (element.name === "oauth_shared_secret") {
        continue;
      }

      params[element.name] = element.value;
    }
    return params;
  }

  /**
   * Return the builder form.
   */
  function getBuilderForm() {
    return document.getElementById("builder-form");
  }
});
