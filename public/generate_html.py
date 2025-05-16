import os
import re

# 各都道府県のデータ
station_data_list = [
    {
        "code": '14163',
        "name": '札幌',
        "pref": '北海道',
        "lat": 43.0645,
        "lon": 141.3468
    },
    {
        "code": '31312',
        "name": '青森',
        "pref": '青森県',
        "lat": 40.8216,
        "lon": 140.7406
    },
    {
        "code": '33431',
        "name": '盛岡',
        "pref": '岩手県',
        "lat": 39.7028,
        "lon": 141.1523
    },
    {
        "code": '32402',
        "name": '秋田',
        "pref": '秋田県',
        "lat": 39.7193,
        "lon": 140.1026
    },
    {
        "code": '35426',
        "name": '山形',
        "pref": '山形県',
        "lat": 38.2405,
        "lon": 140.3637
    },
    {
        "code": '34392',
        "name": '仙台',
        "pref": '宮城県',
        "lat": 38.2682,
        "lon": 140.8694
    },
    {
        "code": '36127',
        "name": '福島',
        "pref": '福島県',
        "lat": 37.7502,
        "lon": 140.4676
    },
    {
        "code": '40201',
        "name": '水戸',
        "pref": '茨城県',
        "lat": 36.3418,
        "lon": 140.4467
    },
    {
        "code": '41277',
        "name": '宇都宮',
        "pref": '栃木県',
        "lat": 36.5551,
        "lon": 139.8824
    },
    {
        "code": '42251',
        "name": '前橋',
        "pref": '群馬県',
        "lat": 36.3917,
        "lon": 139.0604
    },
    {
        "code": '43056',
        "name": '熊谷',
        "pref": '埼玉県',
        "lat": 36.1477,
        "lon": 139.3923
    },
    {
        "code": '45148',
        "name": '銚子',
        "pref": '千葉県',
        "lat": 35.7347,
        "lon": 140.8241
    },
    {
        "code": '44132',
        "name": '東京',
        "pref": '東京都',
        "lat": 35.6895,
        "lon": 139.6917
    },
    {
        "code": '46106',
        "name": '横浜',
        "pref": '神奈川県',
        "lat": 35.4437,
        "lon": 139.6380
    },
    {
        "code": '54232',
        "name": '新潟',
        "pref": '新潟県',
        "lat": 37.9024,
        "lon": 139.0233
    },
    {
        "code": '55102',
        "name": '富山',
        "pref": '富山県',
        "lat": 36.6953,
        "lon": 137.2138
    },
    {
        "code": '56227',
        "name": '金沢',
        "pref": '石川県',
        "lat": 36.5761,
        "lon": 136.6473
    },
    {
        "code": '57066',
        "name": '福井',
        "pref": '福井県',
        "lat": 36.0652,
        "lon": 136.2205
    },
    {
        "code": '49142',
        "name": '甲府',
        "pref": '山梨県',
        "lat": 35.6623,
        "lon": 138.5683
    },
    {
        "code": '48156',
        "name": '長野',
        "pref": '長野県',
        "lat": 36.6513,
        "lon": 138.1830
    },
    {
        "code": '52586',
        "name": '岐阜',
        "pref": '岐阜県',
        "lat": 35.3912,
        "lon": 136.7223
    },
    {
        "code": '50331',
        "name": '静岡',
        "pref": '静岡県',
        "lat": 34.9786,
        "lon": 138.3831
    },
    {
        "code": '51106',
        "name": '名古屋',
        "pref": '愛知県',
        "lat": 35.1815,
        "lon": 136.9066
    },
    {
        "code": '53133',
        "name": '津',
        "pref": '三重県',
        "lat": 34.7303,
        "lon": 136.5086
    },
    {
        "code": '60131',
        "name": '彦根',
        "pref": '滋賀県',
        "lat": 35.2758,
        "lon": 136.2462
    },
    {
        "code": '61286',
        "name": '京都',
        "pref": '京都府',
        "lat": 35.0116,
        "lon": 135.7681
    },
    {
        "code": '62078',
        "name": '大阪',
        "pref": '大阪府',
        "lat": 34.6851,
        "lon": 135.5059
    },
    {
        "code": '63518',
        "name": '神戸',
        "pref": '兵庫県',
        "lat": 34.6900,
        "lon": 135.1956
    },
    {
        "code": '64036',
        "name": '奈良',
        "pref": '奈良県',
        "lat": 34.6851,
        "lon": 135.8050
    },
    {
        "code": '65042',
        "name": '和歌山',
        "pref": '和歌山県',
        "lat": 34.2260,
        "lon": 135.1675
    },
    {
        "code": '69122',
        "name": '鳥取',
        "pref": '鳥取県',
        "lat": 35.5037,
        "lon": 134.2375
    },
    {
        "code": '68132',
        "name": '松江',
        "pref": '島根県',
        "lat": 35.4723,
        "lon": 132.9851
    },
    {
        "code": '66408',
        "name": '岡山',
        "pref": '岡山県',
        "lat": 34.6617,
        "lon": 133.9180
    },
    {
        "code": '67437',
        "name": '広島',
        "pref": '広島県',
        "lat": 34.3963,
        "lon": 132.4607
    },
    {
        "code": '81428',
        "name": '下関',
        "pref": '山口県',
        "lat": 33.9576,
        "lon": 130.9355
    },
    {
        "code": '71106',
        "name": '徳島',
        "pref": '徳島県',
        "lat": 34.0735,
        "lon": 134.5594
    },
    {
        "code": '72086',
        "name": '高松',
        "pref": '香川県',
        "lat": 34.3403,
        "lon": 134.0470
    },
    {
        "code": '73166',
        "name": '松山',
        "pref": '愛媛県',
        "lat": 33.8416,
        "lon": 132.7661
    },
    {
        "code": '74182',
        "name": '高知',
        "pref": '高知県',
        "lat": 33.5597,
        "lon": 133.5311
    },
    {
        "code": '82182',
        "name": '福岡',
        "pref": '福岡県',
        "lat": 33.5904,
        "lon": 130.4017
    },
    {
        "code": '85142',
        "name": '佐賀',
        "pref": '佐賀県',
        "lat": 33.2494,
        "lon": 130.2975
    },
    {
        "code": '84496',
        "name": '長崎',
        "pref": '長崎県',
        "lat": 32.7448,
        "lon": 129.8738
    },
    {
        "code": '86141',
        "name": '熊本',
        "pref": '熊本県',
        "lat": 32.8033,
        "lon": 130.7089
    },
    {
        "code": '83216',
        "name": '大分',
        "pref": '大分県',
        "lat": 33.2381,
        "lon": 131.6000
    },
    {
        "code": '87376',
        "name": '宮崎',
        "pref": '宮崎県',
        "lat": 31.9111,
        "lon": 131.4239
    },
    {
        "code": '88317',
        "name": '鹿児島',
        "pref": '鹿児島県',
        "lat": 31.5602,
        "lon": 130.5581
    },
    {
        "code": '91197',
        "name": '那覇',
        "pref": '沖縄県',
        "lat": 26.2124,
        "lon": 127.6809
    }
]

