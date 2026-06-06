import boto3

from ..config import settings


dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION
)

table = dynamodb.Table(
    settings.DYNAMODB_TABLE_NAME
)


def get_contact(
    contact_id: str
):

    response = table.get_item(
        Key={
            "contactId": contact_id
        }
    )

    return response.get("Item")


def batch_get_contacts(
    contact_ids: list[str]
):

    client = boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION
    )

    request_items = {
        settings.DYNAMODB_TABLE_NAME: {
            "Keys": [
                {
                    "contactId": {
                        "S": contact_id
                    }
                }
                for contact_id
                in contact_ids
            ]
        }
    }

    response = client.batch_get_item(
        RequestItems=request_items
    )

    return (
        response["Responses"]
        [settings.DYNAMODB_TABLE_NAME]
    )


def save_contact(
    contact
):

    table.put_item(
        Item=contact
    )

def count_contacts():

    response = table.scan(
        Select="COUNT"
    )

    return response["Count"]