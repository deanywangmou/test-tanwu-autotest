#!/usr/bin/env python
# coding:utf-8
import os
from yjyhrp.util.runner import yjytest

if __name__ == '__main__':
    set_env = 'PRE'
    os.environ['TEST_ENV'] = set_env
    runtest = yjytest(set_env, 'info')
    if set_env == 'DEV':
        runtest.runtestcase(test_path='testsuites/P端接口/API对接主要接口流程/dev环境通用api主流程测试集.yml',
                            report_title='小前端dev环境P端api测试集报告')
    else:
        runtest.runtestcase(test_path='testsuites/P端接口/API对接主要接口流程/pre环境通用api主流程测试集.yml',
                            report_title='小前端pre环境P端api测试集报告')
