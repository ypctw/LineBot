import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()
USER_ID = {}
def createMachine():
    machine = TocMachine(
        states=["user","Start",
                    "Search",
                        "Crypto",
                            "Crypto_Fetch",
                        "Stock",
                            "Stock_US",
                                "Stock_US_Index",
                                    "Stock_US_Index_four",
                                "Stock_US_Individual",
                                    "Stock_US_Fetch",
                            "Stock_TW",
                                "Stock_TW_Fetch",
                    "SMA",
                        "SMA_S","SMA_S_US",
                            "S_Stock","S_Stock_US",
                        "SMA_M","SMA_M_US",
                            "M_Stock","M_Stock_US",
                        "SMA_L","SMA_L_US",
                            "L_Stock","L_Stock_US",
             ],
        transitions=[
            # Start
            {"trigger" : "advance", "source" : "user",  "dest" : "Start",   "conditions" : "is_going_to_Start"},
            # Search #
            {"trigger" : "advance", "source" : "Start", "dest" : "Search",  "conditions" : "is_going_to_Search"},
            ## Search Crypto ##
            {"trigger" : "advance", "source" : "Search","dest" : "Crypto",      "conditions" : "is_going_to_Crypto"},
            {"trigger" : "advance", "source" : "Crypto","dest" : "Crypto_Fetch","conditions" : "is_going_to_Crypto_Fetch"},
            ### Search Crypto Fetch to Start ###
            {"trigger" : "advance", "source" : "Crypto_Fetch","dest" : "Start", "conditions" : "is_going_to_Return_Start"},
            {"trigger" : "advance", "source" : "Crypto_Fetch","dest" : "Crypto", "conditions" : "is_going_to_Return_Crypto"},
            ## Search Stock ##
            {"trigger" : "advance", "source" : "Search","dest" : "Stock",   "conditions" : "is_going_to_Stock"},
            {"trigger" : "advance", "source" : "Stock", "dest" : "Stock_US","conditions" : "is_going_to_Stock_US"},
            {"trigger" : "advance", "source" : "Stock", "dest" : "Stock_TW","conditions" : "is_going_to_Stock_TW"},
            ### Search Stock US Fetch to Start ###
            {"trigger" : "advance", "source" : "Stock_US","dest" : "Stock_US_Index", "conditions" : "is_going_to_Stock_US_Index"},
            {"trigger" : "advance", "source" : "Stock_US","dest" : "Stock_US_Individual", "conditions" : "is_going_to_Stock_US_Individual"},
            ####
            {"trigger" : "advance", "source" : "Stock_US_Index","dest" : "Stock_US_Index_four", "conditions" : "is_going_to_Stock_US_Index_four"},
            {"trigger" : "advance", "source" : "Stock_US_Index_four","dest" : "Start", "conditions" : "is_going_to_Return_Start"},
            {"trigger" : "advance", "source" : "Stock_US_Index_four","dest" : "Stock", "conditions" : "is_going_to_Stock"},
            {"trigger" : "advance", "source" : "Stock_US_Individual","dest" : "Stock_US_Fetch", "conditions" : "is_going_to_Stock_US_Fetch"},
            ##### EXIT
            {"trigger" : "advance", "source" : "Stock_US_Fetch","dest" : "Stock", "conditions" : "is_going_to_Stock"},
            {"trigger" : "advance", "source" : "Stock_US_Fetch","dest" : "Start", "conditions" : "is_going_to_Return_Start"},
            ### Search Stock tw Fetch to NEXT ###
            {"trigger" : "advance", "source" : "Stock_TW","dest" : "Stock_TW_Fetch", "conditions" : "is_going_to_Stock_TW_Fetch"},

            #### Search Stock TW Fetch to Start ####
            {"trigger" : "advance", "source" : "Stock_TW_Fetch","dest" : "Stock", "conditions" : "is_going_to_Stock"},
            {"trigger" : "advance", "source" : "Stock_TW_Fetch","dest" : "Start", "conditions" : "is_going_to_Stock_TW_Fetch_2_End"},

            # From Start into SMA
            {"trigger" : "advance", "source" : "Start", "dest" : "SMA",  "conditions" : "is_going_to_SMA"},
            # From SMA to Short Medium Long

            # From SML to SML_DAYS
            {"trigger" : "advance", "source" : "SMA", "dest" : "SMA_S",  "conditions" : "is_going_to_SMA_S"},
            {"trigger" : "advance", "source" : "SMA", "dest" : "SMA_M",  "conditions" : "is_going_to_SMA_M"},
            {"trigger" : "advance", "source" : "SMA", "dest" : "SMA_L",  "conditions" : "is_going_to_SMA_L"},
            {"trigger" : "advance", "source" : "SMA", "dest" : "SMA_S_US",  "conditions" : "is_going_to_SMA_S_US"},
            {"trigger" : "advance", "source" : "SMA", "dest" : "SMA_M_US",  "conditions" : "is_going_to_SMA_M_US"},
            {"trigger" : "advance", "source" : "SMA", "dest" : "SMA_L_US",  "conditions" : "is_going_to_SMA_L_US"},
            # From S M L to Stock
            {"trigger" : "advance", "source" : "SMA_S", "dest" : "S_Stock",  "conditions" : "is_going_to_S_Stock"},
            {"trigger" : "advance", "source" : "SMA_M", "dest" : "M_Stock",  "conditions" : "is_going_to_M_Stock"},
            {"trigger" : "advance", "source" : "SMA_L", "dest" : "L_Stock",  "conditions" : "is_going_to_L_Stock"},
            {"trigger" : "advance", "source" : "SMA_S_US", "dest" : "S_Stock_US",  "conditions" : "is_going_to_S_Stock_US"},
            {"trigger" : "advance", "source" : "SMA_M_US", "dest" : "M_Stock_US",  "conditions" : "is_going_to_M_Stock_US"},
            {"trigger" : "advance", "source" : "SMA_L_US", "dest" : "L_Stock_US",  "conditions" : "is_going_to_L_Stock_US"},
            # Stock_Analysis
    #         {"trigger" : "advance", "source" : "S_Stock",   "dest" : "Stock_Analysis", "conditions" : "is_going_to_Stock_Analysis"},
    #         {"trigger" : "advance", "source" : "M_Stock",   "dest" : "Stock_Analysis", "conditions" : "is_going_to_Stock_Analysis"},
    #         {"trigger" : "advance", "source" : "L_Stock",   "dest" : "Stock_Analysis", "conditions" : "is_going_to_Stock_Analysis"},
    #         {"trigger" : "advance", "source" : "S_Stock_US","dest" : "Stock_Analysis", "conditions" : "is_going_to_Stock_Analysis"},
    #         {"trigger" : "advance", "source" : "M_Stock_US","dest" : "Stock_Analysis", "conditions" : "is_going_to_Stock_Analysis"},
    #         {"trigger" : "advance", "source" : "L_Stock_US","dest" : "Stock_Analysis", "conditions" : "is_going_to_Stock_Analysis"},
            ## Replay
            {"trigger" : "advance", "source" : "S_Stock",       "dest" : "SMA", "conditions" : "is_going_to_SMA"},
            {"trigger" : "advance", "source" : "M_Stock",       "dest" : "SMA", "conditions" : "is_going_to_SMA"},
            {"trigger" : "advance", "source" : "L_Stock",       "dest" : "SMA", "conditions" : "is_going_to_SMA"},
            {"trigger" : "advance", "source" : "S_Stock_US",    "dest" : "SMA", "conditions" : "is_going_to_SMA"},
            {"trigger" : "advance", "source" : "M_Stock_US",    "dest" : "SMA", "conditions" : "is_going_to_SMA"},
            {"trigger" : "advance", "source" : "L_Stock_US",    "dest" : "SMA", "conditions" : "is_going_to_SMA"},
    #         {"trigger" : "advance", "source" : "Stock_Analysis","dest" : "SMA", "conditions" : "is_going_to_SMA"},
            ## EXIT
            {"trigger" : "advance", "source" : "S_Stock",       "dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},
            {"trigger" : "advance", "source" : "M_Stock",       "dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},
            {"trigger" : "advance", "source" : "L_Stock",       "dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},
            {"trigger" : "advance", "source" : "S_Stock_US",    "dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},
            {"trigger" : "advance", "source" : "M_Stock_US",    "dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},
            {"trigger" : "advance", "source" : "L_Stock_US",    "dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},
    #         {"trigger" : "advance", "source" : "Stock_Analysis","dest" : "Start", "conditions" : "is_going_to_Restart_SMA"},


            ],
        initial="user",
        auto_transitions=False,
    #     show_conditions=True,
    )
    return machine

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)




if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


# @app.route("/callback", methods=["POST"])
# def callback():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     print("-------------------------------------")
#     print("body")
#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue
#
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.message.text)
#         )
#
#     return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        if events.source.user_id not in USER_ID:
            USER_ID[events.source.user_id] = createMachine()
        response = USER_ID[events.source.user_id].advance(event)
        if response == False:
            send_text_message(event.reply_token, "找不到指令\n還是你只是想找我聊天哩")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)