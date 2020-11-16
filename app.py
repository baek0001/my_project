from flask import Flask, render_template, jsonify, request
import requests

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbschool  # 'dbreview'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/school/<sido>', methods=['GET'])
def read_school(sido):
    # 1. DB에서 리뷰 정보 모두 가져오기
    filter = {'시도': sido}
    if sido == '시도':
        filter = {}
    all_list = list(db.dbschool.find(filter, {'_id': False}).sort([('시도', 1), ('시군구', 1), ('4년제 진학률', -1)]))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'data': all_list})


@app.route('/sido', methods=['GET'])
def read_sido():
    # 1. DB에서 리뷰 정보 모두 가져오기
    all_list = list(db.dbschool.find({}, {'_id': False}).sort([('시도', 1), ('시군구', 1), ('4년제 진학률', -1)]))
    sido_list = ['시도']
    for school in all_list:
        sido = school['시도']
        if sido not in sido_list:
            sido_list.append(sido)
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'data': sido_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
