# -*- coding: utf-8 -*-

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

import unittest

import django
from django.conf import settings
from mock import patch

from u1testutils.django import CsrfMiddlewareEnabledTestCase, patch_settings


class PatchSettingsTestCase(unittest.TestCase):

    def test_patch_settings_using_as_context_manager(self):
        assert not settings.DEBUG
        with patch_settings(DEBUG=True):
            self.assertTrue(settings.DEBUG)
        self.assertFalse(settings.DEBUG)

    def test_patch_settings_start_stop(self):
        assert not settings.DEBUG
        p = patch_settings(DEBUG=True)
        p.start()
        self.assertTrue(settings.DEBUG)
        p.stop()
        self.assertFalse(settings.DEBUG)

    def test_patch_settings_not_available_setting(self):
        marker = object()
        assert getattr(settings, 'NOT_AVAILABLE', marker) is marker
        with patch_settings(NOT_AVAILABLE=True):
            self.assertTrue(settings.NOT_AVAILABLE)
        self.assertIs(getattr(settings, 'NOT_AVAILABLE', marker), marker)


class CsrfMiddlewareEnabledTestCaseTestCase(unittest.TestCase):

    def setUp(self):
        p = patch_settings(MIDDLEWARE_CLASSES=[])
        p.start()
        self.addCleanup(p.stop)

        class CustomTestCase(CsrfMiddlewareEnabledTestCase):
            def runTest(self):
                # added fake runTest method to allow testcase initialization
                pass

        self.testcase = CustomTestCase()

    def test_csrf_middleware_django_13(self):
        with patch('u1testutils.django.django') as mock_django:
            mock_django.VERSION = (1, 3, 7)
            self.testcase.setUp()

        self.assertIn('django.contrib.csrf.middleware.CsrfMiddleware',
                      settings.MIDDLEWARE_CLASSES)
        self.assertNotIn('django.middleware.csrf.CsrfViewMiddleware',
                         settings.MIDDLEWARE_CLASSES)

    def test_csrf_middleware_django_15(self):
        with patch('u1testutils.django.django') as mock_django:
            mock_django.VERSION = (1, 5, 0)
            self.testcase.setUp()

        self.assertNotIn('django.contrib.csrf.middleware.CsrfMiddleware',
                         settings.MIDDLEWARE_CLASSES)
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware',
                      settings.MIDDLEWARE_CLASSES)

    def test_csrf_middleware(self):
        django13_csrf_middleware = \
            'django.contrib.csrf.middleware.CsrfMiddleware'
        django15_csrf_middleware = 'django.middleware.csrf.CsrfViewMiddleware'

        included = django13_csrf_middleware
        excluded = django15_csrf_middleware

        if django.VERSION[:2] > (1, 3):
            included, excluded = excluded, included

        self.testcase.setUp()

        self.assertIn(included, settings.MIDDLEWARE_CLASSES)
        self.assertNotIn(excluded, settings.MIDDLEWARE_CLASSES)
