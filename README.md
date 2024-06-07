# fastapi_mysite_card
fastapi, jinja2, sqlalchemy, mariadb, docker, docker-compose, aws,  langchain, apscheduler, uvicorn, requests

# pip install -r requirements.txt
# requirements.txt 전부 인스톨
# pip freeze > requirements.txt

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

### 2.DAO and DTO(VO)
  - DAO(Data Access Object): CRUD 할 때 사용
      + Create : INSERT
      + Read   : SELECT
      + Update : UPDATE
      + Delete : DELETE
  - DTO(Data Transfer Object): 데이터를 전달할 때

### 3.유효성(Validation) 체크
  -유효성체크는 사용자의 값이 올바른 값인지 체크
    + 예: 이메일(이메일 형식인지?)
  - 역사
    1. 유효성체크 : 서버 -> 과부화
    2.             클라이언트(웹브라우저) -> JS (사용중)
    3.             서버 추가 -> 더블 체크(pydantic)

### 4.웹 동자 과정 PROCESS
  - 정의: Client(=Web browser), Server(회사)
  - 동작: Client -> request -> server -> response -> Client
  - 동작(심화): View단(Client) -> Controller단(main, router) -> Service단 -> Model단(DB)
    + View단 : 사용자에게 보여지는 화면
    + Controller : 사용자가 요청한 URL과 데이터(유효성체크)를 전달받고 일을 분배하는 곳
    + Service단 : 실제 기능구현
    + Model단 : DB관련된 기능 구현(DAO)

  1. Client에서 form 또는 ajax 등을 사용해서 request(+data)   # fnc.js의 #.ajax
    -URL: http://127.0.0.1:8000/kakao/
    -method : Post
    -data : json
  2. Server의 main.py 에서 요청을 받기 -> 해당 라우터로 전달
  3. Server의 해당 Router(kakao)에서 request와 data를 받음
    - pydantic을 활용한 data validation check(유효성 검증) -> data
  4. Server의 Service단으로 request와 data를 전달  

### 5. Web과 DB
- 2가지방법(SQL 매핑, ORM)
- SQL 매핑: web서버 -> DB 커넥션 ->SQL 작성 -> DB에서 SQL 실행 -> Web서버 결과 받기
- ORM: DB의 테이블 객체화 시켜서 사용하는 방법(최신), SQL 사용 안함, 확장성 및 유지보수 등이 용이
 + Web서버 -> DB 커넥션 -> ORM(객체화) -> ORM사용 -> Web서버 결과 받기

 
### 카카오 나에게 톡 보내기
- 인증코드 URL(Base): https://kauth.kakao.com/oauth/authorize?client_id={REST API 키}&redirect_uri={Redirect URI}&response_type=code&scope=talk_message
- 인증코드 URL(Me): https://kauth.kakao.com/oauth/authorize?client_id=671934a076b2386de0d1673885c05e26&redirect_uri=http://127.0.0.1:8000&response_type=code&scope=talk_message

#### 1. 카카오 API 용어
- 인증코드: 1회성, 토큰(Access, Refresh)
  발급 받기 위해 사용!
- Access 토큰: 카카오 API 서비스를 이용할 때 사용
- Refresh 토큰: Access 토큰을 재발급 받기 위해 사용
- 생명주기: 인증코드(1회), Access(6시간), Refresh(2달)
- Refresh Token은 발급받고 1달 후부터 재발급 가능
- Access와 Refresh 재발듭 받는 코드는 동일
-   ㄴ 재발급 코드: Refresh 발급받은지 1달 미만, Access토큰만 재발급해서 리턴
-   ㄴ 재발급 보드: Refresh 발급받은지 1달 이상, Access토큰과 Refresh 토큰 재발급해서 리턴

#### 2. 카카오 API 사용 방법
1. Kakoa Developer 사이트에서 권한 허용 및 동의
2. 웹브라우저 URL을 통해서 인증 코드 발급
3. 인증코드 사용해서 토큰(Access, Refresh) 발급
4. Access 사용해서 서비스 이용!
5. + 1달에 한번씩 Refresh 토큰 재발급 스케줄링


### LLM 모델 신기술 : RAG(검색증강생성)

