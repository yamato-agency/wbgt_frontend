from flask import Flask, Response, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://*.github.io",  # GitHub Pagesのドメイン
            "http://localhost:8000",
            "http://localhost:5000",
            "null",
            "file://",
            "*"
        ],
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
    },
    # 'hokkaido': {
    #     'name': '北海道',
    #     'stations': {
    #         '14163': { 'name': '札幌', 'lat': 43.0645, 'lon': 141.3468 }
    #     }
    # },
    # 'aomori': {
    #     'name': '青森県',
    #     'stations': {
    #         '31312': { 'name': '青森', 'lat': 40.8216, 'lon': 140.7406 }
    #     }
    # },
    # 'iwate': {
    #     'name': '岩手県',
    #     'stations': {
    #         '33431': { 'name': '盛岡', 'lat': 39.7028, 'lon': 141.1523 }
    #     }
    # },
    # 'miyagi': {
    #     'name': '宮城県',
    #     'stations': {
    #         '34392': { 'name': '仙台', 'lat': 38.2682, 'lon': 140.8694 }
    #     }
    # },
    # 'akita': {
    #     'name': '秋田県',
    #     'stations': {
    #         '32402': { 'name': '秋田', 'lat': 39.7193, 'lon': 140.1026 }
    #     }
    # },
    # 'yamagata': {
    #     'name': '山形県',
    #     'stations': {
    #         '35426': { 'name': '山形', 'lat': 38.2405, 'lon': 140.3637 }
    #     }
    # },
    # 'fukushima': {
    #     'name': '福島県',
    #     'stations': {
    #         '36127': { 'name': '福島', 'lat': 37.7502, 'lon': 140.4676 }
    #     }
    # },
    # 'ibaraki': {
    #     'name': '茨城県',
    #     'stations': {
    #         '40201': { 'name': '水戸', 'lat': 36.3418, 'lon': 140.4467 }
    #     }
    # },
    # 'tochigi': {
    #     'name': '栃木県',
    #     'stations': {
    #         '41277': { 'name': '宇都宮', 'lat': 36.5551, 'lon': 139.8824 }
    #     }
    # },
    # 'gunma': {
    #     'name': '群馬県',
    #     'stations': {
    #         '42251': { 'name': '前橋', 'lat': 36.3917, 'lon': 139.0604 }
    #     }
    # },
    # 'saitama': {
    #     'name': '埼玉県',
    #     'stations': {
    #         '43056': { 'name': '熊谷', 'lat': 36.1477, 'lon': 139.3923 }
    #     }
    # },
    # 'chiba': {
    #     'name': '千葉県',
    #     'stations': {
    #         '45148': { 'name': '銚子', 'lat': 35.7347, 'lon': 140.8241 }
    #     }
    # },
    # 'tokyo': {
    #     'name': '東京都',
    #     'stations': {
    #         '44132': { 'name': '東京', 'lat': 35.6895, 'lon': 139.6917 }
    #     }
    # },
    # 'kanagawa': {
    #     'name': '神奈川県',
    #     'stations': {
    #         '46106': { 'name': '横浜', 'lat': 35.4437, 'lon': 139.6380 }
    #     }
    # },
    # 'niigata': {
    #     'name': '新潟県',
    #     'stations': {
    #         '54232': { 'name': '新潟', 'lat': 37.9024, 'lon': 139.0233 }
    #     }
    # },
    # 'toyama': {
    #     'name': '富山県',
    #     'stations': {
    #         '55102': { 'name': '富山', 'lat': 36.6953, 'lon': 137.2138 }
    #     }
    # },
    # 'ishikawa': {
    #     'name': '石川県',
    #     'stations': {
    #         '56227': { 'name': '金沢', 'lat': 36.5761, 'lon': 136.6473 }
    #     }
    # },
    # 'fukui': {
    #     'name': '福井県',
    #     'stations': {
    #         '57066': { 'name': '福井', 'lat': 36.0652, 'lon': 136.2205 }
    #     }
    # },
    # 'yamanashi': {
    #     'name': '山梨県',
    #     'stations': {
    #         '49142': { 'name': '甲府', 'lat': 35.6623, 'lon': 138.5683 }
    #     }
    # },
    # 'nagano': {
    #     'name': '長野県',
    #     'stations': {
    #         '48156': { 'name': '長野', 'lat': 36.6513, 'lon': 138.1830 }
    #     }
    # },
    # 'gifu': {
    #     'name': '岐阜県',
    #     'stations': {
    #         '52586': { 'name': '岐阜', 'lat': 35.3912, 'lon': 136.7223 }
    #     }
    # },
    # 'shizuoka': {
    #     'name': '静岡県',
    #     'stations': {
    #         '50331': { 'name': '静岡', 'lat': 34.9786, 'lon': 138.3831 }
    #     }
    # },
    # 'aichi': {
    #     'name': '愛知県',
    #     'stations': {
    #         '51106': { 'name': '名古屋', 'lat': 35.1815, 'lon': 136.9066 }
    #     }
    # },
    # 'mie': {
    #     'name': '三重県',
    #     'stations': {
    #         '53133': { 'name': '津', 'lat': 34.7303, 'lon': 136.5086 }
    #     }
    # },
    # 'shiga': {
    #     'name': '滋賀県',
    #     'stations': {
    #         '60131': { 'name': '彦根', 'lat': 35.2758, 'lon': 136.2462 }
    #     }
    # },
    # 'osaka': {
    #     'name': '大阪府',
    #     'stations': {
    #         '62078': { 'name': '大阪', 'lat': 34.6851, 'lon': 135.5059 }
    #     }
    # },
    # 'hyogo': {
    #     'name': '兵庫県',
    #     'stations': {
    #         '63518': { 'name': '神戸', 'lat': 34.6900, 'lon': 135.1956 }
    #     }
    # },
    # 'nara': {
    #     'name': '奈良県',
    #     'stations': {
    #         '64036': { 'name': '奈良', 'lat': 34.6851, 'lon': 135.8050 }
    #     }
    # },
    # 'wakayama': {
    #     'name': '和歌山県',
    #     'stations': {
    #         '65042': { 'name': '和歌山', 'lat': 34.2260, 'lon': 135.1675 }
    #     }
    # },
    # 'tottori': {
    #     'name': '鳥取県',
    #     'stations': {
    #         '69122': { 'name': '鳥取', 'lat': 35.5037, 'lon': 134.2375 }
    #     }
    # },
    # 'shimane': {
    #     'name': '島根県',
    #     'stations': {
    #         '68132': { 'name': '松江', 'lat': 35.4723, 'lon': 132.9851 }
    #     }
    # },
    # 'okayama': {
    #     'name': '岡山県',
    #     'stations': {
    #         '66408': { 'name': '岡山', 'lat': 34.6617, 'lon': 133.9180 }
    #     }
    # },
    # 'hiroshima': {
    #     'name': '広島県',
    #     'stations': {
    #         '67437': { 'name': '広島', 'lat': 34.3963, 'lon': 132.4607 }
    #     }
    # },
    # 'yamaguchi': {
    #     'name': '山口県',
    #     'stations': {
    #         '81428': { 'name': '下関', 'lat': 33.9576, 'lon': 130.9355 }
    #     }
    # },
    # 'tokushima': {
    #     'name': '徳島県',
    #     'stations': {
    #         '71106': { 'name': '徳島', 'lat': 34.0735, 'lon': 134.5594 }
    #     }
    # },
    # 'kagawa': {
    #     'name': '香川県',
    #     'stations': {
    #         '72086': { 'name': '高松', 'lat': 34.3403, 'lon': 134.0470 }
    #     }
    # },
    # 'ehime': {
    #     'name': '愛媛県',
    #     'stations': {
    #         '73166': { 'name': '松山', 'lat': 33.8416, 'lon': 132.7661 }
    #     }
    # },
    # 'kochi': {
    #     'name': '高知県',
    #     'stations': {
    #         '74182': { 'name': '高知', 'lat': 33.5597, 'lon': 133.5311 }
    #     }
    # },
    # 'fukuoka': {
    #     'name': '福岡県',
    #     'stations': {
    #         '82182': { 'name': '福岡', 'lat': 33.5904, 'lon': 130.4017 }
    #     }
    # },
    # 'saga': {
    #     'name': '佐賀県',
    #     'stations': {
    #         '85142': { 'name': '佐賀', 'lat': 33.2494, 'lon': 130.2975 }
    #     }
    # },
    # 'nagasaki': {
    #     'name': '長崎県',
    #     'stations': {
    #         '84496': { 'name': '長崎', 'lat': 32.7448, 'lon': 129.8738 }
    #     }
    # },
    # 'kumamoto': {
    #     'name': '熊本県',
    #     'stations': {
    #         '86141': { 'name': '熊本', 'lat': 32.8033, 'lon': 130.7089 }
    #     }
    # },
    # 'oita': {
    #     'name': '大分県',
    #     'stations': {
    #         '83216': { 'name': '大分', 'lat': 33.2381, 'lon': 131.6000 }
    #     }
    # },
    # 'miyazaki': {
    #     'name': '宮崎県',
    #     'stations': {
    #         '87376': { 'name': '宮崎', 'lat': 31.9111, 'lon': 131.4239 }
    #     }
    # },
    # 'kagoshima': {
    #     'name': '鹿児島県',
    #     'stations': {
    #         '88317': { 'name': '鹿児島', 'lat': 31.5602, 'lon': 130.5581 }
    #     }
    # },
    # 'okinawa': {
    #     'name': '沖縄県',
    #     'stations': {
    #         '91197': { 'name': '那覇', 'lat': 26.2124, 'lon': 127.6809 }
    #     }
    # }
}

@app.route('/get-wbgt-html', methods=['GET'])
def get_wbgt_html():
    """
    外部サイトからHTMLを取得してクライアントに返すプロクシエンドポイント
    
    処理の流れ:
    1. 外部サイトにサーバーからリクエスト
    2. レスポンスをクライアントに返す
    3. エラーが発生した場合はエラーメッセージを返す
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