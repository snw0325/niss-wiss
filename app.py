from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('yNJ0FKXfiEMZcQTeGFBZVe3DHm/PSdRw1h1WU8VoABuZplyFFlcCOHpXrdYHzdp3MIZyTtKWptP1IfN0+cwiVhEY45TMyGzRytvN7Pb5gXNshpvU+3pK9OG0m2PYaALeOjjCObV4Uc7yD4vOnOluOQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('92d7e646b4f0872de0126ea1f3beda21')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

def KeyWord(text):
    KeyWordDict = {"納克":"暴擊流- 獸魂",
                  "中路":"圖倫",
                  "邊線":"瑞克"}
    for k in KeyWordDict.keys():
        if text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]

def Button(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://github.com/snw0325/niss-wiss/blob/master/33a89ece71e46ed35f738321ec8d62fa1486014888.jpg?raw=true',
            title='攻略',
            text='Nakroth',
             actions=[PostbackTemplateAction(label='坦裝',text='野斧',data='還沒'),
                MessageTemplateAction(label='爆擊流',text='聖劍'),
                URITemplateAction(label='全裝備網',uri='https://moba.garena.tw/game/props')]
         )
    )
    line_bot_api.reply_message(event.reply_token, message)

 
def Reply(event):
    Ktmp = KeyWord(event.message.text)
    if Ktmp[0]:
        line_bot_api.reply_message(event.reply_token,
             TextSendMessage(text = Ktmp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,
             TextSendMessage(text = event.message.text))

def Reply(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "Ue129a6e5ffff890a19d2a4d97ed2974d":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
    else:
        Ktemp = KeyWord(event)
        if Ktemp[0]:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = Ktemp[1]))
        else:
            line_bot_api.reply_message(event.reply_token,
                Button(event))

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
        line_bot_api.push_message("Ue129a6e5ffff890a19d2a4d97ed2974d", TextSendMessage(text=event.source.user_id))
        line_bot_api.push_message("Ue129a6e5ffff890a19d2a4d97ed2974d", TextSendMessage(text=event.message.text))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        #Reply(event)
        Button(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,
             TextSendMessage(text=str(e)))


@handler.add(PostbackEvent)
def handle_postback(event):
    command = enent.postback.data.split(",")
    if command[0] == "還沒":
        line_bot_api.reply_message(event.reply_token,
            TextMessage(text="還沒就快去練習"))
        line_bot_api.push_message(event.source.user_id, TextSendMessage(text="12345678"))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)