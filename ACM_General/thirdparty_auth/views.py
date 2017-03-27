from core.actions import is_valid_email
from django.conf import settings
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from accounts.models import User
import hashlib
import os
import requests
import json
import base64
# Create your views here.


###
# TODO: Modular Authentication with support for different protocols
#       As of right now the Views do not actually use the auth_backend
#       parameter.
###
class AuthorizationView(View):
    """
    @Desc: Default Social Authentication Class View which attempts to define
           the necessary elements for plug-and-play Social Authentication for
           any format.
    """
    http_method_names = ['get']

    def get(self, request, **kwargs):
        """
        @Desc: OAuth authorization processing and transaction handler.

        @Returns: Prepared GET/POST redirect to the OAuth authentication
                  endpoint.
        """

        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        auth_type = kwargs.get('auth_type', None)
        auth_provider = kwargs.get('auth_provider', None)
        try:
            auth_data=getattr(settings, 'SOCIAL_AUTH_CONFIG')[auth_type][auth_provider]
        except:
            auth_data=None

        if auth_data is not None:
            data = self.prepare_transaction(request, auth_data)
            request = requests.post(
                        'https://accounts.google.com/o/oauth2/v2/auth',
                        data=data
                      )

            return HttpResponseRedirect(request.url)
        else:
            raise Http404("Authentication type does not exist")

    @staticmethod
    def prepare_transaction(request, auth_data):
        """
        @Desc: Prepares the POST/GET request parameters for the initial
               authorization request for OAuth2. Also, Creates state comparator
               which ensures transaction integrity between the server and a
               specific client 'state'.

        @Returns: Returns a dictonary of the necessay POST/GET parameters
                  for an authorization request.
        """
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        request.session['state'] = state

        data = {
            'client_id': auth_data.get('client_id'),
            'response_type': 'code',
            'scope': 'openid email profile',
            'redirect_uri': auth_data.get('redirect_uri'),
            'state': state,
            'hd': 'mst.edu',
        }

        return data


class TokenView(View):
    """
    @Desc: Default Token Transaction View which handles the token OAuth
           transaction as well as User registration/login for each User
           authenticated
    """
    http_method_names = ['get']
    auth_type = 'oauth2'

    def get(self, request, **kwargs):
        """
        @Desc: Google Callback URL which takes the POST data from google,
               cleans the data to python datatypes, and creates/finds the user
               with the data.

               For furthur information, see Step 4 of:
               https://developers.google.com/identity/protocols/OpenIDConnect#server-flow
        """
        ###
        # Normalizing data from callback
        ###
        response_state=request.GET.get('state', None)

        try:
            session_state=request.session['state']
        except:
            session_state=None

        auth_type=kwargs.get('auth_type', None)
        auth_provider=kwargs.get('auth_provider', None)

        try:
            auth_data=getattr(settings, 'SOCIAL_AUTH_CONFIG')[auth_type][auth_provider]
        except:
            auth_data=None

        ###
        # Ensure state integrity of the user
        ###
        if response_state != session_state or response_state == None or session_state == None:
            raise Http404('Invalid Session State')

        if auth_data is None:
            raise Http404('Authentication Callback not found')

        payload = self.prepare_transaction(request, auth_data)
        ##
        # TODO: Automatically generate goopleapi link as may change in future.
        ##
        token_request = requests.post(
                            "https://www.googleapis.com/oauth2/v4/token",
                            data=payload
                       )
        if token_request.status_code == 200:
            cleaned_data = self.clean_jwt(token_request.text)
            return self.post_auth(request, cleaned_data)
        else:
            raise Http404("Invalid transaction as Google falied to send a JWT")

    @staticmethod
    def prepare_transaction(request, auth_data):
        """
        @Desc: Preparing the GET/POST data necessary to perform the Token
               Transaction.

        @Returns: Returns the GET/POST data necessary to perform the Token
                  Transaction.
        """
        code = request.GET.get('code')

        payload = {
            'code': code,
            'scope': '',
            'client_id': auth_data.get('client_id'),
            'client_secret': auth_data.get('client_secret'),
            'redirect_uri': auth_data.get('redirect_uri'),
            'grant_type': 'authorization_code',
        }

        return payload

    @staticmethod
    def clean_jwt(text):
        """
        @Desc: Transforms text containing a JSON Web Token into a cleaned
               python dictionary.

        @Returns: Returns the clean JSON Web Token as a python dictionary.
        """
        json_data = json.loads(text)
        jwt_segments = json_data['id_token'].split('.')
        user_data = base64.urlsafe_b64decode(jwt_segments[1] + "==")
        cleaned_user_data = json.loads(user_data.decode('utf-8'))

        return cleaned_user_data

    @staticmethod
    def post_auth(request, cleaned_data):
        """
        @Desc: Actions after the JSON Web Token has been cleaned and the rest
               of the transaction has been properly authenticated. Should be
               used to perform some post_auth action and then present some
               template/redirect.
        """
        email = cleaned_data.get('email', None)
        first_name = cleaned_data.get('given_name', None)
        last_name = cleaned_data.get('family_name', None)

        if(is_valid_email(email)):
            ##
            #TODO: Define get_or_create() in user manager
            ##
            User.objects.get_or_create(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user = authenticate(email=email)

        if user is not None:
            login(request, user)
        else:
            return HttpResponse('Error')

        return HttpResponseRedirect('/')
