FROM python:3.8.10


# 기본 패키지들 설치 및 Python 3.6 설치
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
# RUN apt-get update
# RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
# RUN apt-get install python3.8.10

#pip 업그레이드
# RUN python3.8.10 -m pip install pip --upgrade

# 현재 폴더내의 모들 파일들을 이미지에 추가
ADD . /app

# 작업 디렉토리로 이동
WORKDIR /app

EXPOSE 5000
# 작업 디렉토리에 있는 requirements.txt로 패키지 설치
RUN pip install -r requirements.txt

# 컨테이너에서 실행될 명령어. 컨테이거나 실행되면 app.py를 실행시킨다.
CMD python AI_ReactFlask.py