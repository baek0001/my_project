import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbschool  # 'dbreview'라는 이름의 db를 만들거나 사용합니다.

# Disable flag warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
# 시도 / 시군구 정보 가져오기
sido_sigungu_list = [
    {
        'sido_name': '서울특별시',
        'sido_code': '1100000000',
        'sigungu_list': [
                {
                    'sigungu_name': '강남구',
                    'sigungu_code': 1168000000
                },
                {
                    'sigungu_name': '강동구',
                    'sigungu_code': 1174000000
                },
                {
                    'sigungu_name': '강북구',
                    'sigungu_code': 1130500000
                },
                ...
        ]
    },
    ...
]
"""


def get_sido_sigungu_list():
    # 브라우저 실행
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome("./chromedriver", options=options)
    driver.get("https://www.schoolinfo.go.kr/ei/ss/pneiss_a05_s0.do")

    # 소스 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    side_options = soup.select('#sidoCode option')

    result = []
    for sido_option in side_options:
        if sido_option['value'] != '':
            # 시도 가져오기
            sido_name = sido_option.text
            sido_code = sido_option['value']

            # 시도 클릭
            sido_option = driver.find_element_by_css_selector(f'#sidoCode > option[value="{sido_code}"]')
            sido_option.click()
            driver.implicitly_wait(1)

            # 시군구 가져오기
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            sigungu_options = soup.select('#sigunguCode option')
            sigungu_list = []
            for sigungu_option in sigungu_options:
                if sigungu_option['value'] != '':
                    sigungu = sigungu_option.text
                    sigungu_code = sigungu_option['value']
                    sigungu_list.append({
                        'sigungu_name': sigungu,
                        'sigungu_code': sigungu_code
                    })

            result.append({
                'sido_name': sido_name,
                'sido_code': sido_code,
                'sigungu_list': sigungu_list
            })

    # 브라우저 종료
    driver.close()
    return result


"""
# 학교 정보 가져오기
{
    "schoolList": [
        {
            "SCHUL_RDNMA": "서울특별시 강남구 개포로 402",
            "FOND_SC_CODE": "2",
            "USER_TELNO_SW": "02-576-3333",
            "ZIP_CODE": "135240",
            "SCHUL_KND_SC_CODE": "04",
            "DTLAD_BRKDN": "173번지",
            "USER_TELNO": "02-576-3333",
            "JU_ATPT_OFCDC_CODE": "B100000001",
            "LCTN_NM": "서울",
            "PERC_FAXNO": "02-571-6560",
            "HS_KND_SC_CODE": "01",
            "USER_TELNO_GA": "02-576-3334",
            "HMPG_ADRES": "http://gaepo.sen.hs.kr",
            "ADRES_BRKDN": "서울특별시 강남구 개포동",
            "SCHUL_CODE": "B100000373",
            "ADRCD_ID": "1168010300",
            "JU_DSTRT_OFCDC_CODE": "B100000001",
            "SCHUL_NM": "개포고등학교"
        },
        ...
    ]
}
"""


def get_school(sido_code, sigungu_code):
    url = 'https://www.schoolinfo.go.kr/ei/ss/pneiss_a05_s0/selectSchoolListLocation.do'
    data = {
        'HG_JONGRYU_GB': '04',  # 학교 급 (ex. 고등학교 = 4)
        'SIDO_CODE': sido_code,  # 시도 코드 (ex. 서울 특별시 = '1100000000')
        'SIGUNGU_CODE': sigungu_code,  # 시군구 코드 (ex. 강남구 = '1168000000')
        'SULRIP_GB': '1',
        'SULRIP_GB': '2',
        'SULRIP_GB': '3',
        'GS_HANGMOK_CD': '06',  # 공시항목 (졸업생의 진로현황 = 06)
        'PBAN_YR': '2020',  # 공시 년도
        'JG_HANGMOK_CD': '52',  # 공시 년도
    }

    data = requests.post(url, data=data, verify=False)
    school_data = data.json()
    return school_data['schoolList']


# 3. 학교 정보
# 데이터가 없을 수도 있음 (ex. 서울특별시 강남구 단국대학교부속소프트웨어고등학교 - B100000373)
def get_school_info(sido, sigungu, school_name, school_code):
    url = 'https://www.schoolinfo.go.kr/ei/pp/Pneipp_b06_s0p.do?'
    params = {
        'GS_HANGMOK_CD': '06',
        'GS_HANGMOK_NO': '13-%EB%8B%A4',
        'GS_HANGMOK_NM': '%EC%A1%B8%EC%97%85%EC%83%9D%EC%9D%98%20%EC%A7%84%EB%A1%9C%20%ED%98%84%ED%99%A9',
        'GS_BURYU_CD': 'JG040',
        'JG_BURYU_CD': 'JG130',
        'JG_HANGMOK_CD': '52',
        'JG_GUBUN': '1',
        'JG_YEAR2': '2020',
        'HG_NM': '%EA%B2%BD%EA%B8%B0%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90',
        'HG_CD': school_code,  # SCHUL_CODE로만 바꿔주면 됨 ('B100000376')
        'GS_TYPE': 'Y',
        'JG_YEAR': '2020',
        'CHOSEN_JG_YEAR': '2020',
        'PRE_JG_YEAR': '2020',
        'LOAD_TYPE': 'single',
        'LOAD_TYPE': 'single'
    }

    data = requests.get(url, params=params, verify=False)
    soup = BeautifulSoup(data.text, 'html.parser')
    univ_entrance = soup.select_one(
        '#excel > div.table_wrap > div.schoolinfo_table.graytable > table > tbody > tr:nth-child(4) > td:nth-child(3)')
    if univ_entrance is None:
        print(f'{school_name} 대학교 진학자률 : 😭 정보가 없습니다')
    else:
        print(f'{school_name} 대학교 진학자률 : {univ_entrance.text}%')

        doc = {
            '시도': sido,
            '시군구': sigungu,
            '고등학교': school_name,  # DB에는 숫자처럼 생긴 문자열 형태로 저장됩니다.
            '4년제 진학률': univ_entrance.text  # DB에는 숫자처럼 생긴 문자열 형태로 저장됩니다.
        }
        db.dbschool.insert_one(doc)


def run():
    # 시도, 시구군 목록 가져오기
    sido_sigungu_list = get_sido_sigungu_list()

    for sido_sigungu in sido_sigungu_list:
        sido_name = sido_sigungu['sido_name']
        sido_code = sido_sigungu['sido_code']
        print(f'================ {sido_name} ================')

        for sigungu in sido_sigungu['sigungu_list']:
            sigungu_name = sigungu['sigungu_name']
            sigungu_code = sigungu['sigungu_code']

            # 해당 시도 / 시구군에 해당하는 학교 정보 조회
            school_list = get_school(sido_code, sigungu_code)

            for school in school_list:
                school_name = school['SCHUL_NM']
                school_code = school['SCHUL_CODE']
                get_school_info(sido_name, sigungu_name, school_name, school_code)
                # break
            # break
        # break


run()

