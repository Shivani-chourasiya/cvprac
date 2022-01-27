import os
import sys
import time
import unittest
import uuid
from pprint import pprint

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from cvprac.cvp_client_errors import CvpRequestError

sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from test_cvp_api import TestCvpClient

class TestCvpClientCC(TestCvpClient):
    ''' Test cases for the CvpClient class.
    '''
    cc_id = None

    def change_control_operations(self, method_to_run, cc_name="", cc_notes=""):
        if self.clnt.apiversion is None:
            self.api.get_cvp_info()
        if self.clnt.apiversion > 3.0:
            pprint('RUN TEST FOR V3 CHANGE CONTROL APIs')
            if method_to_run == 'change_control_create_for_tasks':
                TestCvpClientCC.cc_id = str(uuid.uuid4())
                (task_id, _) = self._create_task()
                chg_ctrl = self.api.change_control_create_for_tasks(
                    TestCvpClientCC.cc_id, cc_name, [task_id])
                return chg_ctrl
            else:
                chg_ctrl_resp = method_to_run(cc_id=TestCvpClientCC.cc_id, notes=cc_notes)
                return chg_ctrl_resp
        else:
            pprint('SKIPPING TEST FOR API - {0}'.format(
                self.clnt.apiversion))
            time.sleep(1)

    def test_api_change_control_create_for_tasks(self):
        ''' Verify change_control_create_for_tasks
        '''

        chg_ctrl_name = 'test_api_%d' % time.time()
        chg_ctrl = self.change_control_operations(
            'change_control_create_for_tasks', cc_name=chg_ctrl_name)
        assert chg_ctrl['value']['change']['name'] == chg_ctrl_name

        # Set client apiversion if it is not already set
        # if self.clnt.apiversion is None:
        #     self.api.get_cvp_info()
        # if self.clnt.apiversion > 3.0:
        #     pprint('RUN TEST FOR V3 CHANGE CONTROL APIs')
        #     # self.cc_id = str(uuid.uuid4())
        #     self.cc_id = str(uuid.uuid4())
        #     chg_ctrl_name = 'test_api_%d' % time.time()
        #     (task_id, _) = self._create_task()
        #     print('tasks...', [task_id])
        #     chg_ctrl = self.api.change_control_create_for_tasks(
        #         self.cc_id, chg_ctrl_name, [task_id])
        #     ccid = chg_ctrl['value']['key']['id']
        #     print('create cc resp', chg_ctrl)
        #     assert chg_ctrl['value']['change']['name'] == chg_ctrl_name

            # cc_id = ''
            # if len(chg_ctrl) > 0:
            #     if 'id' in chg_ctrl[0]:
            #         cc_id = chg_ctrl[0]['id']
            # if cc_id != '':
            #     # Verify the pending change control information
            #     status_url = '/cvpservice/changeControl/' \
            #                  'getChangeControlInformation.do?' \
            #                  'startIndex=0&endIndex=0&ccId={}'.format(cc_id)
            #     chg_ctrl_pending = self.clnt.get(status_url)
            #     print('')
            #     print(chg_ctrl_pending)
            #     print('')

            # # Approve the change control
            # approve_note = "Approving CC via cvprac"
            # approve_chg_ctrl = self.api.change_control_approve(self.cc_id, notes=approve_note)
            # print('Approve chg ctrl rep', approve_chg_ctrl)
            # assert approve_chg_ctrl is not None
            # print(approve_chg_ctrl['value']['approve']['value'])
            # assert approve_chg_ctrl['value']['approve']['value'] is True
            # assert approve_chg_ctrl['value']['approve']['notes'] == approve_note
            # assert approve_chg_ctrl['value']['key']['id'] == cc_id

            # # Start the chnage control
            # start_note = "Start the CC via cvprac"
            # start_chg_ctrl = self.api.change_control_start(self.cc_id, notes=start_note)
            # print('Start change control resp', start_chg_ctrl)
            # assert start_chg_ctrl is not None
            # assert start_chg_ctrl['value']['start']['value'] is True
            # assert start_chg_ctrl['value']['start']['notes'] == start_note
            # assert start_chg_ctrl['value']['key']['id'] == cc_id
            # time.sleep(1)

            # # Stop the chnage control
            # stop_note = "stop the CC via cvprac"
            # stop_chg_ctrl = self.api.change_control_stop(self.cc_id, notes=stop_note)
            # print('stop change control resp', stop_chg_ctrl)
            # assert stop_chg_ctrl is not None
            # assert stop_chg_ctrl['value']['start']['value'] is False
            # assert stop_chg_ctrl['value']['start']['notes'] == stop_note
            # assert stop_chg_ctrl['value']['key']['id'] == cc_id

        # else:
        #     pprint('SKIPPING TEST FOR API - {0}'.format(
        #         self.clnt.apiversion))
        #     time.sleep(1)

        # @parameterized.expand(['333'])

    def test_api_change_control_approve(self):
        # Approve the change control
        approve_note = "Approving CC via cvprac"
        approve_chg_ctrl = self.change_control_operations(
            self.api.change_control_approve, cc_notes=approve_note)
        # approve_chg_ctrl = self.api.change_control_approve(self.cc_id, notes=approve_note)
        print('Approve chg ctrl rep', approve_chg_ctrl)
        assert approve_chg_ctrl is not None
        print(approve_chg_ctrl['value']['approve']['value'])
        assert approve_chg_ctrl['value']['approve']['value'] is True
        assert approve_chg_ctrl['value']['approve']['notes'] == approve_note
        assert approve_chg_ctrl['value']['key']['id'] == TestCvpClientCC.cc_id

    def test_api_change_control_start(self):
        print('ccid in strart', TestCvpClientCC.cc_id)
        # Start the change control
        start_note = "Start the CC via cvprac"
        # start_chg_ctrl = self.api.change_control_start(self.cc_id, notes=start_note)
        start_chg_ctrl = self.change_control_operations(
            self.api.change_control_start, cc_notes=start_note)
        print('Start change control resp', start_chg_ctrl)
        assert start_chg_ctrl is not None
        assert start_chg_ctrl['value']['start']['value'] is True
        assert start_chg_ctrl['value']['start']['notes'] == start_note
        assert start_chg_ctrl['value']['key']['id'] == TestCvpClientCC.cc_id
        time.sleep(1)

    def test_api_change_control_stop(self):
        print('ccid in stop', TestCvpClientCC.cc_id)
        # Stop the chnage control
        stop_note = "stop the CC via cvprac"
        # stop_chg_ctrl = self.api.change_control_stop(self.cc_id, notes=stop_note)
        stop_chg_ctrl = self.change_control_operations(
            self.api.change_control_stop, cc_notes=stop_note)
        print('stop change control resp', stop_chg_ctrl)
        assert stop_chg_ctrl is not None
        assert stop_chg_ctrl['value']['start']['value'] is False
        assert stop_chg_ctrl['value']['start']['notes'] == stop_note
        assert stop_chg_ctrl['value']['key']['id'] == TestCvpClientCC.cc_id

    # def test_api_change_control_create_for_empty_tasks_list(self):
    #     ''' Verify create_change_control_v3
    #     '''
    #     # Set client apiversion if it is not already set
    #     if self.clnt.apiversion is None:
    #         self.api.get_cvp_info()
    #     if self.clnt.apiversion > 3.0:
    #         obj = TestCvpClient()
    #         cc_id = str(uuid.uuid4())
    #         pprint('RUN TEST FOR V3 CHANGE CONTROL APIs')
    #         chg_ctrl_name = 'test_api_%d' % time.time()
    #         with self.assertRaises(CvpRequestError):
    #             chg_ctrl = self.api.change_control_create_for_tasks(
    #                 cc_id, chg_ctrl_name, [], series=False)
    #     else:
    #         pprint('SKIPPING TEST FOR API - {0}'.format(
    #             self.clnt.apiversion))
    #         time.sleep(1)
    #
    # def test_api_change_control_create_for_none_task_id_in_list(self):
    #     ''' Verify create_change_control_v3
    #     '''
    #     # Set client apiversion if it is not already set
    #     if self.clnt.apiversion is None:
    #         self.api.get_cvp_info()
    #     if self.clnt.apiversion > 3.0:
    #         obj = TestCvpClient()
    #         cc_id = str(uuid.uuid4())
    #         pprint('RUN TEST FOR V3 CHANGE CONTROL APIs')
    #         chg_ctrl_name = 'test_api_%d' % time.time()
    #         with self.assertRaises(CvpRequestError):
    #             chg_ctrl = self.api.change_control_create_for_tasks(
    #                 cc_id, chg_ctrl_name, [None], series=False)
    #     else:
    #         pprint('SKIPPING TEST FOR API - {0}'.format(
    #             self.clnt.apiversion))
    #         time.sleep(1)
    #
    # def test_api_change_control_create_for_none_task_ids_not_list(self):
    #     ''' Verify create_change_control_v3
    #     '''
    #     # Set client apiversion if it is not already set
    #     if self.clnt.apiversion is None:
    #         self.api.get_cvp_info()
    #     if self.clnt.apiversion > 3.0:
    #         obj = TestCvpClient()
    #         cc_id = str(uuid.uuid4())
    #         pprint('RUN TEST FOR V3 CHANGE CONTROL APIs')
    #         chg_ctrl_name = 'test_api_%d' % time.time()
    #         with self.assertRaises(TypeError):
    #             chg_ctrl = self.api.change_control_create_for_tasks(
    #                 cc_id, chg_ctrl_name, None, series=False)
    #     else:
    #         pprint('SKIPPING TEST FOR API - {0}'.format(
    #             self.clnt.apiversion))
    #         time.sleep(1)
    #
    # def test_api_change_control_create_for_random_task_id(self):
    #     ''' Verify create_change_control_v3
    #     '''
    #     # Set client apiversion if it is not already set
    #     if self.clnt.apiversion is None:
    #         self.api.get_cvp_info()
    #     if self.clnt.apiversion > 3.0:
    #         random_task_id = '3333'
    #         cc_id = str(uuid.uuid4())
    #         pprint('RUN TEST FOR V3 CHANGE CONTROL APIs')
    #         chg_ctrl_name = 'test_api_%d' % time.time()
    #         # with self.assertRaises(CvpRequestError):
    #         chg_ctrl = self.api.change_control_create_for_tasks(
    #             cc_id, chg_ctrl_name, [random_task_id], series=False)
    #         print('Change control resp', chg_ctrl)
    #
    #         # Approve the change control
    #         '''
    #         Issue - Approve CC succeded for random task_id without creating a task
    #         # but on CVP UI approve button is not enale and it gives msg No congn or image
    #         difference to show. Ideally API should also fail.
    #         '''
    #         approve_note = "Approving CC via cvprac"
    #         approve_chg_ctrl = self.api.change_control_approve(cc_id, notes=approve_note)
    #         print('Approve chg ctrl rep', approve_chg_ctrl)
    #         assert approve_chg_ctrl is not None
    #         print(approve_chg_ctrl['value']['approve']['value'])
    #         assert approve_chg_ctrl['value']['approve']['value'] is True
    #
    #     else:
    #         pprint('SKIPPING TEST FOR API - {0}'.format(
    #             self.clnt.apiversion))
    #         time.sleep(1)


if __name__ == '__main__':
    unittest.main()
