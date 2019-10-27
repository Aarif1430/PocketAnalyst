from PIL import Image, ImageDraw, ImageFont
from iexfinance.stocks import Stock
import io
import plotly.graph_objects as go

import requests

BG_WIDTH = 1000
BG_HEIGHT = 1000
IEX_TOKEN = "sk_e4b122da6af4409fb2b69a760f8d2137"


def bebas_font(font_size):
    return ImageFont.truetype('bebas_neue.ttf', font_size)


def generate_stock_info_image(ticker):

    stock = Stock(ticker, token=IEX_TOKEN)
    stock_data = stock.get_historical_prices()

    date = [entry["date"] for entry in stock_data]
    close = [entry["close"] for entry in stock_data]

    today_change = stock_data[-1]["change"]
    today_change_percent = stock_data[-1]["changePercent"]
    today_price = str(stock_data[-1]["close"])
    company = stock.get_company()
    company_name = company["companyName"]
    exchange_name = company["exchange"]

    fig = go.Figure(data=[go.Scatter(x=date, y=close)], layout=go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                    ))
    chart_img_bytes = fig.to_image(format="png", height=450, width=825)
    chart_img = Image.open(io.BytesIO(chart_img_bytes))
    chart_img.save('chart.png')

    logo_img_bytes = requests.get(stock.get_logo()['url']).content
    logo_img = Image.open(io.BytesIO(logo_img_bytes))
    logo_img = logo_img.resize((100, 100), resample=Image.BICUBIC)

    if today_change > 0:
        bg_img = Image.open("up.png")
        change = "+" + str(round(today_change, 2)) + \
            " (" + str(round(today_change_percent, 2)) + "%)"
        change_color = "#0f9d58"
    else:
        bg_img = Image.open("down.png")
        change = "-" + str(round(today_change, 2)) + \
            " (" + str(round(today_change_percent, 2)) + "%)"
        change_color = "#ed1c24"

    bg_w, bg_h = bg_img.size
    chart_w, chart_h = chart_img.size

    d = ImageDraw.Draw(bg_img)
    chart_offset = ((bg_w - chart_w) // 2 - 15, (bg_h - chart_h) // 2 - 15)
    logo_offset = (110, 110)
    bg_img.paste(chart_img, chart_offset, chart_img)
    bg_img.paste(logo_img, logo_offset)
    d.text((230, 130), exchange_name + ": " + ticker,
           font=bebas_font(56), fill="#000000")
    d.text((230, 185), company_name, font=bebas_font(24), fill="#a6a6a6")
    d.text((125, 245), today_price, font=bebas_font(60), fill="#000000")
    d.text((270, 270), "USD", font=bebas_font(24), fill="#a6a6a6")
    d.text((165, 310), change, font=bebas_font(24), fill=change_color)
    bg_img.save('pil_text_font.png')

def generate_portfolio_chart_image(pairs):
    labels = []
    vals = []
    for key in pairs:
        if key != "USD":
            labels.append(key)
            vals.append(pairs[key])
    fig = go.Figure(data=[go.Pie(labels=labels, values=vals)])
    chart_img_bytes = fig.to_image(format="png", height=450, width=825)
    chart_img = Image.open(io.BytesIO(chart_img_bytes))
    chart_img.save('stonk_piechart.png')
    chart_img.show()


if __name__ == "__main__":
    generate_stock_info_image("TSLA")
    generate_stock_info_image("AAPL")
    generate_stock_info_image("FB")
    generate_stock_info_image("UBER")