기존 LLM 모델의 단점
  1. 최신 내용 반영 X -> 최신 내용 반영하도록 재학습(시간, 자원) / 비효율적

RAG 방법
  + 기존에 추가해야하는 내용 -> 임베딩 -> Vector DB에 저장
  1. 사용자 질문
    - 사용자 질문과 Vector DB에 있는 값들간의 유사도를 계산해서 비슷한 내용을 추출
    - 추출한 내용과 사용자 질문을 함께 LLM 모델에 전달
    - LLM 모델이 Vector DB(질문과 유사한 값)에 있는 값을 활용해서 답변을 생성

### 서비스 배포
  - AWS Lightsail(월 7달러) / RAM !GB 이상

  1. Lightsail: 인스턴스 생성(Linux / Ubuntu 22.04 LTS)
  2. Lightsail: 고정 IP 생성
  3. Lightsail: Port 오픈(8000, 443, 3306)
  4. Window 터미널: Lightsail 원격 접속 SSH 설정
  5. Github: Token 생성
  6. Lightsail: Github repository clone(Token 필요!)
  7. Windows 터미널: SCP를 사용해서 파일 전송(.env, kakao_code.json, resume.pdf)
  8. Lightsail: Docker 및 Docker-compose 설치
  9. Lightsail: dockerfile, docker-compose 파일 작성
  10. Lightsail: docker build를 통해서 이미지 생성(mysite)
  11. Lightsail: docker-compose 서비스 시작
  12. Lightsail: Nginx(리버스 프록시) 
      - 기본 설정(client -> uvicorn(mysite))
      - 프록시 설정(client -> Nginx-> uvicorn(mysite))
  13. Lightsail: Gunicorn
    - Uvicorn(ASGI) : 비동기 서버 게이트웨이 인터페이스 , 스레드 1개
    - Gunicorn(WSGI) : 웹 서버 게이트웨이 인터페이스(다수의 네트워크 통신 가능)
    - Gunicorn설정(with Uvicorn) # windows 사용 불가
  14. 가비아 : 도메인 구매 및 도메인 연결
    - 도메인 구매 www.mysite.com -> AWS Lightsail 고정 IP로 설정
  15. Lightsail: HTTPS(SSL) 적용(웹 통신 암호화) -> Nginx 설정
    - HTTPS 암호화 코드 (CERTBOT 무료)
    - 4개월만 사용, 4개월 후에는 refresh(스케줄링: 매월 1일 refresh)


    ### 도커 컨테이너
      - "내 컴퓨터에서는 되는데 왜 니 컴퓨터에서는 안되지?
      - -> 개발 환경이 바뀌면 기존에 잘 동작하던 코드도 비정상 오류가 발생
      - -> 컨테이너 단위로 만들어서 그 안에서 개발한 서비스를 동작시키자
      - 생성된 컨테이너는 어디서든지 도커만 있으면 똑같이 동작
      - * 컨테이너를 생성하기 위해서는 도커 이미지 필요
      -  도커 이미지(설계도면)

      - JAVA: Class(설계 도면) -> 객체 생성 -> 인스턴스
      - DOCKER: 도커 이미지 -> 컨테이너 생성 -> 컨테이너(동일한 이미지로 다수 생성 가능)
      - 도커 이미지? Dockerfile과 build 명령어를 사용하면 이미지 생성 가능

      - 도커 허브: 다양한 도커 이미지가 존재(mysql, mariadb, mongodb 기타 등등 존재)


      - ex) 컨테이너1(mysite) : 이미지 생성 필요
      -     컨테이너2(mariadb) : 도커 허브에 이미지 존재
      -     컨테이너3(nginx)  : 도커 허브에 이미지 존재
      -     컨테이너4(CERTBOT) 도커 허브에 이미지 존재

### 도커 실생과정
1. RUN 명령어로 Docker 실행
  - 로컬에서 이미지 찾기!(있으면 실행)
  - 로컬에 이미지가 없으면 도커 허브로 가서 검색 및 다운로드
  - 이미지로 컨테이너 생성 및 실행

### 도커 컴포우즈
  - 도커 컨테이너를 프로젝트 단위로 묶어서 사용함으로써 관리 및 유지보수가 편리하게 해줌
  - docker(x), docker-compose(o)    
###













