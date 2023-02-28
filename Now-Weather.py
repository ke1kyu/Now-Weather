import requests
from datetime import datetime
import tkinter as tk

# アメダスから情報を取得
def get_weather_info():
    latest_time_url = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"
    latest_time_req = requests.get(latest_time_url)
    latest_datetime = datetime.strptime(latest_time_req.text, "%Y-%m-%dT%H:%M:%S%z")
    date = latest_datetime.strftime('%Y%m%d') # 年月日
    h3 = ("0" + str((latest_datetime.hour//3)*3))[-2:] # 3時間ごとの時間
    stnid = "51106" # 観測所番号（名古屋）

    amedas_url = f"https://www.jma.go.jp/bosai/amedas/data/point/{stnid}/{date}_{h3}.json"
    amedas_req = requests.get(amedas_url)
    amedas_data = amedas_req.json()
    latest_key = max(amedas_data) # 最新のデータが入っているkey
    latest_temp = amedas_data[latest_key]["temp"]
    latest_wind = amedas_data[latest_key]["wind"]
    latest_precipitation10m = amedas_data[latest_key]["precipitation10m"]

    now_str=f"{latest_key[:4]}年{latest_key[4:6]}月{latest_key[6:8]}日 {latest_key[8:10]}:{latest_key[10:12]}" # 年月日
    # ウィンドウ上にラベルを描写
    result_label.configure(text=f"{now_str} 観測時の天気情報\n\n気温 : {latest_temp[0]} 度\n風速 : {latest_wind[0]} m/s\n降水量(10分あたり) : {latest_precipitation10m[0]} mm")

# 更新ボタンを押下した時
def update_weather_info():
    get_weather_info()

# ウィンドウ設定
window = tk.Tk()
window.title("天気情報")
window.geometry("400x260")

# ラベル情報
result_label = tk.Label(window, text="", font=("メイリオ", 12))
result_label.pack(pady=20)

# 更新ボタン
update_button = tk.Button(window, text="更新", font=("メイリオ", 12), command=update_weather_info)
update_button.pack(pady=10)

get_weather_info()

window.mainloop()
