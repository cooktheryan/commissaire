# Copyright (C) 2016  Red Hat, Inc
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
"""
Test cases for the commissaire.jobs.investigator module.
"""

import mock
import os

from . import TestCase
from commissaire.compat.urlparser import urlparse

from commissaire.jobs.investigator import clean_up_key, investigator
from Queue import Queue
from mock import MagicMock


class Test_CleanUpKey(TestCase):
    """
    Tests for clean_up_key function.
    """

    def test_clean_up_key(self):
        """
        Verify clean_up_key removes a given file.
        """
        f = open('clean_up_key_test_file', 'w')
        f.close()
        self.assertTrue(os.stat(f.name))
        clean_up_key(f.name)
        self.assertRaises(OSError, os.stat, f.name)


class Test_JobsInvestigator(TestCase):
    """
    Tests for the investigator job.
    """

    etcd_host = ('{"address": "10.2.0.2",'
                 ' "ssh_priv_key": "dGVzdAo=", "remote_user": "root",'
                 ' "status": "available", "os": "atomic",'
                 ' "cpus": 2, "memory": 11989228, "space": 487652,'
                 ' "last_check": "2015-12-17T15:48:18.710454"}')

    def test_investigator(self):
        """
        Verify the investigator.
        """
        with mock.patch('commissaire.transport.ansibleapi.Transport') as _tp, \
             mock.patch('etcd.Client.get') as _etcd_get, \
             mock.patch('etcd.Client.write') as _etcd_write:

            _tp().get_info.return_value = (
                0,
                {
                    'os': 'fedora',
                    'cpus': 2,
                    'memory': 11989228,
                    'space': 487652,
                }
            )

            q = Queue()

            _etcd_get.return_value = MagicMock(
                'etcd.EtcdResult', value=self.etcd_host)

            to_investigate = {
                'address': '10.0.0.2',
            }
            ssh_priv_key = 'dGVzdAo='

            connection_config = {
                'etcd': {
                    'uri': urlparse('http://127.0.0.1:2379'),
                },
                'kubernetes': {
                    'uri': urlparse('http://127.0.0.1:8080'),
                    'token': 'token',
                }
            }

            q.put_nowait((to_investigate, ssh_priv_key, 'root'))
            investigator(q, connection_config, run_once=True)

            self.assertEquals(1, _etcd_get.call_count)
            self.assertEquals(2, _etcd_write.call_count)
