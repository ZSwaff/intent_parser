#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module encapsulates a Flask server for the intent parser."""

from flask import Flask, request, json

from EqualityModel import EqualityModel


def build_app():
    """Build the application.

    :return: The app.
    """
    app = Flask(__name__)

    model_type_store = {'equality': EqualityModel}
    model_store = {}
    skills_store = {}

    def __get_model_types():
        return model_type_store.keys()

    def __train(team, model_type, skills):
        if team not in model_store:
            model_store[team] = {}
        model = model_type_store[team]()
        model.train(skills)
        model_store[team][model_type] = model

    def __predict(team, model_type, user_input, is_mention):
        if team not in model_store:
            return 'Team not found', 404
        if model_type not in model_store[team]:
            return 'Team model not found', 404

        model = model_store[team][model_type]
        skills = skills_store[team]
        return model.predict(skills, user_input, is_mention)

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

        skills = body['skills']
        for model_type in model_type_store.keys():
            __train(team, model_type, skills)

        skills_store[team] = skills

        return 'Success'

    @app.route(make_url('/predict/<team>/<model_type>'), methods=['GET'])
    def predict_action(team, model_type):
        """Predicts which action(s) are matched by a given input.

        :param team: The team id.
        :param model_type: The model to use to predict the action.

        :return: The predicted action.
        """
        user_input = request.args.get('input')
        if user_input is None:
            return 'Missing \'input\' query arg', 400

        is_mention = request.args.get('isMention')
        if is_mention is None:
            return 'Missing \'isMention\' query arg', 400

        return json.dumps({
            'prediction_set_id': 0,
            'predictions': __predict(team, model_type, user_input, is_mention)
        })

    @app.route(make_url('/feedback/<prediction_set_id>'), methods=['POST'])
    def provide_feedback(prediction_set_id):
        """Saves user feedback on a given prediction set for future training use.

        :param prediction_set_id: The id of the prediction set.

        :return: Status of the request.
        """
        body = request.get_json()

        # todo save body to database

        return 'Success'

    return app


if __name__ == '__main__':
    build_app().run(host='0.0.0.0', port=80)
