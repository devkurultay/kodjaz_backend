import boto3
from botocore.exceptions import ClientError


def send_email(sender, recipients, aws_region, subject, body_text, body_html):
    client = boto3.client('ses', region_name=aws_region)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': recipients,
            },
            Message={
                'Body': {
                    # TODO(murat): activate this when we come up with 
                    # 'Html': {
                    #     'Charset': "UTF-8",
                    #     'Data': body_html
                    # },
                    'Text': {
                        'Data': body_text,
                        'Charset': "UTF-8",
                    },
                },
                'Subject': {
                    'Data': subject
                },
            },
            Source=sender
        )
    except ClientError as e:
        print(e.response['Error']['Message'], recipients)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def handler(event, context):
    email_params = event['email_params']
    send_email(**email_params)
