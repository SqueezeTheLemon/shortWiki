import pyrebase #firebase와 , python을 연결하는 라이브러리 pyrebase
import json #json파일을 다루기 위한 라이브러리
import re #정규 표현식 사용 가능
from datetime import datetime #현재 날짜 및 시간 기록

class DBhandler: #firebase realtime databse와 연결하여, 데이터를 다루는 역할을 하는 클래스
    
    #Firebase 초기화
    def __init__(self):
        #firebase 인증 정보를 json 파일에서 불러온다. 
        #firebase_auth.json 파일을 불러와 어떤 firebase와 연결해야 하는지 정보를 읽어옴
        with open("./authentication/firebase_auth.json") as f:
            config = json.load(f)

        #config라는 파라미터를 사용, firebase 연결을 초기화한다
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database() #realtime database 객체 생성
    
    #특정 작품명을 검색
    def search_term(self, query, search_type):#검색어(query)를 받아온다
        #dictionary 컬렉션에서 title이 동일한 데이터를 검색한다. 
        
        query = query.replace(" ", "")  # 모든 띄어쓰기 제거
        try:
            if search_type == "title":
                results = self.db.child("dictionary").order_by_child("title").equal_to(query).get()
            else:
                results = self.db.child("dictionary").order_by_child("short").equal_to(query).get()
        #order_by_child("title") : title 필드 기준대로 정렬하여
        #equal_to(query) : 검색어 query와 정확히 일치하는 데이터만 가져온다. 
            if results.each(): #results를 리스트 형태로 변환한다. 
                data = [{"title": item.val()["title"], "short": item.val()["short"], "views": item.val().get("views", 0), "key": item.key()} for item in results.each()]

                for item in results.each():
                    doc_id=item.key() #firebase에서, 해당 데이터의 key 가져오기
                    current_views=item.val().get("views",0) #현재 조회수 가져옴.
                    self.db.child("dictionary").child(doc_id).update({"views":current_views+1}) #조회수 +1 업데이트
                return data

        except Exception as e:
            print(f"🔥 Firebase 검색 오류: {e}")
            return []
        
    #새로운 줄임말 추가
    def add_term(self, title, short, category):
        title = title.replace(" ", "")  # 모든 띄어쓰기 제거
        short = short.replace(" ", "")  # 모든 띄어쓰기 제거

        new_entry = {
            "title": title, #작품명
            "short": short, #줄임말
            "category": category, #웹소설/웹툰 값 firebase에 추가
            "views": 0, #초기 조회수
            "timestamp": datetime.now().isoformat() #데이터를 추가한 시간을 기록한다. 
        }
        self.db.child("dictionary").push(new_entry) #새로운 항목을 dictionary 컬렉션에 추가한다
        return True
    
    #인기 줄임말 가져오기 (조회수 기준)
    def get_popular_terms(self):
        results = self.db.child("dictionary").order_by_child("views").limit_to_last(5).get()
        return [{"title": item.val()["title"], "short": item.val()["short"], "views": item.val()["views"]} for item in results.each()] if results.each() else []
