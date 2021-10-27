from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('JBeCGWLzR8V7X25RBiQAB7i4gXgCcao8kkmoY0YzCrRWzIpAO5G1EiL0kuvyOhxrNRYMAPTt0PUuXxbWm1CKK6Q/rGsTAA2VHVF1O2+qrQ1hcsMgac1suemgIaI07BMtYwkd2q041PWK3wV+3V8cxwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('af7ef1c4fed5b04d9e4dc52d257280c0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    
    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message))

        return

    if 'hi' in msg:
        r = "很高興認識你！"
    elif '吃飯' in msg:
        r = '我也要吃飯，帶我一起去'
    else:
        r = '講人話！'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()