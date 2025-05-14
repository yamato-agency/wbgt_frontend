from flask import Flask, Response, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["https://wbgt-frontend.onrender.com", "null", "file://", "*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept", "Cache-Control"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# データを取得したい外部サイトのURL
EXTERNAL_SITE_URL = 'https://www.wbgt.env.go.jp/wbgt_data.php'

# 観測地点の設定
STATION_CONFIG = {
    'kyoto': {
        'name': '京都府',
        'stations': {
            '61286': { 'name': '京都', 'lat': 35.0116, 'lon': 135.7681 }
        }
    }
    # 将来的に他の都道府県を追加する場合は、ここに追加
    # 'osaka': {
    #     'name': '大阪府',
    #     'stations': {
    #         '62078': { 'name': '大阪', 'lat': 34.6851, 'lon': 135.5059 }
    #     }
    # }
}

@app.route('/get-wbgt-html', methods=['GET'])
def get_wbgt_html():
    """
    外部サイトからHTMLを取得してクライアントに返すプロクシエンドポイント
    """
    try:
        # 外部サイトにサーバーからリクエスト
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Cache-Control': 'no-cache'
        }
        response = requests.get(EXTERNAL_SITE_URL, headers=headers)
        response.raise_for_status()

        return Response(
            response.text,
            mimetype='text/html',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept, Cache-Control'
            }
        )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching external content: {e}")
        return Response(f"Error fetching external content: {e}", status=500, mimetype='text/plain')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return Response(f"An unexpected error occurred: {e}", status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')