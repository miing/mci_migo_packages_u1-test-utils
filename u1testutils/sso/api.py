# Copyright 2012, 2013 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from ssoclient.v2 import V2ApiClient

from u1testutils.sso import environment


class APIClient(object):
    """API client helper for identity tests."""

    def __init__(self, sso_server_url=None):
        sso_server_url = self._get_sso_server_url(sso_server_url)
        self.client = V2ApiClient(sso_server_url + '/api/v2')

    def _get_sso_server_url(self, sso_server_url=None):
        if sso_server_url is None:
            sso_server_url = environment.get_sso_base_url()
        else:
            sso_server_url = sso_server_url.rstrip('/')
        return sso_server_url

    def get_account_openid(self, email, password, token_name):
        response = self.client.login(
            email=email, password=password, token_name=token_name)
        data = response.json()
        openid = data.get('consumer_key')
        return openid

    def create_new_account(self, user, captcha_id=None, captcha_solution=None):
        data = dict(
            email=user.email,
            password=user.password,
            displayname=user.full_name
        )
        if captcha_id is not None:
            data['captcha_id'] = captcha_id
        if captcha_solution is not None:
            data['captcha_solution'] = captcha_solution
        response = self.client.register(data)
        return response.status_code == 201
