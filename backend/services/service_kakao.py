from backend.schemas.message import MessageDTO
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json

_ = load_dotenv(find_dotenv())

url = "https://kauth.kakao.com/oauth/token"

client_id= os.getenv("KAKAO_REST_API_KEY")
redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
auth_code=""

class KakaoService:

    #카카오 토큰 발급받기(+인증코드)
    def get_first_token(self):
        data = {
              "grant_type" : "authorization_code",
              "client_id" : "671934a076b2386de0d1673885c05e26",         # RESTAPI KEY
              "redirect_uri": "http://127.0.0.1:8000",
              "code": auth_code
              
        }
        
        response = requests.post(url, data=data)
        tokens = response.json()
        print(tokens)
          
        
        # 발급받은 토큰 kakao_code.json에 저장
        with open(r"./kakao_code.json", "w") as fp:
            json.dump(tokens,fp)
        return tokens
           
    # Access Token 재발급(+ Refresh Token)    
    def refresh_access_token(self):
        # kakao_code.json 파일에서 token 불러오기
        with open(r"./kakao_code.json", "r") as fp:
            tokens = json.load(fp)
        
        refresh_token = tokens["refresh_token"]

        data = {
            "grant_type": "refresh_token",
            "client_id":client_id,
            "refresh_token": refresh_token
        }
        print(data)

        response = requests.post(url, data=data)
        new_tokens = response.json()
        print(new_tokens)

        # Refresh_token으로 access_token 재발급 받는 경우 2가지
        # -refresh_token(2달, 1달 뒤부터 재발급 가능)
        # 1.refresh_token 발급받고 1달 이내(재발급x)
        #   response(new access_token 발급)
        # 2.refresh_token 발급받고 1달 이후

        if new_tokens.get("refresh_token"):
            tokens["refresh_token"] = new_tokens.get("refresh_token")

        tokens["access_token"] = new_tokens.get("access_token")

        with open(r"./kakao_code.json", "w") as fp:
            json.dump(tokens, fp)
        return tokens

    #나에게 카카오톡 보내기
    def send_message(self, msg: MessageDTO):
        
        # 1. 토큰 유무 체크
        # - 토큰 있는 경우 -> Refresh Token을 활용해서 재발급
        if os.path.isfile("./kakao_code.json"):
            # 동작 : kakao_Code.json 파일이 존재한다면
            #        refresh_token을 사용해서 Access_token을 재발급 받으세요
            #        이유는 Access_token(4시간만 사용 가능)
            tokens = self.refresh_access_token()
        else:
            # 동작 : kakao_Code.json 파일이 없다면
            #        토큰을 발급받은적이 없기 때문에
            #        최초로 Access_token과 Refresh_token을 발급받고
            #        kakao_code.json에 저장
            tokens = self.get_first_token()

        # kakao_code.json 유무와 상관없이 토큰(Access, Refresh) 보유
    access_token = "kF2ClmP4DKCfK1paTEt5g6D3ly07UYU0B9IKPXTZAAABjuTlw0HRDLJpR7eCqA"
    msg_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
                 "Authorization": "Bearer " + access_token
    }
    msg_data = {
             "template_object": json.dumps({
            "object_type": "text",
            "text": f"이름: {msg.name} \n메일: {msg.email} \n메시지: {msg.message}",
            "link": {"mobile_web_url" : "https://127.0.0.1:8000"}
        })
    }

    response = requests.post(msg_url, headers=headers, data=msg_data)
    if response.json().get("result_code") == 0:
            print("메시지를 성공적으로 보냈습니다.")
    else:
            print("메시지를 보내는데 실패했습니다. Error" + str(response.json()))
