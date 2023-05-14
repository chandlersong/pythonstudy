import os
import random
import unittest
import boto3
from botocore.exceptions import ClientError
from loguru import logger
from dotenv import load_dotenv


class SNSSimpleCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()

    def test_publish_message(self):
        topic_arn = os.getenv("topic_arn")
        sns = boto3.resource('sns')
        topic = sns.Topic(topic_arn)
        message = f'hello world:{random.randint(0,100)}'
        subject = f'subject'
        logger.info(f"message {subject},content is {subject},to topic arn {topic_arn}")
        try:
            response = topic.publish(
                Message=message,
                Subject=subject,
            )['MessageId']
            logger.info(f"send message success, message is {response}")
        except ClientError:
            logger.exception(f'Could not publish message to the topic.')
            raise



if __name__ == '__main__':
    unittest.main()
