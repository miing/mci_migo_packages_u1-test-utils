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

from __future__ import absolute_import

import sst.actions

from django.conf import settings


def get_sso_base_url(default='http://localhost:8000'):
    base_url = getattr(settings, 'OPENID_SSO_SERVER_URL', default).rstrip('/')
    return base_url


# this is a temporarly helper so we can detect brands at UI rendering time
# since we can not access flags properly from within the acceptance run
def get_current_brand():
    try:
        sst.actions.get_element_by_css('*[data-qa-id="brand_ubuntuone"]')
    except:
        pass
    else:
        return 'ubuntuone'

    try:
        sst.actions.get_element_by_css('*[data-qa-id="brand_launchpad"]')
    except:
        pass
    else:
        return 'launchpad'

    # if all the above failed, the following must succeed
    sst.actions.get_element_by_css('*[data-qa-id="brand_ubuntu"]')
    return 'ubuntu'
