# fastapi_mysite_card
fastapi, jinja2, sqlalchemy, mariadb, docker, docker-compose, aws,  langchain, apscheduler, uvicorn, requests

### 라이브러리 설명
1.fastapi : 웹 프레임워크 + API
2.uvicorn : WAS(웹 어플리케이션 서버)
3.jinja2 : 템플릿 엔진(HTML, CSS, JS)

### Web 프로그래밍 기초 설명

### 1.URL
  - http://127.0.0.1:8000 = http/localhost:8000
  - 127.0.0.1과 localhost는 루프백 주소(현재 디바이스의 IP를 의미)
  - http -> 프로토콜
  - 8000 -> Port번호
  - http 프로토콜 제공하는 함수(get, post, put, delete)
  - http://127.0.0.1:8000/member?id=abc1234&name=cherry -> 쿼리스트링(get 방식)
  - 숨겨야하는 정보들(post 방식)


### 카카오 나에게 톡 보내기
- 인증코드 URL(Base): https://kauth.kakao.com/oauth/authorize?client_id={REST API 키}&redirect_uri={Redirect URI}&response_type=code&scope=talk_message
- 인증코드 URL(Me): https://kauth.kakao.com/oauth/authorize?client_id=671934a076b2386de0d1673885c05e26&redirect_uri=http://127.0.0.1:8000&response_type=code&scope=talk_message