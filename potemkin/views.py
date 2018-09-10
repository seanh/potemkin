from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults

import oauthlib.oauth1
import oauthlib.common
import webob

import potemkin.models as models


@view_defaults(route_name="install", renderer="templates/install.html.jinja2")
class InstallViews:
    """Views for the page with the "Install LTI App" form."""
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        return {}

    @view_config(request_method="POST")
    def post(self):
        application_instance = models.ApplicationInstance(
            name=self.request.params["name"],
            launch_url=self.request.params["launchURL"],
            consumer_key=self.request.params["consumerKey"],
            shared_secret=self.request.params["sharedSecret"],
        )
        self.request.db.add(application_instance)
        self.request.session.flash(
            f'Application instance "{application_instance.name}" installed.',
            queue="install",
        )
        return {}


class LaunchViews:
    """Views for the "LTI Launch" page.

    The LTI launch page is somewhat complicated. It's composed of four
    different views, most of which have their own templates:

    1. The "iframe" view is the "root" or "top" view of the page. It renders an
       HTML page containing an <iframe>.

    2. The "builder_form" view is what gets rendered inside the <iframe>. It's
       a great big HTML form that the user fills out to specify what kind of
       LTI launch they want to do.

       Although this form contains all the LTI launch parameters it's *not*
       actually an LTI launch form - it also contains some parameters that
       aren't part of the LTI launch. For example the URL that the LTI launch
       form will be submitted to is a parameter of this form. So is the shared
       secret that'll be used to sign the LTI launch request.

       The user submits this form back *to Potemkin* and Potemkin uses it
       generate n launch form that auto-submits itself to the LTI app's launch
       URL.

    3. The "launch_form" view is the view that receives submissions of the
       builder form and renders a self-submitting launch form.

       There's no view for receiving submissions of the launch form - those
       aren't received by this app, they're sent to the LTI app that's being
       tested.

       The browser renders the response from the LTI app inside the <iframe>
       that previously contained the launch form (and before that the builder
       form).

    4. The "sign" view is used for signing the LTI launch form.

       We want the user to be able to send whatever OAuth signature they want
       to the LTI app in the launch request - a valid signature or an invalid
       one. So the OAuth signature is a field in the builder form - the user
       can enter whatever they want into this field and we'll add that to the
       launch request as the OAuth signature, or they can leave it blank to
       submit an unsigned request.

       We want to make it easy for the user to generate a valid signature of
       the field values they've entered too, so the builder form contains a
       Sign button that does an AJAX request to the sign view to get a valid
       signature over the form and add it into the signature field.

    """
    def __init__(self, request):
        self.request = request

    @view_config(route_name="launch", request_method="GET", renderer="templates/launch/iframe.html.jinja2")
    def iframe(self):
        """Render the parent page containing the <iframe>."""
        return {}

    @view_config(route_name="launch_form", request_method="GET", renderer="templates/launch/builder_form.html.jinja2")
    def builder_form(self):
        """Render the builder form."""
        # We're gonna use an OAuth 1 client object to generate the initial
        # values for the OAuth 1 nonce and timestamp fields. To do so we need
        # to specify a fake client key and URL.
        # There's probably an easier way to do this.
        oauth_params = dict(oauthlib.oauth1.Client("foo").get_oauth_params(oauthlib.common.Request("foo")))

        # These are the initial values for some of the form fields.
        # Other fields have their initial values hard-coded in the
        # builder_form.html.jinja2 template.
        fields = {
            "oauth_nonce": oauth_params["oauth_nonce"],
            "oauth_timestamp": oauth_params["oauth_timestamp"],
        }

        return fields

    @view_config(route_name="launch_form", request_method="POST", renderer="templates/launch/launch_form.html.jinja2")
    def launch_form(self):
        """Receive a builder form post and render the launch form.

        The user submits the builder form to Potemkin and based on the
        submitted builder form params Potemkin renders an LTI launch form that
        automatically submits itself to the LTI app.

        """
        # Make a copy of the request params so we can modify it.
        params = webob.multidict.MultiDict(self.request.params)

        # These fields aren't part of the LTI launch form so remove them.
        lti_launch_url = params.pop("lti_launch_url")
        oauth_shared_secret = params.pop("oauth_shared_secret")

        return {
            "lti_launch_url": lti_launch_url,
            "params": params,
        }

    @view_config(route_name="launch_sign", request_method="POST", renderer="json")
    def sign(self):
        """Return a valid OAuth 1 signature for the launch form."""
        # Make a copy of the request params so we can modify it.
        params = webob.multidict.MultiDict(self.request.params)

        # These fields aren't part of the LTI launch form so remove them.
        lti_launch_url = params.pop("lti_launch_url")
        oauth_shared_secret = params.pop("oauth_shared_secret")

        oauth_client = oauthlib.oauth1.Client(params["oauth_consumer_key"],
                                              oauth_shared_secret)
        oauth_signature = oauth_client.get_oauth_signature(
            oauthlib.common.Request(
                lti_launch_url,
                http_method="POST",
                body=params,
            )
        )
        return dict(oauth_signature=oauth_signature)


@view_config(route_name="index", request_method="GET")
def index(request):
    raise HTTPFound(location=request.route_url("launch"))
