from flask import Flask, render_template, request
import requests

app = Flask(__name__)

NEWS_API_KEY = "bce887c3d02f4b40ad16b6451aa930fd"
NEWS_URL = "https://newsapi.org/v2/top-headlines"


@app.route("/")
def home():
    country = request.args.get("country", "us")  # Default to US news
    response = requests.get(NEWS_URL, params={"country": country, "apiKey": NEWS_API_KEY})
    news_data = response.json()

    if news_data["status"] != "ok":
        return "Error fetching news"

    articles = news_data.get("articles", [])
    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
