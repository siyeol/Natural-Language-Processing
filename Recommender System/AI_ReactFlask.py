import pymysql
import pandas as pd
import json
from collections import Counter
import sys
import requests
from konlpy.tag import Okt

from flask import Flask, Response, request, jsonify, make_response

from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv(verbose=True)
host = os.getenv('HOST')
port = 3306
user = "admin"
dbname = os.getenv('DBNAME')
password = os.getenv('PASSWORD')
# print(host, port, user, dbname, password)

# const roadmap_recommend = spawn('python3', ['pymyscl_conn_test.py']); #자스에서 파이썬 실행

conn = pymysql.connect(host=host, user=user,port=port,
                        passwd=password, db=dbname)


# @app.route('/', methods=['OPTIONS','POST'])
@app.route('/roadmap-build', methods=['OPTIONS','POST'])
def roadmap():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    elif request.method == 'POST': 
        req = request.get_json()

        keyword = req['hi']
        # df = pd.read_sql("SELECT content FROM roadmaps", conn)
        df = pd.read_sql("SELECT id, content FROM roadmaps WHERE content LIKE '%{}%'".format(keyword), conn)

        # print(df)

        #Json Parsing
        # print(df['id'].values, "id의 게시물 에서 사용이 되었습니다") #check id of dataframe
        print(len(df),"개, ",df['id'].values, "id의 로드맵에서 사용이 되었습니다!\n\n") 

        frequency_list = []

        for j in range(0,len(df)):
            ###Save as Dictionary###
            temp_dic = dict()

            keyword_id = ""

            jsoninfied = json.loads(df['content'][j])['elements']
            jsonLength = len(jsoninfied)
            notEdgeCount = 0
            for i in range(0,jsonLength-1):
                if 'value' in jsoninfied[i]:
                    print(jsoninfied[i]['id']," : ",jsoninfied[i]['value'][1])
                    temp_dic[jsoninfied[i]['id']] = jsoninfied[i]['value'][1]
                    if(jsoninfied[i]['value'][1]==keyword):
                        keyword_id=jsoninfied[i]['id']
                    notEdgeCount+=1
                else:
                    break
                # print(jsoninfied[i]['id'])
            edgeCount = jsonLength - notEdgeCount
            print("Edge Num : ",edgeCount)
            # print(jsoninfied[-edgeCount]) #edge 갯수

            ###edge들 출력###
            for i in range(-edgeCount,0):
                # print(jsoninfied[i]['source'],'-->', jsoninfied[i]['target'])
                if(jsoninfied[i]['source']==keyword_id):
                    print(temp_dic[jsoninfied[i]['target']]) #알고리즘 다음 과목
                    frequency_list.append(temp_dic[jsoninfied[i]['target']])

            # print(len(json.loads(df['content'][0])['elements']))
            # print(temp_dic)
            print("\n")


        count_dict = (dict(Counter(frequency_list)))
        # print((Counter(frequency_list).most_common(3)))
        # print(Counter(frequency_list)[1])
        # sys.stdout.flush()
        return build_actual_response(jsonify(json.loads(json.dumps(count_dict))))


@app.route('/', methods=['OPTIONS','POST'])
def comments():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    elif request.method == 'POST': 
        req = request.get_json()

        df = pd.read_sql("SELECT content FROM comments", conn)

        df["nouns"]=df.content.apply(lambda x: Okt().nouns(x))

        #stopword 추가
        stopwords = pd.read_csv("https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt").values.tolist()
        custom_stopwords = ['답글', '댓글'] #여기에 직접 추가 가능
        for word in custom_stopwords:
            stopwords.append(word)

        counter = Counter()
            
        for nouns in df.nouns:
            word_set = set()

            for noun in nouns:
                if noun in stopwords:
                    continue
                if len(noun)==1:
                    continue
                word_set.add(noun)
            counter.update(word_set)
            
        counter = counter.most_common(5)
        count_dict = (dict(counter))
        return build_actual_response(jsonify(json.loads(json.dumps(count_dict))))


@app.route('/creating-post', methods=['OPTIONS','POST'])
def article():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    elif request.method == 'POST': 
        req = request.get_json()
        # print(req['hi'])
        # print(request)

        article = req['article']

        okt=Okt()
        noun=okt.nouns(article)

        #stopword 추가
        stopwords = pd.read_csv("https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt").values.tolist()
        custom_stopwords = ['생각', '경우', '상황', '이유', '얘기'] #여기에 직접 추가 가능
        for word in custom_stopwords:
            stopwords.append(word)
        # print(stopwords)
        noun = [x for x in noun if len(x) > 1]  # 한글자 키워드 제거
        noun = [x for x in noun if not x in stopwords]  # 불용어 제거

        count = Counter(noun)
            
        count_dict = (dict(count))
        return build_actual_response(jsonify(json.loads(json.dumps(count_dict))))


def build_preflight_response():
    response = make_response()
    if request.headers['Origin'] == "http://localhost:3000" :
        response.headers.add('Access-Control-Allow-Origin', "http://localhost:3000")
    elif request.headers['Origin'] == "http://ec2co-ecsel-1xtrd1tzo98h5-156481910.ap-northeast-2.elb.amazonaws.com" :
        response.headers.add('Access-Control-Allow-Origin', "http://ec2co-ecsel-1xtrd1tzo98h5-156481910.ap-northeast-2.elb.amazonaws.com")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
    
def build_actual_response(response):
    if request.headers['Origin'] == "http://localhost:3000" :
        response.headers.add('Access-Control-Allow-Origin', "http://localhost:3000")
    elif request.headers['Origin'] == "http://ec2co-ecsel-1xtrd1tzo98h5-156481910.ap-northeast-2.elb.amazonaws.com" :
        response.headers.add('Access-Control-Allow-Origin', "http://ec2co-ecsel-1xtrd1tzo98h5-156481910.ap-northeast-2.elb.amazonaws.com")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)