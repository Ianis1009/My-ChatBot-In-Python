import json 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLOG_FILE = os.path.join(BASE_DIR, "static", "data", "blog.json")

def load_articles():
    try:
        with open(BLOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("[ERROR]: blog.json was not found.")
        return []
    except json.JSONDecodeError:
        print("[ERROR]: Invalid blog JSON format.")
        return []

def get_article_by_id (article_id):
    articles = load_articles()
    for article in articles:
        if article["id"] == article_id:
            return article

    return None

def get_articles_by_category(category):
    articles = load_articles()
    category = category.lower()
    return [article for article in articles if article["category"].lower() == category]


def get_all_articles():
    return load_articles()


def get_article_by_id(article_id):
    articles = load_articles()

    for article in articles:
        if article["id"] == article_id:
            return article

    return None