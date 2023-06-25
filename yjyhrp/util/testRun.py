import argparse

import os
from yjyhrp.util.runner import yjytest

from yjyhrp.util.parserConf import ParserConf
from yjyhrp.util.wechatData import wechatData


def jenkinsRun():
    testrun = TestRun()
    projectName = testrun.args.projectName
    buildUrl = os.environ.get('BUILD_URL', '')
    if str(buildUrl).endswith('/'):
        buildId = buildUrl.split('/')[-2]
        reportUrl = '{0}_e6b58b_e8af95_e68aa5_e5918a/'.format(buildUrl)
    else:
        buildId = buildUrl.split('/')[-1]
        reportUrl = '{0}/_e6b58b_e8af95_e68aa5_e5918a/'.format(buildUrl)
    testrun.runner.runAndUploadResult(report_title='{}测试报告'.format(projectName), args=testrun.args)
    if testrun.args.testType == TEST_TYPE_1:
        reportUrl = '{0}/ws/failReports/{1}'.format(buildUrl.split('/' + buildId)[0],
                                                    testrun.runner.reportName)
    wechatD = wechatData(testrun.runner.summary, reportUrl, testrun.args)
    wechatD.sendWcData()


def CICDRun():
    testrun = TestRun()
    buildUrl = os.environ.get('BUILD_URL', '')
    if str(buildUrl).endswith('/'):
        reportUrl = '{0}testReport/'.format(buildUrl)
    else:
        reportUrl = '{0}/testReport/'.format(buildUrl)
    # casepath = os.environ['autotest.casepath']
    # if not casepath:
    #     print('没有找到可以执行的用例')
    #     return
    # summary=testrun.runner.runtestcase(test_path=casepath, report_title='testReport')
    testrun.runner.runAndUploadResult(report_title='testReport', args=testrun.args)
    wechatD = wechatData(testrun.runner.summary, reportUrl, testrun.args)
    wechatD.sendWcData()
