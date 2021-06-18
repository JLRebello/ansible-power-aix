# -*- coding: utf-8 -*-
# Copyright: (c) 2020- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import unittest
from unittest import mock
import copy

from ansible_collections.ibm.power_aix.plugins.modules import flrtvc

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, exit_json, fail_json, rootdir
)


class TestDownloadOnly(unittest.TestCase):
    def setUp(self):
        #TODO make sure working directory isn't empty
        mock_file = open("mock_https_results.txt", "r") #mock of what the flrtvc script returns
        mock_read = mock_file.read()
        mock_https_results = ast.literal_eval(mock_read)
        mock_file.close()

        mock_http_results = None

        mock_file = open("mock_ftp_results.txt", "r") #mock of what the flrtvc script returns
        mock_read = mock_file.read()
        mock_ftp_results = ast.literal_eval(mock_read)
        mock_file.close()

    def _search_dict(subs, s_dict):
        for x in range(len(s_dict)):
            if subs in s_dict[x]:
                return True
        return False


    def test_http_to_ftp(self):
        pass

    def test_http_to_https(self):
        pass

    def test_ftp_to_http(self):
        pass

    @patch('flrtvc.run_flrtvc') #mock run_flrtvc() to keep mock_ftp_results
    def test_ftp_to_https(self):
        self.module.params['protocol'] = "https"
        self.results = mock_ftp_results #TODO maybe we only need to modify results['meta']['report'] here.
        with self.assertRaises(AnsibleExitJson) as result:
            self.flrtvc.main()
            
        self.assertFalse(_search_dict('ftp', results['meta']['1.parse']))
        self.assertFalse(_search_dict('ftp', results['meta']['0.report']))
        pass

    def test_https_to_ftp(self, mock_run_flrtvc):
        pass

    def test_https_to_http(self):
        pass











