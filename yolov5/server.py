import mydetect
import sendMSG


if __name__ == '__main__':

    #전송받은 사진
    source = 'car/car1.png'

    #장애인차량 판별
    if mydetect.detect(source):
        print("장애인차량 맞음")
    else:
        print("장애인차량 아님")
        #경찰한테 메세지 보내기
        gps = '위치정보'
        # sendMSG.sendMessage(gps) <- 이거 돈나갑니다 신중하게 쓰세요
       

