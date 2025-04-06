from flask import Flask,render_template
import pandas
import requests
from bs4 import BeautifulSoup
from flask import request  # also import this at the top



app=Flask(__name__)
@app.route('/')
def home():
    return render_template('form.html')
@app.route('/submit', methods=['POST'])
def submit():
    url = request.form["url"]
    res = requests.get(url)
    soup =BeautifulSoup(res.content,'html.parser')
    headline = []
    link = []
    summary = []
    date = []
    category =[] 
    for article in soup.find_all("div", class_="article-card"):
        headline.append(article.find("h3").text.strip())
        link.append(article.find("a")["href"])
        date.append(article.find("span", class_="date").text.strip())
        sum_tag = article.find("p")
        sum_text = sum_tag.text.strip() if sum_tag else "No summary"
        summary.append(sum_text)

        
        category.append(article.find("a", class_="tag").text.strip())
    data = {
    "Headline": headline,
    "Link": link,
    "Date": date,
    "Summary": summary,
    "Tags": category}
    df=pandas.DataFrame(data)
    df.to_excel("static/news_articles.xlsx", index=False)
    return render_template('result.html', file_url="/static/news_articles.xlsx")
@app.route('/download')
def download():
    return render_template('result.html', file_url="/static/news_articles.xlsx")
    
if __name__ == '__main__':
    app.run(debug=True)

