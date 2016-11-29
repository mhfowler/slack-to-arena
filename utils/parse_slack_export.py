import json
import os
import re

from slacktoarena.utils.constants import PROJECT_PATH


def parse_slack_export(input_path):
    """
    parses a slack export found at input_path
    and returns
    :param input_path: string path to location of slack export
    :return:
    """
    print('++ parsing slack export at location: {}'.format(input_path))

    # there is a folder for each channel in the slack export
    channels = [d for d in os.listdir(input_path)
                if os.path.isdir(os.path.join(input_path, d))]

    # this dictionary will be populated as we iterate through the channels
    channel_links_dict = {}

    # iterate through channels looking for links
    for channel in channels:
        channel_links = set([])
        channel_links_dict[channel] = channel_links
        channel_dir_path = os.path.join(input_path, channel)
        for day in sorted(os.listdir(channel_dir_path)):
            with open(os.path.join(channel_dir_path, day)) as f:
                day_messages = json.load(f)
                for message in day_messages:
                    msg = message.get('text')
                    if msg:
                        for match in re.findall('<(\S+)>', msg):
                            if 'http' in match:
                                channel_links.add(match)

        # return dictionary of channels (where all values are lists of links found in that channel)
        return channel_links_dict


if __name__ == '__main__':
    data_dir = os.path.abspath(os.path.dirname(PROJECT_PATH))
    input_dir = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016')
    parse_slack_export(input_dir)