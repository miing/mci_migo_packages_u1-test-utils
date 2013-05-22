# Copyright 2013 Canonical Ltd.
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
# with this program.  If not, see <http://www.gnu.org/licenses/

import mock

import u1testutils.logging
from u1testutils.sso.sst import pages


class LogInFromRedirectTestCase(u1testutils.logging.LogHandlerTestCase):

    def test_site_without_rpconfig(self):
        with mock.patch.object(pages.LogInFromRedirect, 'assert_page_is_open'):
            page = pages.LogInFromRedirect()

        with mock.patch('sst.actions.get_elements') as mock_elements:
            mock_elements.return_value = []
            headings2 = ['Log in to Ubuntu Single Sign On', 'Are you new?']
            for heading in headings2:
                mock_heading_element = mock.Mock()
                mock_heading_element.text = heading
                mock_elements.return_value.append(mock_heading_element)
            with self.assertRaises(AssertionError):
                page.assert_headings2()
        self.assertLogLevelContains(
            'ERROR',
            'Please check that you are logging in from a server with '
            'an rpconfig on SSO. Otherwise, the headings in the page '
            'will not be the ones we expect.')
