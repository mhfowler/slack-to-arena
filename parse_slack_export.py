import os
import json
import re

from slackarchiver.hello_settings import PROJECT_PATH


def parse_slack_export(input_path):
    channels = [d for d in os.listdir(input_path)
                if os.path.isdir(os.path.join(input_path, d))]
    channel_links_dict = {}
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
        for channel, channel_links in channel_links_dict.items():
            print '+++++ {}'.format(channel)
            for link in channel_links:
                print link



if __name__ == '__main__':
    data_dir = os.path.abspath(os.path.dirname(PROJECT_PATH))
    input_dir = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016')
    # input_file = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016.zip')
    parse_slack_export(input_dir)