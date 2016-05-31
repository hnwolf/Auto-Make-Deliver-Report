#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR: hieulq

from datetime import datetime, date, timedelta

import gerritssh as gssh
import logging
import optparse
import os
import requests
import sys
import txt2pdf

# LOGGING

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    stream=sys.stderr)

# DEFAULT SETTINGS

PROTO = 'https://'
OWNER = 'hieulq'
GERRIT_HOST = 'review.openstack.org'
GERRIT_PORT = 29418
START_TIME = (date.today() - timedelta(days=7)).isoformat()
OUTPUT = 'Deliver'


def check_date(value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date: %r" % value)


def get_content(patch_url):
    r = requests.get(patch_url)
    if r.ok:
        return r.content


def create_file(project_name, bug_name, patch_url, patch_num=1):
    filename = '%s_%s_PS%s.txt' % (project_name, bug_name, patch_num)
    LOG.info('|_______ Getting patch: %s', patch_num)
    while True:
        try:
            with open(filename, 'w+') as f:
                f.write(get_content(patch_url))
        except TypeError:
            LOG.error('Failed to get PS raw data! Retrying..')
            continue
        break
    outfile = txt2pdf.convert(filename)
    os.remove(filename)
    LOG.info('|_______ Finish creating: %s', outfile)


def create_folder(project_name, topic):
    folder_name = '%s_%s' % (project_name, topic)
    directory = "%s/Patches" % folder_name
    if not os.path.exists(directory):
        LOG.info('|_______ Create folder: %s', folder_name)
        os.makedirs(directory)
    else:
        LOG.info('|_______ Folder %s existed!', folder_name)
    return directory


def get_topic_name(ps):
    msg = ps.raw['commitMessage']
    change = ps.number
    if 'Closes-Bug: #' in msg:
        return 'bug_%s' % msg.split('Closes-Bug: #')[1].rstrip()
    elif 'Closes-bug: #' in msg:
        return 'bug_%s' % msg.split('Closes-bug: #')[1].rstrip()
    elif 'Partial-Bug: #' in msg:
        return (
            'bug_%s' % msg.split('Partial-Bug: #')[1].rstrip(),
            'patch_%s' % change
        )
    elif 'Partial-bug: #' in msg:
        return (
            'bug_%s' % msg.split('Partial-bug: #')[1].rstrip(),
            'patch_%s' % change
        )
    elif 'blueprint ' in msg:
        return (
            'bp_%s' % msg.split('blueprint ')[-1].splitlines()[0].rstrip(),
            'patch_%s' % change
        )
    elif 'bp:' in msg:
        return (
            'bp_%s' % msg.split('bp:')[-1].splitlines()[0].rstrip(),
            'patch_%s' % change
        )
    else:
        return 'patch_%s' % change


def main():
    parser = optparse.OptionParser(usage="usage: %prog [options]",
                                   version="%prog 1.0")
    parser.add_option("-o", "--owner", dest="owner", action='store',
                      help="gerrit pwner [default: %default]", metavar="OWNER",
                      default=OWNER)
    parser.add_option("-s", "--server", dest="server", action='store',
                      help="gerrit server [default: %default]",
                      metavar="SERVER", default=GERRIT_HOST)
    parser.add_option("-p", "--port", dest="port", action='store',
                      type="int", help="gerrit port [default: %default]",
                      metavar="PORT", default=GERRIT_PORT)
    parser.add_option("--start-time", dest="start_time", action='store',
                      type="string", help="start time for querrying in "
                                          "gerrit, in format: YYYY-MM-DD",
                      metavar="STARTTIME", default=START_TIME)
    parser.add_option("-k", "--keyfile", dest="keyfile", action='store',
                      help="gerrit ssh keyfile [default: use local keyfile]",
                      metavar="FILE", default=None)
    (options, args) = parser.parse_args()
    check_date(options.start_time)
    owner = options.owner
    start_time = options.start_time
    port = options.port
    server = options.server
    keyfile = options.keyfile

    rsite = gssh.Site(server, owner, port, keyfile).connect()
    plist = gssh.Query('--commit-message',
                       'owner:' + owner +
                       ' AND (status:merged OR status:pending)' +
                       ' since:' + start_time).execute_on(rsite)
    LOG.info("| Total gerrit results: %d", len(plist))

    # Create delivery folder
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    if OUTPUT.startswith('/'):
        root_dir = OUTPUT
    else:
        root_dir = "/".join([os.getcwd(), OUTPUT])

    for p in plist:
        LOG.info("|_ Generating doc from gerrit patch: %s ", p.number)
        os.chdir(root_dir)

        project_name = '[' + p.repo_name.split('/')[-1] + ']'
        topic = get_topic_name(p)
        pss = p.patchsets
        patch_urls = {}
        for num, ps in pss.iteritems():
            patch_urls[num] = PROTO + GERRIT_HOST + \
                '/gitweb?p=' + p.repo_name + \
                '.git;a=patch;h=' + \
                ps.raw['revision']

        LOG.info('|____ Project: %s', project_name)
        LOG.info('|____ Topic: %s', topic)
        LOG.info('|____ PS count: %s', len(patch_urls))
        if isinstance(topic, tuple):
            directory = create_folder(project_name, topic[0])
            os.chdir("/".join([os.getcwd(), directory]))
            topic = topic[1]
        if len(patch_urls) == 1:
            create_file(project_name, topic, patch_urls[1])
        else:
            directory = create_folder(project_name, topic)
            os.chdir("/".join([os.getcwd(), directory]))
            for patch_num, patch_url in patch_urls.iteritems():
                create_file(project_name, topic, patch_url, patch_num)
    LOG.info("|_ FIN!")


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    main()
