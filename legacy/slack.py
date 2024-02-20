import boto3
import json
import time
import random
from slack_sdk import WebClient
from ec2_metadata import ec2_metadata


class SlackAPI:
    def __init__(self, token):
        # 슬랙 클라이언트 인스턴스 생성
        self.client = WebClient(token)

    def get_channel_id(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        # conversations_list() 메서드 호출
        result = self.client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels']
        # 채널 명이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id

    def post_message(self, channel_id, text):
        """
        슬랙 채널에 메세지 보내기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text
        )
        return result


def receive_and_process_sqs_messages():
    # SQS 큐 URL 설정
    sqs_queue_url = ''

    aws_region = 'ap-northeast-2'
    token = ""

    # Slack Configure
    slack = SlackAPI(token)
    channel_name = "general"

    channel_id = slack.get_channel_id(channel_name)

    # AWS SQS 클라이언트 생성
    sqs_client = boto3.client('sqs', region_name=aws_region)

    # 메시지를 수신하여 처리
    while True:
        # SQS에서 메시지 받기
        response = sqs_client.receive_message(
            QueueUrl=sqs_queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=1,  # 여기에서 120초로 조절하여 VisibilityTimeout을 늘립니다.
            WaitTimeSeconds=20
        )

        # 받은 메시지가 있는지 확인
        if 'Messages' in response:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']

            try:
                # 메시지 처리 (여기서는 간단히 출력만 함)
                body = json.loads(message['Body'])
                nowtime = time.time()
                ec2_id = ec2_metadata.instance_id
                sqs_body = f"Received message: {body}\n" + f"time : {nowtime}\n" + f"ec2 : {ec2_id}\n\n"
                print(sqs_body)
                print(nowtime)

                # slack message 전송
                message_ts = slack.post_message(channel_id, sqs_body)

                # 메시지 처리 후 SQS에서 삭제
                sqs_client.delete_message(
                    QueueUrl=sqs_queue_url,
                    ReceiptHandle=receipt_handle
                )

                sleep_time = random.uniform(1, 10)
                print(f"Sleeping for {sleep_time:.2f} seconds.")
                time.sleep(sleep_time)

            except sqs_client.exceptions.ReceiptHandleIsInvalid:
                # 만료된 Receipt Handle을 사용하면 다시 메시지를 받아오고 새로운 Receipt Handle로 삭제
                print("Receipt Handle has expired. Receiving the message again.")
                continue
    print('all messages done')


if __name__ == '__main__':
    receive_and_process_sqs_messages()
