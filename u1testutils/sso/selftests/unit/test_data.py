# -*- coding: utf-8 -*-

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
# with this program.  If not, see <http://www.gnu.org/licenses/

import unittest

from mock import patch

import u1testutils.django
from u1testutils.sso import api, data


class DataTestCase(unittest.TestCase):

    def test_make_unique_user(self):
        user = data.User.make_unique(unique_id='test_uuid')

        self.assertEqual(user.full_name, 'Test user test_uuid')
        self.assertEqual(user.email, 'test+test_uuid@example.com')
        self.assertEqual(user.password, 'Hola123*')

    def test_make_exising_user_from_configuration(self):
        with u1testutils.django.patch_settings(
                SSO_TEST_ACCOUNT_FULL_NAME='Test existing name',
                SSO_TEST_ACCOUNT_EMAIL='existingemail@example.com',
                SSO_TEST_ACCOUNT_PASSWORD='existing password'):
            user = data.User.make_from_configuration()

        self.assertEqual(user.full_name, 'Test existing name')
        self.assertEqual(user.email, 'existingemail@example.com')
        self.assertEqual(user.password, 'existing password')

    def test_make_new_user_from_configuration(self):
        with u1testutils.django.patch_settings(
                EMAIL_ADDRESS_PATTERN='newemail+%s@example.com',
                SSO_TEST_ACCOUNT_PASSWORD='new password'):
            user = data.User.make_from_configuration(
                new_user=True, unique_id='test_uuid')

        self.assertEqual(user.full_name, 'Test user test_uuid')
        self.assertEqual(user.email, 'newemail+test_uuid@example.com')
        self.assertEqual(user.password, 'new password')


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.user = data.User.make_from_configuration()

    def test_default_openid(self):
        self.assertIsNone(self.user._openid)

    def test_openid_for_valid_account(self):
        with patch.object(api.APIClient, 'get_account_openid') as mock_open_id:
            mock_open_id.return_value = 'foo1234'

            self.assertEqual(self.user.openid, 'foo1234')
            self.assertEqual(self.user._openid, 'foo1234')

    def test_openid_for_invalid_account(self):
        with patch.object(api.APIClient, 'get_account_openid') as mock_open_id:
            mock_open_id.return_value = None

            self.assertEqual(self.user.openid, None)
            self.assertIsNone(self.user._openid, None)
