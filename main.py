import json
import boto3
import requests
from urllib.parse import urlencode


def get_account_url():
    credentials = get_role_sts()
    print(credentials)
    return get_switch_url(credentials) if credentials else None


def get_role_sts():
    sts_client = boto3.client('sts')
    try:
        response = sts_client.get_federation_token(
            Name='Saltware_federation_user',
            DurationSeconds=900,
            PolicyArns=[
                {
                    'arn': 'arn:aws:iam::aws:policy/AdministratorAccess'
                }
            ]
        )
        return response['Credentials']
    except Exception as e:
        print(f"Error assuming role: {e}")
        return None


def get_switch_url(sts):
    console_url = "https://console.aws.amazon.com/console/home"
    sign_in_url = "https://signin.aws.amazon.com/federation"

    session_parameters = {
        "sessionId": sts['AccessKeyId'],
        "sessionKey": sts['SecretAccessKey'],
        "sessionToken": sts['SessionToken']
    }
    encoded_session = urlencode({"Session": json.dumps(session_parameters)})
    session_duration = str(6 * 60 * 60)

    get_signin_token_url = f"{sign_in_url}?Action=getSigninToken&SessionDuration={session_duration}&SessionType=json&{encoded_session}"

    try:
        response = requests.get(get_signin_token_url)
        # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        signin_token = response.json().get('SigninToken')
        if not signin_token:
            print("SigninToken not found in response")
            return None
        signin_token_parameter = urlencode({"SigninToken": signin_token})
        destination_parameter = urlencode({"Destination": console_url})
        return f"{sign_in_url}?Action=login&{signin_token_parameter}&{destination_parameter}"
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response")
    return None


url = get_account_url()

print(url)
