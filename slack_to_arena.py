import sys
import os
import re
from time import sleep

from slacktoarena.utils.constants import PROJECT_PATH, RATE_LIMIT_SLEEP_TIME
from slacktoarena.utils.parse_slack_export import parse_slack_export
from slacktoarena.utils.arena_syncer import ArenaSyncer


def slack_to_arena(path_to_slack_export, arena_username, save_images=False):
    """
    parses a slack export at the given path, and syncs all links found in all channels to the are.na
    of the given username
    :param path_to_slack_export: string path to unzipped slack export
    :param arena_username: string username of are.na user to sync to
    :return: None
    """
    print('++ archiving links from {} to the are.na user {}'.format(path_to_slack_export, arena_username))

    # parse the slack export
    print('++ parsing all the links from the slack export')
    slack_channels_dict = parse_slack_export(input_path=path_to_slack_export, save_files=False)

    # print total number of links
    total_links = 0
    for channel, links in slack_channels_dict.items():
        total_links += len(links)
    print('++ uploading {} links'.format(total_links))

    # initialize are.na api
    print('++ initializing are.na api')
    arena_syncer = ArenaSyncer(username=arena_username)

    # for each channel, sync all of its links to arena
    num_links = 0
    for channel_title, links in slack_channels_dict.items():

        # if the channel was already synced, let's skip it for now
        if arena_syncer.has_channel(channel_title):
            # TODO: figure out what to do here
            pass
            # continue
        # if the channel was not already synced, then sync it
        print('++ saving links for slack channel: {}'.format(channel_title))
        for link in links:

            num_links += 1
            if not num_links % 20:
                completion_percent = (num_links / float(total_links)) * 100
                print('++ {}/{} {}%'.format(num_links, total_links, completion_percent))

            if 'slack.com' in link:
                if save_images:
                    match = re.match('.*slack.com/files/(\S+)/(\S+)/(\S+)', link)
                # TODO: figure out how to handle these
                print('++ skipping {}'.format(link))
                continue
            # clean links with title in the link
            match = re.match('(.*)(\|.*)', link)
            if match:
                print('++ trimming title from link {}'.format(match.group(2)))
                link = match.group(1)
            try:
                arena_syncer.save_link_to_arena(channel_title=channel_title, link=link)
                sleep(RATE_LIMIT_SLEEP_TIME)
            except Exception as e:
                print('++ WW: failed to save link {}'.format(link))


if __name__ == '__main__':

    # boolean flag to parse arguments from CLI or read hardcoded args
    USE_CLI = True

    # parse arguments from command line
    if USE_CLI:
        export_path = sys.argv[1]
        username = sys.argv[2]
    # or hardcode them
    else:
        data_dir = os.path.abspath(os.path.dirname(PROJECT_PATH))
        # export_path = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016')
        # export_path = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016')
        export_path = os.path.join(data_dir, 'darkslack/darkslack_export')
        # export_path = os.path.join(data_dir, 'learning-gardens/Learning Gardens Slack export Feb 10 2018')
        # export_path = os.path.join(data_dir, 'computerlab/computerlab_slack_export_nov11_2016')
        username = 'dark-slack'

    # run the script
    slack_to_arena(path_to_slack_export=export_path, arena_username=username)
