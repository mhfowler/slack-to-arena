from slackarchiver.archive_util import extract_archive, get_users, get_channels, compile_channels



def archive_util_slack_export(input_file):
    print '++ parsing slack export: {}'.format(input_file)
    # path = extract_archive(input_file)
    path = '/tmp/_slackviewer/e3e1eb8b99f78912ddc9b273f2b52613537d19b6/sfpc_slack_export_nov14-2016'
    user_data = get_users(path)
    channel_data = get_channels(path)
    channels = compile_channels(path, user_data, channel_data)
    for channel, channel_data in channels.items():
        print channel