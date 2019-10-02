import os

import requests
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto3

dynamodb = boto3.resource('dynamodb')


def search_for_houses():
    data = {
        'lnmn': os.environ['lnmn'],  # longitude min
        'lnmx': os.environ['lnmx'],  # longitude max
        'ltmn': os.environ['ltmn'],  # latitude min
        'ltmx': os.environ['ltmx'],  # latitude max
        'sort_by': 'date_desc',
        'min_num_of_acres': 0.250,
        'min_year_built': 2000.000,
        'max_price': os.environ['max_price'],
        'property_type[]': 'Single Family',
        'mx': 100,  # max number of results
    }

    request = requests.get('https://rest.mobilerealtyapps.com/listing/listings/themlsonline', params=data)
    json_dict = request.json()

    houses = json_dict['results']

    return houses


def new_house_attachment(house):
    data = {
        'fallback': house['a'],
        'title': house['a'],
        'title_link': house['eu'],
        'image_url': house['i'],
        'fields': [
            {'title': 'City', 'value': house['c'], 'short': True},
            {'title': 'Year', 'value': house['yb'], 'short': True},
            {'title': 'Price', 'value': house['lp'], 'short': True},
            {'title': 'Lot Size', 'value': house['ac'], 'short': True},
            {'title': 'Lot Size', 'value': house['ac'], 'short': True},
            {'title': 'Finished Sq Ft', 'value': house['fsf'], 'short': True},
            {'title': 'Beds', 'value': house['br'], 'short': True},
            {'title': 'Baths', 'value': house['ba'], 'short': True},
        ]
    }
    return data


def get_new_houses(houses):
    new_houses = []
    table = dynamodb.Table('Houses')

    for house in houses:
        try:
            table.put_item(
                Item={
                    'ID': house['mls'],
                    'Price': house['lp'],
                },
                ConditionExpression=Attr('ID').not_exists() | Attr('Price').ne(house['lp']))

            new_houses.append(house)

        except ClientError as e:
            pass

    return new_houses


def send_notification(slack_hook):
    data = {'text': '<!here> new houses!'}
    requests.post(slack_hook, json=data)


def send_house_message(house, slack_hook):
    data = {'attachments': [new_house_attachment(house)]}
    requests.post(slack_hook, json=data)


def main():
    all_houses = search_for_houses()
    new_houses = get_new_houses(all_houses)

    slack_hook = os.environ['slack_hook']

    if len(new_houses) > 0:
        send_notification(slack_hook)

    for house in new_houses:
        send_house_message(house, slack_hook)


if __name__ == "__main__":
    main()
