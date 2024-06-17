import boto3
import json
import time

def lambda_handler(event, context):
    # SQS 큐 URL 설정
    sqs_queue_url = ''
    aws_region = 'ap-northeast-2'
    # AWS SQS 클라이언트 생성
    sqs_client = boto3.client('sqs',region_name=aws_region)

    # 메시지를 생성하여 SQS에 전송
    for i in range(100):
        message_body = {'message_number': i + 1, 'timestamp': int(time.time())}
        message_body_json = json.dumps(message_body)

        # SQS에 메시지 전송
        response = sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=message_body_json,
            MessageDeduplicationId=f'message-{i + 1}',  # 중복 방지를 위한 ID 설정
            MessageGroupId='test_messages'  # 메시지 그룹 ID를 원하는 값으로 설정
        )

        print(f"Sent message {i + 1} to SQS. Message ID: {response['MessageId']}")
        
        time.sleep(6)

    return {
        'statusCode': 200,
        'body': json.dumps('Messages sent to SQS successfully!')
    }

