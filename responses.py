import requests,json
from flask import Flask, request, make_response, jsonify


def next (mongodb_saved):
    return message(mongodb_saved=mongodb_saved)

def message (text='',page='',mongodb_saved={}):
    fulfillmentResponse = {
        "fulfillmentResponse": {
            "messages": [{
                "text": {
                    "text": [
                        text
                    ]
                },
            }
            ]
        },
        "target_page": page
    }
    if page == '':
        fulfillmentResponse.update({"sessionInfo": {
            "parameters": {"mongodb_saved":mongodb_saved}
        }})

    return jsonify(fulfillmentResponse)


def chips(choices,page=''):
    options=[]
    for i in choices:
        options.append({"text":i})
    fulfillmentResponse = {
        "fulfillmentResponse": {
            "messages": [
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "type": "chips",
                                    "options": options
                                }
                            ]
                        ]
                    }
                }
            ]
        },
        "target_page": page
    }
    return jsonify(fulfillmentResponse)
