#! /usr/bin/env python

import argparse
import json
import logging
import sys

import requests
import concurrent.futures

from tabulate import tabulate


logging.basicConfig(
    level=logging.INFO,
    format=('%(asctime)s [%(process)d] [%(levelname)s] %(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S'
)
LOGGER = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def arguments():
    '''
    Init argparer and parse arguments.
    '''
    parser = argparse.ArgumentParser(
        description='''Check status endpoing of servers specified in file.  Will output statistics
            via stdout, and more detailed information in status.json'''
        )

    parser.add_argument('-f', '--file', action='store', dest='filename', type=str)
    parser.add_argument('-t', '--threads', action='store', dest='threads', default=100, type=int)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False)

    args = parser.parse_args()

    if not args.filename:
        print('You must supply a file containing the servers to check.')
        parser.print_help()
        sys.exit(1)
    return args


class StatusCheck(object):
    def __init__(self, filename, threads, verbose):
        self.applications = {}
        self.collected_status = []
        self.output = {}
        self.threads = threads
        self.verbose = verbose
        self._get_server_list(filename)

    def _get_app_version(self, app, version):
        '''
        Return or create the app / version data structure.
        '''
        if app not in self.output:
            self.output[app] = {}
        if version not in self.output[app]:
            self.output[app][version] = {
                'Request_Count': 0,
                'Error_Count': 0,
                'Success_Count': 0
            }
        return self.output[app][version]

    def _get_server_list(self, filename):
        '''
        Read in list of servers from specified files.

        Sets self.servers on the class.
        '''
        with open(filename) as file_in:
            self.servers = file_in.read().split('\n')

    def _poll_server_status(self, server):
        '''
        Poll the specified server on the /status endpoint.

        Appends dict containing Host and json response to self.collected_status, this is used
        for outputing a json file of the responses.

        Creates the self.output structure and populates.  Used for creating human friendly
        output to stdout.
        '''
        url = 'http://{0}/status'.format(server)
        try:
            response = requests.get(url)
            if response.ok:
                try:
                    status = response.json()
                    status['Host'] = server
                    self.collected_status.append(status)
                    app_ver = self._get_app_version(status['Application'], status['Version'])
                    app_ver['Request_Count'] += status['Request_Count']
                    app_ver['Error_Count'] += status['Error_Count']
                    app_ver['Success_Count'] += status['Success_Count']
                    if self.verbose:
                        LOGGER.info(status)
                except json.decoder.JSONDecodeError:
                    LOGGER.debug('Unable to parse json response from %s', url)
            else:
                LOGGER.info('Server %s returned status code: %s', server, response.status_code)
        except requests.exceptions.ConnectionError:
            LOGGER.info('Server %s failed to connect.', server)

    def gather_servers_status(self):
        '''
        Parallel process the polling of all servers in the list.
        '''
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as pool:
            pool.map(self._poll_server_status, self.servers)

    def write_to_disk(self):
        '''
        Write the raw responses to disk.
        '''
        with open('status_output.json', 'w') as file_out:
            json.dump(self.collected_status, file_out)


def cli():
    args = arguments()
    status = StatusCheck(args.filename, args.threads, args.verbose)
    status.gather_servers_status()
    status.write_to_disk()

    for app in sorted(status.output.keys()):
        table = [[app, 'Requests', 'Success', 'Errors']]
        for version in sorted(status.output[app].keys()):
            count = status.output[app][version]
            table.append(
                [version, count['Request_Count'], count['Success_Count'], count['Error_Count']]
            )
        print(tabulate(table))
