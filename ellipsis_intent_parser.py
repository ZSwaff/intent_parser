#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module encapsulates a Flask server for the ellipsis intent parser."""


from flask import Flask, request, json


def build_app():
    """Build the application.

    :return: The app.
    """

    model_types = ['equality']

    app = Flask(__name__)

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
        return json.dumps({'modelTypes': model_types})

    @app.route(make_url('/train/<team>'), methods=['PUT'])
    def train_model(team):
        """Trains or retrains the specified model for the given team based on possible intents.

        :param team: The team id.
        :return: Status of the request.
        """
        # todo implement
        return 'Success'

    @app.route(make_url('/predict/<team>'), methods=['GET'])
    def predict_intent(team):
        """Predicts which intent(s) are matched by a given input.

        :param team: The team id.
        :return: The predicted intent.
        """
        # todo implement
        return {}

    @app.route(make_url('/feedback/<prediction_id>'), methods=['POST'])
    def provide_feedback(prediction_id):
        """Allows feedback on a given prediction to refine the model.

        :param prediction_id: The id of the prediction to provide feedback on,
        :return: Status of the request.
        """
        # todo implement
        return 'Success'


if __name__ == '__main__':
    build_app().run(host='0.0.0.0', port=5000)
