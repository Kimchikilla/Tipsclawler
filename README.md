# TIPS Company Crawler

이 프로젝트는 [TIPS(Tech Incubator Program for Startup)](http://jointips.or.kr) 웹사이트에서 2025년 선정 기업 정보를 수집하는 크롤러입니다.

## 기능

- TIPS 웹사이트의 기업 목록을 순회하며 상세 정보를 수집합니다.
- 수집된 데이터는 CSV 파일(`tips_companies_2025.csv`)로 저장됩니다.
- 수집 항목:
  - 업체명
  - 과제명
  - 사업분야
  - 선정년월
  - 대표자명
  - 홈페이지
  - 소개
  - 운영사

## 설치 방법

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

## 사용 방법

스크립트를 실행하면 크롤링이 시작됩니다.

```bash
python crawler.py
```

실행이 완료되면 같은 디렉토리에 `tips_companies_2025.csv` 파일이 생성됩니다.
