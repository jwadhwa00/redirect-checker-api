from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/check_links', methods=['POST'])
def check_links():
    data = request.get_json()
    results = []

    for test in data:
        input_url = test.get("url")
        expected_domain = test.get("expected_domain")
        try:
            response = requests.get(input_url, allow_redirects=True, timeout=10)
            final_url = response.url
            final_domain = urlparse(final_url).netloc

            match = expected_domain in final_domain
            results.append({
                "original_url": input_url,
                "final_url": final_url,
                "expected_domain": expected_domain,
                "match": match,
                "status_code": response.status_code
            })
        except Exception as e:
            results.append({
                "original_url": input_url,
                "final_url": None,
                "expected_domain": expected_domain,
                "match": False,
                "error": str(e)
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
