# 카카오 API를 사용해서 나에게 톡 보내기
# 1.Kakao Developer 설정
# 2.인증 코드 요청 -> 카카오 서버 -> 인증 코드 전달(인증 코드 1회성 -> 토큰 1회 발급받음과 동시에 효력X)
# 3.인증 코드를 사용해서 토큰 발급
# 4.토큰을 사용해서 나에게 메시지 보내기
import requests
import json

# 1.카카오 OAUTH URL과 Redirct Key를 사용해서 인증 코드 요청
# -웹 브라우저 URL: https://kauth.kakao.com/oauth/authorize?client_id=671934a076b2386de0d1673885c05e26&redirect_uri=http://127.0.0.1:8000&response_type=code&scope=talk_message
# -위의 코드를 웹 브라우저 URL에 입력하고 엔터누르면 새로운 URL로 변경 code=[???]
# -[???] -> 카카오로부터 전달받은 인증코드

# 2.인증코드를 사용해서 토큰 발급받기
url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type" : "authorization_code",
    "client_id" : "671934a076b2386de0d1673885c05e26",         # RESTAPI KEY
    "redirect_uri": "http://127.0.0.1:8000",
    "code": "FYld0dgtPw9JRlQcNp6rIMJTzWotlWQzN7LNIau0iGwLuK3jnYpN-TuTNNIKKwyoAAABj1E6DX3SDh85zpcCzQ"
}
print(data)
response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# 3.토큰 이용해서 나에게 톡 보내기
# access_token = "kF2ClmP4DKCfK1paTEt5g6D3ly07UYU0B9IKPXTZAAABjuTlw0HRDLJpR7eCqA"

# msg_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
# headers = {
#     "Authorization": "Bearer " + access_token
# }
# msg_data = {
#     "template_object": json.dumps({
#         "object_type": "text",
#         "text": "카카오톡 테스트",
#         "link": {"mobile_web_url" : "https://www.naver.com"}
#     })
# }

# response = requests.post(msg_url, headers=headers, data=msg_data)







