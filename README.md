# 임시 로그인 URL을 반환하는 애플리케이션 입니다.
일시적으로 계정에 접근하여 로그아웃 또는 세션 만료 시 접근 불가합니다.


# 해당 애플리케이션 사용 방법

``` bash
git clone https://github.com/fitcloud/temporary-login-url-generator & cd temporary-login-url-generator
```
해당 명령줄을 `cloudshell`에서 실행합니다.
<br><br>
```bash
aws configure
```
해당 명령줄을 실행한 후 미리 발급받은 `accessKey`와 `secretKey`를 입력합니다.<br>
`accessKey`와 `secretKey` 발급 방법은 가이드를 참고해주세요.
<br><br>
```bash
python main.py
```
해당 명령줄을 실행 후 파라미터 값에 응답합니다.
<br><br>
```bash
세션 만료 시간을 입력해주세요. 기본값은 6시간 입니다. : 
```
세션이 유효할 원하는 시간을 입력합니다. 입력하지 않으면 기본인 6시간으로 설정됩니다.
<br><br>
```bash
다음 URL을 복사해 주세요: {URL값}
```
URL값을 복사해서 해당 담당자에게 전송해주세요.<br>

