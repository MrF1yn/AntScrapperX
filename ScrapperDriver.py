from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_scrapper', methods=['GET'])
def run_scrapper():
    scrapper_name = request.args.get('scrapper')

    if scrapper_name == 'amazon':
        result = subprocess.run(['python', 'AmazonScrapper.py'], capture_output=True, text=True)
    elif scrapper_name == 'flipkart':
        result = subprocess.run(['python', 'FlipkartScrapper.py'], capture_output=True, text=True)
    elif scrapper_name == 'quora':
        result = subprocess.run(['python', 'QuoraScrapper.py'], capture_output=True, text=True)
    else:
        return jsonify({'error': 'Invalid scrapper name'}), 400

    return jsonify({'output': result.stdout, 'error': result.stderr})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)