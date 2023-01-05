import boto3
import json


def delete_log_streams(prefix=None):
    """Delete CloudWatch Logs log streams with given prefix or all."""
    next_token = None
    logs = boto3.client('logs')

    if prefix:
        log_groups = logs.describe_log_groups(logGroupNamePrefix=prefix)
    else:
        log_groups = logs.describe_log_groups()

    for log_group in log_groups['logGroups']:
        log_group_name = log_group['logGroupName']
        print("Delete log group:", log_group_name)

        while True:
            if next_token:
                log_streams = logs.describe_log_streams(logGroupName=log_group_name,
                                                        nextToken=next_token)
            else:
                log_streams = logs.describe_log_streams(logGroupName=log_group_name)

            next_token = log_streams.get('nextToken', None)

            for stream in log_streams['logStreams']:
                log_stream_name = stream['logStreamName']
                print("Delete log stream:", log_stream_name)
                logs.delete_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
                # delete_log_stream(log_group_name, log_stream_name, logs)

            if not next_token or len(log_streams['logStreams']) == 0:
                break


if __name__ == '__main__':
    delete_log_streams(prefix='/aws/lambda/test-aws--batch-create')

    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-inbound')

    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-create-inbound')
    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-create')
    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-create-outbound')

    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-merge-inbound')
    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-merge')
    delete_log_streams(prefix='/aws/lambda/test-aws-samplefn-merge-outbound')