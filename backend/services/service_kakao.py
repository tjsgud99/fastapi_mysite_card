from backend.schemas.message import MessageDTO
import os
from dotenv import load_dotenv


class KakaoService:

    #카카오 토큰 발급받기(+인증코드)
    def get_first_token(self):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
              "grant_type" : "authorization_code",
              "client_id" : "671934a076b2386de0d1673885c05e26",         # RESTAPI KEY
              "redirect_uri": "http://127.0.0.1:8000",
              "code": "TEL0QcFadhwFPOk1r4tMsRbZ5XmShKy2Rug3pKA0lctTeNpW6tLvRwTvG3YKPXWcAAABjuTlMCESmUam6ZdnFg"
        }

    # Access Token 재발급(+ Refresh Token)    
    def refresh_access_token(self):
        pass

    #나에게 카카오톡 보내기
    def send_message(self, msg: MessageDTO):
        
        # 1. 토큰 유무 체크
        # - 토큰 있는 경우 -> Refresh Token을 활용해서 재발급
        if os.path.isfile("./kakao_code.json"):
            tokens = self.refresh_access_token()
        else:
            # - 토큰 없는 경우 -> 토큰 발급
            tokens = self.get_first_token()

        # 2. Access Token을 사용해서 나에게 카카오톡 보내기

        # 3. DB에 저장

        # +. 스케줄러 등록(Refresh Token 재발급)
        # - Refresh Token은 유효기간 2달
        # - 그리고 발급받은 날짜로부터 1달 후 재발급 가능
        # - 스케줄러 -> 1달에 한번씩 Refresh Token을 재발급 받으세요!
