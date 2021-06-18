# -*- coding: utf-8 -*-
# Copyright: (c) 2020- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import unittest
from unittest import mock
import copy
import stat

from ansible_collections.ibm.power_aix.plugins.modules import flrtvc

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, exit_json, fail_json, rootdir, mock_ftp_report
)

params = {
        'apar': None,
        'filesets': None,
        'csv': None,
        'path': '/var/adm/ansible',
        'save_report': False,
        'verbose': False,
        'force': False,
        'clean': False,
        'check_only': False,
        'download_only':False,
        'extend_fs':True,
        '/protocol': None,
}

init_results = {
    'changed': False,
    'msg': '',
    'meta':{'messages': []}
    # meta structure will be updated as follow:
    # meta={'messages': [],     detail execution messages
    #       '0.report': [],     run_flrtvc reports the vulnerabilities
    #       '1.parse': [],      run_parser builds the list of URLs
    #       '2.discover': [],   run_downloader builds the list of epkgs found in URLs
    #       '3.download': [],   run_downloader builds the list of downloaded epkgs
    #       '4.1.reject': [],   check_epkgs builds the list of rejected epkgs
    #       '4.2.check': [],    check_epkgs builds the list of epkgs checking prerequisites
    #       '5.install': []}    run_installer builds the list of installed epkgs
}

def _search_dict(subs, s_dict):
    for x in range(len(s_dict)):
        if subs in s_dict[x]:
            return True
    return False


class TestDownloadOnly(unittest.TestCase):
    def setUp(self):
        global params, init_results
        #mock_file = open("mock_https_results.txt", "r") #mock of what the flrtvc script returns
        # with open("/Users/juliarebello/Ansible/ansible_collections/ibm/power_aix/tests/unit/plugins/modules/mock_https_results.txt", "r") as mock_file:
        #     mock_read = mock_file.read()
        #     mock_https_results = ast.literal_eval(mock_read)
        #     mock_file.close()

        mock_http_results = None

        self.module = mock.Mock()
        self.module.params = params
        self.module.debug.return_value = None
        self.run_command_environ_update.return_value = None
        with open(mock_ftp_report, "r") as mock_file:
            mock_read = mock_file.read()
            #mock_ftp_results = ast.literal_eval(mock_read)

    def test_http_to_ftp(self):
        pass

    def test_http_to_https(self):
        pass

    def test_ftp_to_http(self):
        pass

    def test_ftp_to_https(self):
        ansible_module_path = rootdir+"flrtvc.AnsibleModule"
        run_flrtvc_path = rootdir+"flrtvc.run_flrtvc"
        os_path_abspath = rootdir+"flrtvc.os.path.abspath"
        os_path_exists = rootdir+"flrtvc.os.path.exists"
        download_path = rootdir+"flrtvc.download"
        unzip_path = rootdir+"flrtvc.unzip"
        os_stat_path = rootdir+"flrtvc.os.stat"
        self.module.params['protocol'] = "https"
        self.results['meta']['0.report'] = self.mock_ftp_results

        with mock.patch(ansible_module_path) as mocked_ansible_module, \
             mock.patch(os_path_abspath) as mocked_os_path_abspath, \
             mock.patch(run_flrtvc_path) as mocked_run_flrtvc, \
             mock.patch(os_path_exists) as mocked_os_path_exists, \
             mock.patch(download_path) as mocked_download, \
             mock.patch(unzip_path) as mocked_unzip, \
             mock.patch(os_stat_path) as mocked_os_stat:
            mocked_run_flrtvc.return_value = True
            mocked_os_path_abspath.side_effect = [ 
                '/var/adm/ansible/work', 
                '/usr/bin', 
                '/usr/bin/flrtvc.ksh',
                '/var/adm/ansible/work/FLRTVC-latest.zip'
            ]
            mocked_os_path_exists.return_value = False
            mocked_download.return_value = True
            mocked_unzip.return_value = True
            flrtvc_stat = mock.Mock()
            flrtvc_stat.st_mode = stat.S_IEXEC
            mocked_os_stat.return_value = flrtvc_stat

            mocked_ansible_module.return_value = self.module
            with self.assertRaises(AnsibleExitJson) as result:
                flrtvc.main()
        
        print(self.results['meta']['0.report'])
        self.assertFalse(_search_dict('ftp', self.results['meta']['0.report']))
        self.assertFalse(_search_dict('ftp', self.results['meta']['1.parse']))
        pass

    def test_https_to_ftp(self):
        pass

    def test_https_to_http(self):
        pass











