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

        # 2. Access Token을 사용해서 나에게 카카오톡 보내기

        # 3. DB에 저장

        # +. 스케줄러 등록(Refresh Token 재발급)
        # - Refresh Token은 유효기간 2달
        # - 그리고 발급받은 날짜로부터 1달 후 재발급 가능
        # - 스케줄러 -> 1달에 한번씩 Refresh Token을 재발급 받으세요!
