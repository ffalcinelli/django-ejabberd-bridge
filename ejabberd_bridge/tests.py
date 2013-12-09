# -*- coding: utf-8 -*-
# Copyright (C) 2013  Fabio Falcinelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from io import StringIO
import struct
from django.contrib.auth import get_user_model
from django.test import TestCase
from mock import patch
from ejabberd_bridge.management.commands import ejabberd_auth

__author__ = 'fabio'


class AuthBridgeTestCase(TestCase):
    fixtures = ["auth"]

    def setUp(self):
        super(AuthBridgeTestCase, self).setUp()
        self.cmd = ejabberd_auth.Command()
        self.srv = "localhost"

    def tearDown(self):
        pass

    def _check_cmd_parsing(self, params):
        data = struct.pack(">H", len(params)) + params.encode("utf-8")
        with patch("sys.stdin", StringIO(data.decode("utf-8"))):
            result = self.cmd.from_ejabberd()
        self.assertSequenceEqual(result, params.split(":"))

    def test_from_jabber_auth(self):
        """
        Tests the parsing of the auth command
        """
        params = "auth:User:Server:Password"
        self._check_cmd_parsing(params)

    def test_from_jabber_isuser(self):
        """
        Tests the parsing of the isuser command
        """
        params = "isuser:User:Server"
        self._check_cmd_parsing(params)

    def test_from_jabber_setpass(self):
        """
        Tests the parsing of the setpass command
        """
        params = "setpass:User:Server:Password"
        self._check_cmd_parsing(params)

    def test_to_jabber_true(self):
        """
        Tests conversion from python True value to bytes suitable for eJabberd
        """
        with patch("sys.stdout", new_callable=StringIO) as stdout_mocked:
            self.cmd.to_ejabberd(True)
        self.assertEqual(stdout_mocked.getvalue(), '\x00\x02\x00\x01')

    def test_to_jabber_false(self):
        """
        Tests conversion from python False value to bytes suitable for eJabberd
        """
        with patch("sys.stdout", new_callable=StringIO) as stdout_mocked:
            self.cmd.to_ejabberd(False)
        self.assertEqual(stdout_mocked.getvalue(), '\x00\x02\x00\x00')

    def test_isuser_ok(self):
        """
        Tests isuser command with a existent and valid user
        """
        username = "admin"
        self.assertTrue(self.cmd.isuser(username=username, server=self.srv))

    def test_isuser_does_not_exists(self):
        """
        Tests isuser command with an user which does not exist
        """
        username = "user_that_does_not_exist"
        self.assertFalse(self.cmd.isuser(username=username, server=self.srv))

    def test_isuser_is_disabled(self):
        """
        Tests isuser command with an user which is disabled
        """
        username = "user01"
        self.assertFalse(self.cmd.isuser(username=username, server=self.srv))

    def test_auth_ok(self):
        """
        Tests auth command with a right user and password pair
        """
        username = "user02"
        password = "password"
        self.assertTrue(self.cmd.auth(username=username, server=self.srv, password=password))

    def test_auth_wrong_password(self):
        """
        Tests auth command with a right user but wrong password
        """
        username = "user02"
        password = "WRONG"
        self.assertFalse(self.cmd.auth(username=username, server=self.srv, password=password))

    def test_auth_does_not_exist(self):
        """
        Tests auth command with a non existent user
        """
        username = "user_that_does_not_exists"
        password = "password"
        self.assertFalse(self.cmd.auth(username=username, server=self.srv, password=password))

    def test_auth_not_active(self):
        """
        Tests auth command with a right user and password pair but user is not active
        """
        username = "user01"
        password = "password"
        self.assertFalse(self.cmd.auth(username=username, server=self.srv, password=password))

    def test_setpass_ok(self):
        """
        Tests setpass command with a right user and a new password
        """
        username = "user02"
        password = "new_password"
        self.assertTrue(self.cmd.setpass(username=username, server=self.srv, password=password))

        try:
            user = get_user_model().objects.get(username=username)
            self.assertTrue(user.check_password(password))
        except Exception:
            self.fail("Error retrieving user %s from test database" % username)

    def test_setpass_does_not_exist(self):
        """
        Tests setpass command with a non existent user
        """
        username = "user_that_does_not_exists"
        password = "new_password"
        self.assertFalse(self.cmd.setpass(username=username, server=self.srv, password=password))

    def _execute_cmd_handle(self, params):
        data = struct.pack(">H", len(params)) + params.encode("utf-8")
        with patch("sys.stdin", StringIO(data.decode("utf-8"))), patch("sys.stdout",
                                                                       new_callable=StringIO) as stdout_mocked:
            self.cmd.handle(params, run_forever=False)
        return stdout_mocked.getvalue()

    def test_handle_auth_ok(self):
        """
        Tests successful auth command thorugh the handle method
        """
        params = "auth:user02:localhost:password"
        self.assertEqual('\x00\x02\x00\x01', self._execute_cmd_handle(params))

    def test_handle_auth_nok(self):
        """
        Tests failing auth command thorugh the handle method
        """
        params = "auth:User:Server:Password"
        self.assertEqual('\x00\x02\x00\x00', self._execute_cmd_handle(params))

    def test_handle_isuser_ok(self):
        """
        Tests successful isuser command thorugh the handle method
        """
        params = "isuser:user02:localhost"
        self.assertEqual('\x00\x02\x00\x01', self._execute_cmd_handle(params))

    def test_handle_isuser_nok(self):
        """
        Tests failing isuser command thorugh the handle method
        """
        params = "isuser:User:Server"
        self.assertEqual('\x00\x02\x00\x00', self._execute_cmd_handle(params))

    def test_handle_setpass_ok(self):
        """
        Tests successful setpass command thorugh the handle method
        """
        params = "setpass:user02:localhost:new_password"
        self.assertEqual('\x00\x02\x00\x01', self._execute_cmd_handle(params))

    def test_handle_setpass_nok(self):
        """
        Tests failing setpass command thorugh the handle method
        """
        params = "setpass:User:Server:Password"
        self.assertEqual('\x00\x02\x00\x00', self._execute_cmd_handle(params))
