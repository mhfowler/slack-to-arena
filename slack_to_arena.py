import sys
import os

from slacktoarena.utils.constants import PROJECT_PATH
from slacktoarena.utils.parse_slack_export import parse_slack_export
from slacktoarena.utils.arena_syncer import ArenaSyncer


def slack_to_arena(path_to_slack_export, arena_username):
    """

    :param path_to_slack_export:
    :param arena_username:
    :return:
    """
    print('++ archiving links from {} to the are.na user {}'.format(path_to_slack_export, arena_username))

    # parse the slack export
    print('++ parsing all the links from the slack export')
    slack_channels_dict = parse_slack_export(path_to_slack_export)

    # initialize are.na api
    print('++ initializing are.na api')
    arena_syncer = ArenaSyncer(username=arena_username)

    # for each channel, sync all of its links to arena
    for channel_title, links in slack_channels_dict.items():
        print('++ saving links for slack channel: {}'.format(channel_title))
        for link in links:
            try:
                arena_syncer.save_link_to_arena(channel_title=channel_title, link=link)
            except:
                print('++ WW: failed to save link {}'.format(link))


if __name__ == '__main__':

    # boolean flag to parse arguments from CLI or read hardcoded args
    USE_CLI = False

    # parse arguments from command line
    if USE_CLI:
        export_path = sys.argv[1]
        username = sys.argv[2]
    # or hardcode them
    else:
        data_dir = os.path.abspath(os.path.dirname(PROJECT_PATH))
        export_path = os.path.join(data_dir, 'sfpc/sfpc_slack_export_nov14-2016')
        username = 'sfpc-arena'

    # run the script
    slack_to_arena(path_to_slack_export=export_path, arena_username=username)