# 都道府県名を英語に変換する辞書
pref_translations = {
    "北海道": "Hokkaido",
    "青森県": "Aomori",
    "岩手県": "Iwate",
    "秋田県": "Akita",
    "山形県": "Yamagata",
    "宮城県": "Miyagi",
    "福島県": "Fukushima",
    "茨城県": "Ibaraki",
    "栃木県": "Tochigi",
    "群馬県": "Gunma",
    "埼玉県": "Saitama",
    "千葉県": "Chiba",
    "東京都": "Tokyo",
    "神奈川県": "Kanagawa",
    "新潟県": "Niigata",
    "富山県": "Toyama",
    "石川県": "Ishikawa",
    "福井県": "Fukui",
    "山梨県": "Yamanashi",
    "長野県": "Nagano",
    "岐阜県": "Gifu",
    "静岡県": "Shizuoka",
    "愛知県": "Aichi",
    "三重県": "Mie",
    "滋賀県": "Shiga",
    "京都府": "Kyoto",
    "大阪府": "Osaka",
    "兵庫県": "Hyogo",
    "奈良県": "Nara",
    "和歌山県": "Wakayama",
    "鳥取県": "Tottori",
    "島根県": "Shimane",
    "岡山県": "Okayama",
    "広島県": "Hiroshima",
    "山口県": "Yamaguchi",
    "徳島県": "Tokushima",
    "香川県": "Kagawa",
    "愛媛県": "Ehime",
    "高知県": "Kochi",
    "福岡県": "Fukuoka",
    "佐賀県": "Saga",
    "長崎県": "Nagasaki",
    "熊本県": "Kumamoto",
    "大分県": "Oita",
    "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima",
    "沖縄県": "Okinawa"
}

# 元のHTMLファイル
with open("index.html", "r", encoding="utf-8") as f:
    original_html = f.read()

# 各都道府県のHTMLファイルを生成
for station_data in station_data_list:
    # 英語の都道府県名を取得
    english_pref = pref_translations.get(station_data['pref'], station_data['pref'])

    # フォルダ名を作成（例: wbgt_shimane）
    safe_folder = f"wbgt_{english_pref.lower()}"
    safe_folder = safe_folder.replace(' ', '_')

    # フォルダがなければ作成
    if not os.path.exists(safe_folder):
        os.makedirs(safe_folder)

    # ファイル名に使用できない文字をアンダースコアに置換
    safe_english_pref = re.sub(r"[^a-zA-Z0-9_]", "_", english_pref)
    
    # ファイル名を生成（例: index.html）
    filename = "index.html"
    
    # 出力先パス
    output_path = os.path.join(safe_folder, filename)

    # stationDataの値を置換
    modified_html = original_html.replace(
        '/* 他の都道府県データ*/\n    const stationData = {',
        '    /* 他の都道府県データ*/\n    const stationData = {'
    )
    modified_html = modified_html.replace(
        "code: '14163',",
        f"code: '{station_data['code']}',"
    )
    modified_html = modified_html.replace(
        "name: '札幌',",
        f"name: '{station_data['name']}',"
    )
    modified_html = modified_html.replace(
        "pref: '北海道',",
        f"pref: '{station_data['pref']}',"
    )
    modified_html = modified_html.replace(
        "lat: 43.0645,",
        f"lat: {station_data['lat']},"
    )
    modified_html = modified_html.replace(
        "lon: 141.3468",
        f"lon: {station_data['lon']}"
    )

    # ファイルを保存
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(modified_html)
    print(f"ファイル '{output_path}' が生成されました")