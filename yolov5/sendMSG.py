import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
# @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP

# 문자 메세지 보내주는 함수


def sendMessage(imgsrc, location):
 # set api key, api secret
    api_key = "NCS7GGR7HWXJ5S63"
    api_secret = "ELXLRUXQCB96IDZPTMWWKALRAANGJZXE"
    # 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'mms'  # Message type ( sms, lms, mms, ata )
    params['to'] = '01087602581'  # Recipients Number '01000000000,01000000001'
    params['from'] = '01030994264'  # Sender number
    params['text'] = '<장애인주차구역 불법주차 발생>\n\n[위치] : ' + location  # Message 바꿔줘야함
    params['image'] = imgsrc
    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])
        if "error_list" in response:
            print("Error List : %s" % response['error_list'])
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
        sys.exit()
