import time

from pyramid.view import view_config
import oauthlib.oauth1
import oauthlib.common
import webob


ONE_YEAR = 60 * 60 * 24 * 365
"""One year in seconds."""


@view_config(
    route_name="launch",
    request_method="GET",
    renderer="templates/launch/index.html.jinja2",
)
def launch(request):
    """Render the main page where you construct and execute LTI launches."""

    # We're gonna use an OAuth 1 client object to generate the initial
    # values for the OAuth 1 nonce and timestamp fields. To do so we need
    # to specify a fake client key and URL.
    # FIXME: There's probably an easier way to do this.
    #
    # Use an OAuth 1 timestamp a full year in the future, so that it doesn't
    # expire while the developer is still trying to use it. (This isn't good
    # security but that's not a problem for this app.)
    timestamp = str(int(time.time() + ONE_YEAR))
    oauth_params = dict(
        oauthlib.oauth1.Client("fake_client_key", timestamp=timestamp).get_oauth_params(
            oauthlib.common.Request("https://example.com")
        )
    )

    # These are the initial values for some of the form fields.
    # Other fields have their initial values hard-coded in the
    # template file.
    return {
        "oauth_nonce": oauth_params["oauth_nonce"],
        "oauth_timestamp": oauth_params["oauth_timestamp"],
    }


@view_config(
    route_name="launch_form",
    request_method="GET",
    renderer="templates/launch/launch_form.html.jinja2",
)
def launch_form(request):
    """Render the actual LTI launch form."""
    return {}


@view_config(route_name="launch_sign", request_method="POST", renderer="json")
def sign(request):
    """Return a valid OAuth 1 signature for the launch form."""
    # Make a copy of the request params so we can modify it.
    params = webob.multidict.MultiDict(request.params)

    # These fields aren't part of the LTI launch form so remove them.
    lti_launch_url = params.pop("lti_launch_url")
    oauth_shared_secret = params.pop("oauth_shared_secret")

    oauth_client = oauthlib.oauth1.Client(
        params["oauth_consumer_key"], oauth_shared_secret
    )
    oauth_signature = oauth_client.get_oauth_signature(
        oauthlib.common.Request(lti_launch_url, http_method="POST", body=params)
    )
    return dict(oauth_signature=oauth_signature)
