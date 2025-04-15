from canlib import canlib, Frame
import time

# Kvaser 연결 및 설정 class
class Kvaser:
    def __init__(self, channel=0):
        self.channel = channel
        self.openFlags = canlib.canOPEN_ACCEPT_VIRTUAL
        self.bitrate = canlib.canBITRATE_125K
        self.bitrateFlags = canlib.canDRIVER_NORMAL

        self.valid = False
        self.ch = None
        self.device_name = ''
        self.card_upc_no = ''
        try:
            self.ch = canlib.openChannel(self.channel, self.openFlags)
            self.ch.setBusOutputControl(self.bitrateFlags)
            self.ch.setBusParams(self.bitrate)
            self.ch.iocontrol.timer_scale = 1
            self.ch.iocontrol.local_txecho = True
            self.ch.busOn()
            self.valid = True
            self.device_name = canlib.ChannelData.channel_name
            self.card_upc_no = canlib.ChannelData(self.channel).card_upc_no
        except canlib.exceptions.CanGeneralError as e:
            print(f"Error initializing Kvaser channel: {e}")
            self.valid = False
            self.ch = None

    def __del__(self):
        if self.ch:
            self.tearDownChannel()


    def read(self, id, timeout_ms=-1): #CAN read 대기시간
        #CAN 메시지를 읽도록 작성

    def mkdata(self, data):
        #데이터 형태를 CAN에 적합하도록 변경
      
    def transmit_data(self, id: int, data: str, msgFlag=canlib.canMSG_STD):
        #CAN 메시지 보내기

    def __iter__(self):
        while True:
            try:
                frame = self.ch.read()
                yield frame
            except canlib.canNoMsg:
                yield 0
            except canlib.canError:
                return

    def tearDownChannel(self):
        self.ch.busOff()
        self.ch.close()

def split_data_into_chunks(data, chunk_size=8):
    #큰 데이터를 CAN 전송을 위해 분할하기

def main():
  #kvaser 활용하여 CAN 전송 혹은 읽기 작성

if __name__ == "__main__":
    main()
