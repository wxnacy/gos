#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
from goss.app import utils
from goss.app.config import goss_config
from goss.app.logger import Logger
import configparser
import os
import pyperclip

logger = Logger()

github = None
owner = None
repo = None

def init_git_config():
    '''初始化 git 信息'''
    credential_path = utils.GOSS_CREDENTIAL_PATH

    config_path = utils.GOSS_CONFIG_PATH

    if not os.path.exists(credential_path):
        return None, ''

    credential = configparser.ConfigParser()
    credential.read(credential_path)
    default_cred = credential['default']

    g = Github(default_cred['user'], default_cred['password'])

    config = configparser.ConfigParser()
    config.read(config_path)
    author = config['user']
    g.set_author(author['name'], author['email'])

    global owner
    owner = credential['default']['owner']

    return g

def create(filepath, path=None, repo=None, yes=False):
    '''
    创建文件
    '''
    g = init_git_config()
    if not path:
        conf_path = goss_config.get_value('repo', 'path')
        if conf_path:
            path = conf_path

    if not path:
        path = os.path.basename(filepath)

    if path.endswith('/'):
        path += os.path.basename(filepath)

    config = configparser.ConfigParser()
    config.read(utils.GOSS_CONFIG_PATH)
    if not repo:
        repo = config['repo']['name']

    logger.info('Upload file')
    logger.info('Source\t:', filepath)
    logger.info('Path\t:', path)
    download_url = 'https://raw.githubusercontent.com/{}/{}/master/{}'.format(
        owner, repo, path
    )
    html_url = 'https://github.com/{}/{}/blob/master/{}'.format(
        owner, repo, path
    )
    logger.info('HtmlUrl\t:', html_url)
    logger.info('DownUrl\t:', click.style(download_url, fg='blue'))
    pyperclip.copy(download_url)
    logger.info('Now you can use it with {} and wait for the upload to succeed.'.format(
        click.style('<Ctrl-v>', fg='blue')
    ))
    logger.info('Waiting...')

    if filepath.startswith('http'):
        default_create = g.create_file_from_url
    else:
        default_create = g.create_file_from_path

    code, data = default_create(owner, repo, filepath, path)
    if code == 404:
        utils.print_failed()
        logger.error('Repository Owner or Name not found', with_color=True)
        return

    # 如果文件已经存在，则询问是否覆盖
    if code == 422 and data.get("message") == \
            'Invalid request.\n\n"sha" wasn\'t supplied.':
        if not yes:
            if not click.confirm('This file is exists. Do you want to replace?'):
                return
        else:
            logger.warn('This file already exists and is now replaced',
                    with_color=True)

        logger.info('Waiting...')
        code, data = g.get_file(owner, repo, path)
        sha = data['sha']
        code, data = default_create(owner, repo, filepath, path, sha)

        if code != 200:
            utils.print_failed()
            utils.print_error(data['message'])
            return
    utils.print_success()

@click.command()
@click.option('--repo', '-r', help='Github repository name')
@click.option('--path', '-p', help='Github repository file path')
@click.option('--yes', '-y', is_flag = True, default = False, help = 'All questions answered yes')
#  @click.argument('filepath', type=click.Path(exists=True))
@click.argument('filepath')
def run(filepath, path, repo, yes):
    '''
    Github Object Storage System
    '''
    create(filepath, path, repo, yes)
    pass

if __name__ == "__main__":
    run()
