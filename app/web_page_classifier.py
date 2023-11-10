import csv
from bs4 import BeautifulSoup
from langdetect import detect

class WebPageClassifier:
    def __init__(self):
        # Define categories and their associated keywords
        self.categories = {
            'Marketplace/Store': ['market', 'store', 'shop', 'buy', 'sell', 'trade'],
            'Search Engine': ['search', 'query', 'find', 'engine', 'lookup'],
            'Forum': ['forum', 'discussion', 'thread', 'post', 'community'],
            'Crypto': ['bitcoin', 'crypto', 'cryptocurrency', 'blockchain', 'wallet', 'monero', 'usdt'],
            'Hidden Wiki': ['wiki', 'hidden', 'index', 'guide', 'links'],
            'Webmail Service': ['email', 'mail', 'inbox', 'smtp', 'webmail'],
            'Personal Blog': ['blog', 'blogger', 'diary', 'personal', 'life'],
            'Uncategorised': []  # Default category if none of the keywords match
        }

    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return 'Unknown'

    def categorize_text(self, text):
        category_scores = {category: 0 for category in self.categories}
        for word in text.split():
            for category, keywords in self.categories.items():
                if word.lower() in keywords:
                    category_scores[category] += 1

        max_category = max(category_scores, key=category_scores.get)
        return max_category if category_scores[max_category] > 0 else 'Uncategorised'

    def requires_javascript(self, text):
        phrases = ['enable javascript', 'javascript required', 'javascript must be enabled']
        return any(phrase in text.lower() for phrase in phrases)

    def detect_captcha(self, text):
        phrases = ['captcha', 'wait while you are redirected', 'wait time']
        return any(phrase in text.lower() for phrase in phrases)

    def classify_page(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text()
        name = soup.title.string if soup.title else 'Unknown'

        category = self.categorize_text(text)
        language = self.detect_language(text)

        has_auth_form = bool(soup.find('input', {'type': 'password'}))
        asks_for_javascript = self.requires_javascript(text)
        asks_for_cookies = 'enable cookies' in text.lower()
        has_captcha = self.detect_captcha(text)

        return {
            'name': name,
            'category': category,
            'language': language,
            'has_auth_form': has_auth_form,
            'asks_for_javascript': asks_for_javascript,
            'asks_for_cookies': asks_for_cookies,
            'has_captcha': has_captcha
        }
