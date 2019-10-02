# HouseFinderBot
Scrape data from MLS and alert via Slack.
I hardcoded a bunch of values for my needs, but this can easily be made more for better extensibility.

I hooked it up to a BuildKite agent that runs the script every 15 minutes.

It uses [AWS Dynamodb](https://aws.amazon.com/dynamodb/) to keep track of houses already seen. 
# Environment Variables
* `lnmn` - Longitude minimum
* `lnmx` - Longitude maximum
* `ltmn` - Latitude minimum
* `ltmx` - Latitude maximum
* `max_price` - Maximum price (USD)
* `slack_hook` - Slack hook for notifications

The [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) library
looks in a few different places to find AWS credentials. I used the environment variable option  


# Usage
`python house-finder.py`
