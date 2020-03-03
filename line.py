import cotoha
import json
from codecs import decode
from os import environ, getenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
handler = WebhookHandler(environ["LINE_CHANNEL_SECRET"])
linebot_api = LineBotApi(environ["LINE_CHANNEL_ACCESS_TOKEN"])
cotoha_api = cotoha.CotohaApi()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sentiment = cotoha_api.sentiment(event.message.text)
    reply_message = make_reply_message(sentiment["result"])
    linebot_api.reply_message(event.reply_token, reply_message)

def make_reply_message(sentiment_result):
    positive_words = ""
    negative_words = ""

    for phrase in sentiment_result['emotional_phrase']:
        if phrase['emotion'] == 'P':
            positive_words = positive_words + '・' + phrase['form'] + '\n'
        if phrase['emotion'] == 'N':
            negative_words = negative_words + '・' + phrase['form'] + '\n'

    if len(negative_words) > 0:
        message = "君の文章、相手を不快にする可能性があります。\n以下のワードは使わないでちょ\uDBC0\uDC9E\n" + negative_words
    elif len(positive_words) < 1:
        message = "君の文章、悪くはないです。\nでもポジティブワードを1つは入れてちょ\uDBC0\uDC9D"
    else:
        message = "君の文章、完璧です。\n以下のワードがGood\uDBC0\uDC7F\n" + positive_words

    return TextSendMessage(text=message)

if __name__ == "__main__":
    port = int(getenv("PORT"))
    app.run(host="0.0.0.0", port=port)