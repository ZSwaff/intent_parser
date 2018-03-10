"""This module includes a model to compare inputs against skills with equality."""

import re


class EqualityModel:
    def __init__(self):
        pass

    def train(self, skills):
        """Prepares the model.

        :param skills: The skills to train on.

        :return: None.
        """
        pass

    def predict(self, skills, user_input, is_mention):
        """Predicts matching skills, if any.

        :param skills: The skills to evaluate against.
        :param user_input: The user's input string.
        :param is_mention: Whether this was a direct mention input.

        :return: The predictions.
        """
        str_matches = []
        re_matches = []

        for skill in skills:
            for action in skill['actions']:
                for trigger in action['triggers']:
                    if trigger['requiresMention'] and not is_mention:
                        continue

                    if trigger['isRegex']:
                        if re.search(trigger['text'], user_input) is not None:
                            re_matches.append({
                                'skillId': skill['exportId'],
                                'actionId': action['exportId']
                            })
                        continue

                    if trigger['text'] in user_input:
                        str_matches.append({
                            'skillId': skill['exportId'],
                            'actionId': action['exportId']
                        })

        prob_str_matches = 1.0 / len(str_matches)
        return [dict(e, probability=prob_str_matches, matchedByRegex=False) for e in str_matches] + \
               [dict(e, probability=1.0, matchedByRegex=True) for e in re_matches]
