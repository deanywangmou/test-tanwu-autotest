# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 10:12
# @Author  : zouay
# @Email   : zouay@yunjiglobal.com
# @File    : wechatData.py
# @Software: PyCharm
import json

import os
import requests

from yunjihrt.config.constant import *
from yunjihrt.util.parserConf import ParserConf
from yunjihrt.util.parserIniFile import parserIniFile
from yunjihrt.util.sysTime import RunTime


class wechatData:

    def __init__(self, summary,reportUrl,args):
        self.summary=summary
        self.reportUrl=reportUrl
        #self.projectName=args.projectName
        self.failCount=0
        self.args=args

    def createMarkdownData(self):
        # 创建一个markdown语法的dict数据，并返回
        testType=self.args.testType
        if testType==TEST_TYPE_0:
            testinfo = self.getTestinfo()
            data = " ### {5}接口测试发布  \n""#### 执行用例数<font color=\"info\"> {0}条</font>，请相关同事注意 <font color=\"info\"> {6}</font>\n" \
                        "> 成功用例数： <font color=\"comment\">{1}条</font> \n" \
                        "> 失败用例数： <font color=\"warning\">{2}条</font> \n" \
                        "> 跳过用例数： <font color=\"comment\">{3}条</font> \n" \
                        ">【报告地址】： [点击查看测试报告]({4})"

        elif testType==TEST_TYPE_1 or testType==TEST_TYPE_2:
            testinfo = self.getTestStepinfo()
            # 创建一个markdown语法的dict数据，并返回
            if testinfo.get('fail') == 0:
                data = " ### {5}测试正常  \n""#### 测试接口数<font color=\"info\"> {0}个</font>\n" \
                       "> 成功接口数： <font color=\"comment\">{1}</font> \n" \
                       "> 失败接口数： <font color=\"warning\">{2}</font> \n" \
                       "> 跳过接口数： <font color=\"comment\">{3}</font> \n" \
                       ">【报告地址】： [点击查看测试报告]({4})"
            else:
                data = " ### {5}测试发布  \n""#### 测试接口数<font color=\"info\"> {0}个</font>，请相关同事注意 <font color=\"info\"> {6}</font>\n" \
                       "> 成功接口数： <font color=\"comment\">{1}</font> \n" \
                       "> 失败接口数： <font color=\"warning\">{2}</font> \n" \
                       "> 跳过接口数： <font color=\"comment\">{3}</font> \n" \
                       ">【报告地址】： [点击查看测试报告]({4})"
        data=data.format(testinfo.get('total'),testinfo.get('success'),testinfo.get('fail'),testinfo.get('skip'),testinfo.get('reportUrl'),testinfo.get('testTime')+" <font color=\"info\"> "+testinfo.get('projectName')+'</font>',testinfo.get('at'))

        dictData = {
            "msgtype": "markdown",
            "markdown": {
                "content": data
            }
        }
        return dictData

    def createFeiShuMarkdownData(self):
        # 创建一个markdown语法的dict数据，并返回
        testType = self.args.testType
        if testType == TEST_TYPE_0:
            testinfo = self.getTestinfo()
            data = """{"msg_type":"post",
    "content":{
        "post":{
            "zh_cn":{
                "title":" %(projectName)s 自动化工程执行完成,请相关同事注意",
                "content":[
                    [
                        {
                            "tag":"text",
                            "text":"总共用例数:  %(total)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"成功用例数:  %(success)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"失败用例数:  %(fail)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"跳过用例数:  %(skip)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "un_escape":true,
                            "text":"【报告地址】: "
                        },
                        {
                            "tag":"a",
                            "text":"点击查看测试报告",
                            "href":" %(reportUrl)s "
                        }
                    ]
                ]
            }
        }
    }
}"""
        elif testType == TEST_TYPE_1 or testType == TEST_TYPE_2:
            testinfo = self.getTestStepinfo()
            # 创建一个markdown语法的dict数据，并返回
            if testinfo.get('fail') == 0:
                data = """{"msg_type":"post",
    "content":{
        "post":{
            "zh_cn":{
                "title":" %(projectName)s 测试正常 测试接口数  %(total)s  请相关同事注意",
                "content":[
                    
                    [
                        {
                            "tag":"text",
                            "text":"成功用例数:  %(success)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"失败用例数:  %(fail)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"跳过用例数:  %(skip)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "un_escape":true,
                            "text":"【报告地址】: "
                        },
                        {
                            "tag":"a",
                            "text":"点击查看测试报告",
                            "href":" %(reportUrl)s "
                        }
                    ]
                ]
            }
        }
    }
}"""
            else:
                data = """{"msg_type":"post",
    "content":{
        "post":{
            "zh_cn":{
                "title":" %(projectName)s 测试发布,测试接口数  %(total)s  请相关同事注意",
                "content":[
                    
                    [
                        {
                            "tag":"text",
                            "text":"成功用例数:  %(success)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"失败用例数:  %(fail)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "text":"跳过用例数:  %(skip)s "
                        }
                    ],
                    [
                        {
                            "tag":"text",
                            "un_escape":true,
                            "text":"【报告地址】: "
                        },
                        {
                            "tag":"a",
                            "text":"点击查看测试报告",
                            "href":" %(reportUrl)s "
                        }
                    ]
                ]
            }
        }
    }
}"""

        data=data%{'total':testinfo.get('total'),'success':testinfo.get('success'),'fail':testinfo.get('fail'),'skip':testinfo.get('skip'),'reportUrl':testinfo.get('reportUrl'),'projectName':testinfo.get('testTime')+" "+testinfo.get('projectName')}
        return data

    def getTestinfo(self):
        testcases = self.summary.get("stat").get('testcases')
        total = testcases.get('total', 0)
        successes = testcases.get('success', 0)
        self.failCount= testcases.get('fail', 0)
        skipped = testcases.get('skip', 0)
        resultdict = {}
        resultdict['total'] = total
        resultdict['success'] = successes
        resultdict['fail'] = self.failCount
        resultdict['skip'] = skipped
        resultdict['reportUrl']=self.reportUrl
        testTime = RunTime().getDateTime()
        resultdict['testTime']=testTime
        resultdict['projectName']=os.environ.get("projectName","") #self.projectName
        #pc = ParserConf('properties.ini')
        at =os.environ.get("at","") #pc.get_config_value_by_key(self.projectName, 'at')
        resultdict['at'] = at
        return resultdict
    def getTestStepinfo(self):
        testcases = self.summary.get("stat").get('teststeps')
        total = testcases.get('total', 0)
        successes = testcases.get('successes', 0)
        self.failCount= testcases.get('failures', 0)
        skipped = testcases.get('skipped', 0)
        resultdict = {}
        resultdict['total'] = total
        resultdict['success'] = successes
        resultdict['fail'] = self.failCount
        resultdict['skip'] = skipped
        resultdict['reportUrl']=self.reportUrl
        testTime = RunTime().getDateTime()
        resultdict['testTime']=testTime
        resultdict['projectName'] = os.environ.get("projectName", "")  # self.projectName
        # pc = ParserConf('properties.ini')
        at = os.environ.get("at", "")
        resultdict['at'] = at
        return resultdict

    def sendWcData(self):
        if self.args.IsSend=='yes':
            wechatdata=self.createFeiShuMarkdownData()
            if (wechatdata == ""):
                print("数据为空,将不执行执行发送飞书消息任务")
            else:

                if self.args.testType==TEST_TYPE_1 and self.failCount:
                    #wechatdata.get('markdown')['content']=wechatdata.get('markdown').get('content').replace('测试发布','<font color="warning">告警</font>' )
                    wechatdata.replace('测试发布','告警' )
                    self.sendData(wechatdata)
                elif self.args.testType==TEST_TYPE_0 or self.args.testType==TEST_TYPE_2:
                    self.sendData(wechatdata)
        else:
            print('配置为不发送')


    def sendData(self, dictData):
        headers = {'Content-Type': 'application/json'}
        json_data = json.loads(dictData) #.encode('utf-8')
        pc = parserIniFile()
        webhook = pc.get_config_value_by_key('wechat', 'webhook')
        webhooklist=webhook.split(';')
        webUrl=set(os.environ.get('Webhook','').split(';') + webhooklist)
        print("发送至飞书的初始数据内容如下:")
        print(json_data)
        for webhook in webUrl:
            if len(webhook)>0:
                try:
                    req = requests.post (webhook, json=json_data, headers=headers)
                    if (int(req.status_code) == 200):
                        print("已发送至飞书")
                    else:
                        print("未成功发送至飞书")
                except Exception as e:
                    print('发送机器人失败')


if __name__=='__main__':
    pass