import json
import os
import re
import urllib
import datetime

from slacktoarena.utils.constants import PROJECT_PATH


def parse_slack_export(input_path, save_links=True, save_files=False, save_path=None):
    """
    parses a slack export found at input_path
    and returns
    :param save_files:
    :param save_links:
    :param input_path: string path to location of slack export
    :return: None
    """
    print('++ parsing slack export at location: {}'.format(input_path))

    links_dict = None
    if save_links:
        links_dict = parse_links_from_slack_export(input_path=input_path)

    if save_files:
        save_files_from_slack_export(input_path=input_path, save_path=save_path)

    # return
    return links_dict


def get_channels(input_path):
    """
    gets a list of channel names from the slack export
    :param input_path: string path to location of slack export
    :return: list of channel names
    """
    # there is a folder for each channel in the slack export
    return [d for d in os.listdir(input_path)
                if os.path.isdir(os.path.join(input_path, d))]


def get_messages_from_channel(input_path, channel):
    """
    get a list of messages (as dictionaries) from a channel
    :param input_path: string path to location of slack export
    :param channel: string name of channel
    :return: list of message dictionaries
    """
    messages = []
    channel_dir_path = os.path.join(input_path, channel)
    for day in sorted(os.listdir(channel_dir_path)):
        with open(os.path.join(channel_dir_path, day)) as f:
            try:
                day_messages = json.load(f)
                messages += day_messages
            except:
                print('++ failed to read json for: {} | {}'.format(channel, day))
    return messages


def parse_links_from_slack_export(input_path):
    """
    returns a dictionary of channels (where all values are lists of links found in that channel)
    :param input_path: string path to location of slack export
    :return: dictionary of channels
    """

    # get the channels from the input_path
    channels = get_channels(input_path)

    # this dictionary will be populated as we iterate through the channels
    channel_links_dict = {}

    # iterate through the channels getting links from messages
    for channel in channels:
        messages = get_messages_from_channel(input_path, channel)
        for message in messages:
            channel_links = channel_links_dict.setdefault(channel, set([]))
            msg = message.get('text')
            if msg:
                for match in re.findall('<([^>]*)>', msg):
                    if 'http' in match:
                        channel_links.add(match)
    # return dictionary of channels (where all values are lists of links found in that channel)
    return channel_links_dict


def save_files_from_slack_export(input_path, save_path):
    """
    finds all images in slack export, and saves them to save_path
    :param input_path: string path to slack export
    :param save_path: string output path
    :return:
    """
    # get the channels from the input_path
    channels = get_channels(input_path)

    msg_types = set([])
    msg_dates = set([])
    # iterate through the channels getting links from messages
    for channel in channels:
        messages = get_messages_from_channel(input_path, channel)
        for message in messages:
            attachment = message.get('file')
            msg_type = message.get('type')
            msg_date = datetime.datetime.fromtimestamp(int(float(message['ts'])))
            msg_types.add(msg_type)
            if attachment:
                msg_dates.add(msg_date)
                # permalink = attachment.get('permalink_public')
                img_link = attachment.get('url_private_download')
                img_name = attachment.get('name')
                if img_link:
                    print('++ downloading: {}'.format(img_link))
                if not img_link:
                    print('++ warning did not find img_link for: {}'.format(img_name))
                img_id = attachment['id']
                filetype = attachment['filetype']
                output_path = os.path.join(save_path, '{}.{}'.format(img_id, filetype))
                print('++ found file: {}'.format(attachment))
                try:
                    if not os.path.exists(output_path):
                        urllib.request.urlretrieve(img_link, output_path)
                    else:
                        print('++ already found: {} at location {}'.format(img_name, output_path))
                except Exception as e:
                    print('++ error: failed to download image for: {} ({})'.format(img_name, img_id))
        print('++ finished downloading all images')
        min_date = min(msg_dates)
        print('++ earliest date: {}'.format(min_date.strftime('%Y-%m-%d %H:%M:%S')))
        print('++ found msg_types: {}'.format(msg_types))

def copy_images_to_folder(input_path, save_path, output_path):
    """
    copy all image files to output location
    :param input_path:
    :param save_path:
    :param output_path:
    :return:
    """
    # get the channels from the input_path
    channels = get_channels(input_path)

    # iterate through the channels getting links from messages
    for channel in channels:
        messages = get_messages_from_channel(input_path, channel)
        for message in messages:
            attachment = message.get('file')
            if attachment:
                img_name = attachment.get('name').replace(' ', '_')
                img_id = attachment['id']
                filetype = attachment['filetype']
                img_input_path = os.path.join(save_path, '{}.{}'.format(img_id, filetype))
                if not os.path.exists(img_input_path):
                    print('++ image not found: {}'.format(img_input_path))
                else:
                    channel_path = os.path.join(output_path, channel)
                    if not os.path.exists(channel_path):
                        os.makedirs(channel_path)
                    img_output_path = os.path.join(channel_path, img_name)
                    cp_cmd = 'cp "{}" "{}"'.format(img_input_path, img_output_path)
                    print(cp_cmd)
                    os.system(cp_cmd)


if __name__ == '__main__':
    data_dir = os.path.abspath(os.path.dirname(PROJECT_PATH))
    # input_dir = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016')
    input_dir = os.path.join(data_dir, 'darkslack/darkslack_export')
    save_path = os.path.join(data_dir, 'darkslack/images')
    output_path= '/Users/maxfowler/Dropbox/share/darkslack_images'
    parse_slack_export(input_dir, save_path=save_path)
    # copy_images_to_folder(input_path=input_dir, save_path=save_path, output_path=output_path)