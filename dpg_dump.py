#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# The MIT License (MIT)

# Copyright (c) 2015 Augustin Cisterne-Kaas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################
from docker_postgres_client import Client
import os


class PgDump(Client):

    def parser(self):
        parser = super(PgDump, self).parser()
        parser.add_argument('database', help="Database name")
        parser.add_argument('-f', '--file', help="Exported file name")
        parser.add_argument('-o', '--clean-odoo-db',
                            help="Clean Odoo Database With Optional Query File")
        return parser

    def docker_cmd(self):
        res = super(PgDump, self).docker_cmd()
        pwd = os.getcwd()
        res.append('--volume %s:/tmp' % pwd)
        return res

    def container_cmd(self):
        # mount a volume if a file is passed as argument
        args = self.args
        res = []
        if args.clean_odoo_db:
            res = \
                ["psql -h db -p %s -U %s -d %s "
                 "-c 'CREATE DATABASE duplicate_db "
                 "WITH TEMPLATE %s OWNER %s;' &&" % (
                    args.port,
                    args.user,
                    args.database,
                    args.database,
                    args.user)]
            res.append("echo '1---Finish Create duplicate_db' &&")
            res.append(
                'psql -h db -p %s -U %s -d duplicate_db -f /tmp/%s &&' % (
                    args.port, args.user, args.clean_odoo_db))
            res.append("echo '2---Finish Clean duplicate_db' &&")
            res.append('pg_dump -h db -p %s -U %s -d duplicate_db' % (
                args.port, args.user))
        else:
            res.append('pg_dump -h db -p %s -U %s -d %s' % (
                args.port, args.user, args.database))
        if args.file:
            res.append('> /tmp/%s' % args.file)
        else:
            res.append('> /tmp/%s.out' % args.database)

        if args.clean_odoo_db:
            res.append("&& echo '3---Finish Dump duplicate_db' &&")
            res.append(
                "psql -h db -p %s -U %s -d %s "
                "-c 'Drop DATABASE duplicate_db'"% (
                    args.port,
                    args.user,
                    args.database))
        return res


def main():
    pgdump = PgDump()
    pgdump.run()

if __name__ == '__main__':
    main()
