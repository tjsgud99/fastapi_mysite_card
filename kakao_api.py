# 카카오 API를 사용해서 나에게 톡 보내기
# 1.Kakao Developer 설정
# 2.인증 코드 요청 -> 카카오 서버 -> 인증 코드 전달(인증 코드 1회성 -> 토큰 1회 발급받음과 동시에 효력X)
# 3.인증 코드를 사용해서 토큰 발급
# 4.토큰을 사용해서 나에게 메시지 보내기
import requests


# 1.카카오 OAUTH URL과 Redirct Key를 사용해서 인증 코드 요청
# -웹 브라우저 URL: https://kauth.kakao.com/oauth/authorize?client_id=671934a076b2386de0d1673885c05e26&redirect_uri=http://127.0.0.1:8000&response_type=code&scope=talk_message
# -위의 코드를 웹 브라우저 URL에 입력하고 엔터누르면 새로운 URL로 변경 code=[???]
# -[???] -> 카카오로부터 전달받은 인증코드

# 2.인증코드를 사용해서 토큰 발급받기
url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant type" : "authorization_code",
    "client_id" : "671934a076b2386de0d1673885c05e26",         # RESTAPI KEY
    "redirect_uri": "http://127.0.0.1:8000",
    "code": "bSPFj1eGxDlmdWpUjuxNzdsDuQHpuL6v6Dw-RGo2BIq_j7WVHP0ssjOx-uYKPXPrAAABjsDsB8uBPKUF0hG4dQ"
}

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)