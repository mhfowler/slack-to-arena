import requests

from slacktoarena.utils.constants import SECRETS_DICT


def get_arena_code_url():
    url = 'http://dev.are.na/oauth/authorize?' \
          'client_id={client_id}' \
          '&redirect_uri={callback_url}' \
          '&response_type=code'.format(
        client_id=SECRETS_DICT['ARENA_CLIENT_ID'],
        callback_url=SECRETS_DICT['ARENA_CALLBACK_URL']
    )
    print(url)
    # resp = requests.get(url)
    # print(resp)


def get_arena_token(arena_code):
    url = 'https://dev.are.na/oauth/token?' \
               'client_id={client_id}' \
               '&client_secret={client_secret}' \
               '&code={arena_code}' \
               '&grant_type=authorization_code' \
               '&redirect_uri={callback_url}'.format(
        client_secret=SECRETS_DICT['ARENA_CLIENT_SECRET'],
        client_id=SECRETS_DICT['ARENA_CLIENT_ID'],
        callback_url=SECRETS_DICT['ARENA_CALLBACK_URL'],
        arena_code=arena_code
    )
    print(url)
    resp = requests.get(url)
    print(resp)


if __name__ == '__main__':
    # run the following function to see url to visit
    get_arena_code_url()
    # get code and use it to get an arena token
    arena_code = input('enter the arena code: ')
    arena_code = 'd28f396e4726e47e56bd3d729d7c49a61fe89c3153b0cd9e0aed6f151dbf7be1'
    get_arena_token(arena_code=arena_code)