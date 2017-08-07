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
import argparse
from subprocess import check_output, call
import sys


class Client(object):
    def __init__(self, args=None):
        if args is None:
            args = sys.argv[1:]
        parser = self.parser()
        self.args = parser.parse_args(args)

    def get_image(self, container):
        try:
            return check_output(
                ["docker", "inspect", "--format",
                 "'{{ .Config.Image }}'", "%s" % container]
            ).strip().strip("'")
        except Exception:
            # Wrong container name error message will appear
            raise sys.exit(0)

    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-c', '--container', help="Container name",
            default="containers_postgres_1")
        parser.add_argument(
            '-p', '--port', help="Container internal port", default=5432)
        parser.add_argument('-U', '--user', help="Container user",
                            default='postgres')
        return parser

    def run(self):
        call(self.cmd(), shell=True)

    def cmd(self):
        args = self.args
        tag = self.get_image(args.container)
        docker_cmd = ' '.join(self.docker_cmd())
        container_cmd = ' '.join(self.container_cmd())
        return '''docker run -it --link %s:db %s \
                  --rm %s sh -c \"%s\"
               ''' % (args.container, docker_cmd, tag, container_cmd)

    def docker_cmd(self):
        return []

    def container_cmd(self):
        raise NotImplementedError
