#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module encapsulates a Flask server for the ellipsis intent parser."""

from collections import defaultdict

from flask import Flask, request, json


def build_app():
    """Build the application.

    :return: The app.
    """
    app = Flask(__name__)

    model_type_store = ['equality']
    model_store = defaultdict(dict)

    def __get_model_types():
        return model_type_store

    def __train(team, model_type, intents):
        model_store[team][model_type] = intents

    def __predict(team, model_type, inpt):
        model = model_store[team].get(model_type)
        if model is None:
            return 'Team or model not found', 404

        intents = [{'intent': inpt, 'probability': 1.0}] if inpt in model else []

        return {'predictions': intents}

    def make_url(suffix):
        """Makes a URL with the suffix.

        :param suffix: The suffix to add to the base URL.
        :return: The full URL.
        """
        return '/api/v0' + suffix

    @app.route('/health', methods=['GET'])
    def report_health():
        """Returns the health of the endpoint.

        :return: The health.
        """
        return 'OK'

    @app.route(make_url('/model-types'), methods=['GET'])
    def get_model_types():
        """Gets the available model types.

        :return: The model types in JSON.
        """
        return json.dumps({'modelTypes': __get_model_types()})

    @app.route(make_url('/train/<team>'), methods=['PUT'])
    def train_model(team):
        """Trains or retrains the specified model for the given team based on possible intents.

        :param team: The team id.
        :return: Status of the request.
        """
        body = request.get_json()
        model_types = body['modelTypes']
        allowed_model_types = __get_model_types()
        for model_type in model_types:
            if model_type not in allowed_model_types:
                return 'Bad model type: ' + model_type, 400

        intents = body['intents']
        for model_type in model_types:
            __train(team, model_type, intents)
        return 'Success'

    @app.route(make_url('/predict/<team>/<model_type>'), methods=['GET'])
    def predict_intent(team, model_type):
        """Predicts which intent(s) are matched by a given input.

        :param team: The team id.
        :return: The predicted intent.
        """
        inpt = request.args.get('input')
        if inpt is None:
            return 'Missing input query arg', 400

        return __predict(team, model_type, inpt)


if __name__ == '__main__':
    build_app().run(host='0.0.0.0', port=5000)
