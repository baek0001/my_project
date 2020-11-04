from flask import Flask, render_template, jsonify, request
import requests

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbschool  # 'dbreview'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sido', methods=['GET'])
def read_sido():
    # 1. DB에서 리뷰 정보 모두 가져오기
    sido_list = list(db.dbschool.find({}, {'_id': False}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'list': sido_list})


# @app.route('/sigungu', methods=['GET'])
# def read_sigungu():
#     # 1. DB에서 리뷰 정보 모두 가져오기
#     sigungu_list = list(db.dbschool.find({}, {'_id': False}))
#     # 2. 성공 여부 & 리뷰 목록 반환하기
#     return jsonify({'result': 'success', 'list': sigungu_list})
#
#
# @app.route('/school', methods=['GET'])
# def read_school():
#     # 1. DB에서 리뷰 정보 모두 가져오기
#     school_list = list(db.dbschool.find({}, {'_id': False}))
#     # 2. 성공 여부 & 리뷰 목록 반환하기
#     return jsonify({'result': 'success', 'list': school_list})
#
#
# @app.route('/univ_entrance', methods=['GET'])
# def read_univ_entrance():
#     # 1. DB에서 리뷰 정보 모두 가져오기
#     univ_entrance_list = list(db.dbschool.find({}, {'_id': False}))
#     # 2. 성공 여부 & 리뷰 목록 반환하기
#     return jsonify({'result': 'success', 'list': univ_entrance_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
