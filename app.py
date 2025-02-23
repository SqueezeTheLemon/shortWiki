from flask import Flask, render_template, request, redirect, url_for, flash
from database import DBhandler

app = Flask(__name__)
app.secret_key="hellomywiki"

DB = DBhandler()

@app.route("/shortwiki", methods=["GET", "POST"])
def shortwiki():
    return render_template("index.html")

@app.route("/shortwiki/add", methods=["POST"])
def add_entry():
    """ 사용자가 입력한 줄임말을 Firebase에 저장 """
    title = request.form["newTitle"]  # 작품명
    short = request.form["newShort"]  # 줄임말s
    category = request.form["newCategory"]  # 웹소설 or 웹툰

    DB.add_term(title, short, category)  # Firebase에 저장
    flash("줄임말이 성공적으로 추가되었습니다!")
    return redirect("/shortwiki") 

@app.route("/shortwiki/search", methods=["POST"])
def search():
    """ 별도 검색 결과 페이지로 이동 """
    query = request.form["search"]
    search_type = request.form["search_type"]
    results = DB.search_term(query, search_type)  # Firebase에서 검색 수행
    return render_template("search_results.html", query=query, results=results)

@app.route("/shortwiki/popular", methods=["GET"])
def get_popular():
    popular_terms=DB.get_popular_terms()
    return render_template("show_popular.html", popular_terms=popular_terms)