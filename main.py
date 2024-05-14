import json
import boto3
import requests
from urllib.parse import urlencode


def get_account_url():
    # 사용자로부터 세션 만료 시간을 입력 받습니다. 기본값은 6시간입니다.
    duration_hours = int(input('세션 만료 시간을 입력해주세요. 기본값은 6시간 입니다. : ').strip() or 6)
    duration_seconds = duration_hours * 3600

    # AWS STS(Security Token Service)를 통해 임시 자격 증명을 가져옵니다.
    credentials = get_federation_credentials(duration_seconds)

    # 가져온 자격 증명을 기반으로 로그인 URL을 생성합니다.
    return get_login_url(credentials, duration_seconds) if credentials else None


def get_federation_credentials(duration_seconds):
    # AWS STS 클라이언트를 생성합니다.
    sts_client = boto3.client('sts')
    try:
        # 연합 토큰을 요청하여 임시 자격 증명을 가져옵니다.
        response = sts_client.get_federation_token(
            Name='Saltware_federation_user',  # 연합 토큰을 요청하는 사용자의 이름
            DurationSeconds=duration_seconds,  # 토큰의 유효 기간(초)
            PolicyArns=[
                {'arn': 'arn:aws:iam::aws:policy/AdministratorAccess'}  # 사용자에게 적용할 IAM 정책의 ARN 목록
            ]
        )
        return response['Credentials']
    except Exception as e:
        print(f"역할을 가져오는 동안 오류가 발생했습니다: {e}")
        return None


def get_login_url(credentials, duration_seconds):
    # AWS 콘솔 및 로그인 URL
    console_url = "https://console.aws.amazon.com/console/home"
    sign_in_url = "https://signin.aws.amazon.com/federation"

    # 세션 매개변수 설정
    session_parameters = {
        "sessionId": credentials['AccessKeyId'],  # 액세스 키 ID
        "sessionKey": credentials['SecretAccessKey'],  # 비밀 액세스 키
        "sessionToken": credentials['SessionToken']  # 세션 토큰
    }
    encoded_session = urlencode({"Session": json.dumps(session_parameters)})  # 세션 매개변수를 JSON 형식으로 인코딩합니다.
    session_duration = str(duration_seconds)  # 세션의 유지 기간을 초 단위로 지정합니다.

    # 로그인 토큰을 가져오는 URL 설정
    get_signin_token_url = f"{sign_in_url}?Action=getSigninToken&SessionDuration={session_duration}&SessionType=json&{encoded_session}"

    try:
        # 로그인 토큰을 요청하여 가져옵니다.
        response = requests.get(get_signin_token_url)
        response.raise_for_status()
        signin_token = response.json().get('SigninToken')  # 로그인 토큰을 가져옵니다.
        if signin_token:
            signin_token_parameter = urlencode({"SigninToken": signin_token})  # 로그인 토큰을 매개변수로 인코딩합니다.
            destination_parameter = urlencode({"Destination": console_url})  # 대상을 매개변수로 인코딩합니다.
            # 로그인 URL을 반환합니다.
            return f"{sign_in_url}?Action=login&{signin_token_parameter}&{destination_parameter}"
        else:
            print("로그인 토큰을 가져오는 데 실패했습니다.")
    except requests.RequestException as e:
        print(f"HTTP 요청이 실패했습니다: {e}")
    except json.JSONDecodeError:
        print("응답에서 JSON을 디코딩하는 데 실패했습니다.")
    return None


# AWS 계정 URL을 가져옵니다.
url = get_account_url()

# 가져온 URL을 출력합니다.
if url:
    print("다음 URL을 복사해 주세요:", url)
else:
    print("AWS 계정 URL을 가져오는 동안 오류가 발생했습니다.")
