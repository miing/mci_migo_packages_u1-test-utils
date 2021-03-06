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

import socket
import threading
import time
import unittest

import localmail
import localmail.tests.helpers
from django.conf import settings

from u1testutils import mail


class MailTestCase(unittest.TestCase):

    SMTP_PORT = 2025

    @classmethod
    def setUpClass(class_):
        class_.localmail_thread = threading.Thread(
            target=localmail.run, args=(class_.SMTP_PORT, settings.IMAP_PORT))
        # Avoid hanging the main process when something goes wrong
        class_.localmail_thread.daemon = True
        class_.localmail_thread.start()
        # There is a race here as there is no (easy, that I know of) way to
        # guarantee that the server has reached the point that it is listening
        # to the socket. This leads to conection errors in these cases.  So the
        # workaround is to... sleep :-/ The proper way to handle this would be
        # to add an Event() in the server that can be waited on in the client
        # (or any other sync mechanism including making sure run() blocks until
        # the listen calls have been really executed) -- vila 2013-05-22
        time.sleep(0.1)
        # Try the port to make sure the server started.
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_.settimeout(10)
        socket_.connect(('localhost', class_.SMTP_PORT))
        socket_.close()

    @classmethod
    def tearDownClass(class_):
        localmail.shutdown_thread(class_.localmail_thread)

    def test_get_latest_email(self):
        from_ = 'from@example.com'
        to = 'to@example.com'
        subject = 'Test Subject'
        body = 'Test body'
        with localmail.tests.helpers.SMTPHelper(port=self.SMTP_PORT) as smtp:
            smtp.login()
            smtp.send(from_, to, subject, body)
        latest_email = mail.get_latest_email_sent_to('to@example.com')
        self.assertEquals(latest_email['From'], from_)
        self.assertEquals(latest_email['To'], to)
        self.assertEquals(latest_email['Subject'], subject)
        self.assertEquals(latest_email.get_payload(), body + '\n')
