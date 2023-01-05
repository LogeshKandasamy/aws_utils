import boto3
import json

client = boto3.client('lambda')


def create_env_existing_resources():
    response = client.list_functions()
    print(response)
    func_paginator = client.get_paginator('list_functions')
    for func_page in func_paginator.paginate():
        for func in func_page['Functions']:
            print(func['FunctionName'])
            if(func['FunctionName'].startswith('test-aws')):
                response = client.update_function_configuration(
                    FunctionName=func['FunctionName'],
                    Environment={
                        'Variables': {
                            'VAR_NAME': 'VAR_VALUE',
                            'VAR_NAME2': 'VAR_VALUE2',
                        }
                    }
                )
               print(response)

def create_tags():
    response = client.list_functions()
    print(response)
    func_paginator = client.get_paginator('list_functions')
    for func_page in func_paginator.paginate():
        for func in func_page['Functions']:
            print(func['FunctionName'])
            if(func['FunctionName'].startswith('test-')):
                tag_response = client.tag_resource(
                    Resource=func['FunctionArn'],
                    Tags={
                        'Category': 'DEV',
                        'CostManagement':'CostCenter',
                        'Owner':'Data'
                    }
                )
                print(tag_response)
                tag_list_response = client.list_tags(
                    Resource=func['FunctionArn'],
                )
                print(tag_list_response)

def list_resources():
    #response = client.list_functions(MasterRegion='us-east-1',FunctionVersion='ALL',MaxItems=200)
    response = client.list_functions()
    print(response)
    print(response['Functions'])
    #print(client.get_paginator())

    func_paginator = client.get_paginator('list_functions')
    for func_page in func_paginator.paginate():
        for func in func_page['Functions']:
            print(func)
            print(func['FunctionName'])
            desc = func.get('Description')
            if desc:
                print(f"\t{desc}")

            print(f"\t{func['Runtime']}: {func['Handler']}")

def invoke_lambda(functionName:str=None):
    test_event = dict()

    response = client.invoke(
        FunctionName=functionName,
        Payload=json.dumps(test_event),
    )
    print("response ",response)
    print(response['Payload'])
    print(response['Payload'].read().decode("utf-8"))

if __name__ == '__main__':
    create_tags()
    list_resources()
    invoke_lambda('test-lambda-name')
    #create_env_existing_resources()