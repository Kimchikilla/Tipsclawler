import requests
from bs4 import BeautifulSoup
import csv
import time
import os

# 설정
BASE_URL = "https://www.jointips.or.kr"
LIST_URL_TEMPLATE = "https://www.jointips.or.kr/bbs/board.php?bo_table=team&page={}&sfl=wr_26&stx=2025"
OUTPUT_FILE = "tips_companies_2025.csv"

# 헤더 설정 (브라우저인 척)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_soup(url):
    """URL에서 HTML을 가져와 BeautifulSoup 객체로 반환"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_company_detail(detail_url):
    """상세 페이지에서 기업 정보 추출"""
    soup = get_soup(detail_url)
    if not soup:
        return None

    company_info = {}
    
    # 컨텐츠 영역 찾기
    content_area = soup.select_one(".content.col-xs-12")
    if not content_area:
        print(f"Warning: Content area not found for {detail_url}")
        return None

    # 기업명
    header = content_area.select_one("section header h2")
    company_info['기업명'] = header.get_text(strip=True) if header else ""

    # 소개
    desc = content_area.select_one(".desc")
    company_info['소개'] = desc.get_text(strip=True) if desc else ""

    # 상세 테이블 파싱
    table = content_area.select_one("table.table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            th = row.find("th")
            td = row.find("td")
            if th and td:
                key = th.get_text(strip=True)
                # 사이트 링크 처리
                if key == "사이트":
                    link = td.find("a")
                    value = link['href'] if link and link.has_attr('href') else td.get_text(strip=True)
                # 운영기관 링크 텍스트 처리    
                elif key == "운영기관":
                    value = td.get_text(strip=True)
                else:
                    value = td.get_text(strip=True)
                
                company_info[key] = value

    return company_info

def main():
    print("크롤링 시작...")
    all_companies = []
    page = 1
    
    while True:
        print(f"페이지 {page} 처리 중...")
        list_url = LIST_URL_TEMPLATE.format(page)
        soup = get_soup(list_url)
        
        if not soup:
            break

        # 리스트 아이템 찾기
        items = soup.select(".packery-list .item")
        if not items:
            print("더 이상 페이지가 없습니다.")
            break
            
        print(f"- {len(items)}개의 기업 발견")
        
        for item in items:
            # 상세 페이지 링크 추출
            link_tag = item.select_one(".mask a")
            if link_tag and link_tag.has_attr('href'):
                detail_url = link_tag['href']
                if detail_url.startswith('..'): # 상대 경로 보정 (혹시 몰라서)
                    detail_url = BASE_URL + detail_url[2:]
                elif detail_url.startswith('/'):
                    detail_url = BASE_URL + detail_url
                
                # 상세 페이지 크롤링
                print(f"  - 상세 정보 수집 중: {detail_url}")
                company_data = parse_company_detail(detail_url)
                if company_data:
                    all_companies.append(company_data)
                
                # 서버 부하 방지
                time.sleep(0.5)
        
        page += 1
        time.sleep(1)

    # CSV 저장
    if all_companies:
        print(f"총 {len(all_companies)}개의 기업 정보를 수집했습니다.")
        
        # 모든 가능한 키(헤더) 수집
        fieldnames = set()
        for c in all_companies:
            fieldnames.update(c.keys())
        
        # 보기 좋게 정렬 (기업명, 소개, 사업분야 등을 앞으로)
        priority_fields = ['기업명', '사업분야', '설립일', '대표자', '사이트', 'TIPS 선정', '운영기관', '소개']
        sorted_fieldnames = [f for f in priority_fields if f in fieldnames] + [f for f in fieldnames if f not in priority_fields]
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted_fieldnames)
            writer.writeheader()
            writer.writerows(all_companies)
            
        print(f"'{OUTPUT_FILE}' 파일로 저장 완료!")
    else:
        print("수집된 데이터가 없습니다.")

if __name__ == "__main__":
    main()
