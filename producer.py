# -*- coding: utf-8 -*-

__author__ = 'sputnik13'

from taskflow.jobs import backends as job_backends
from taskflow.persistence import backends as persistence_backends
from taskflow.persistence import logbook

from time import sleep
import sys

PERSISTENCE_BACKEND_CONF = {
    #"connection": "mysql+pymysql://taskflow:taskflow@localhost/taskflow",
    "connection": "zookeeper",
}

JOB_BACKEND_CONF = {
    "board": "zookeeper",
}


def main():
    count = 1
    with persistence_backends.backend(PERSISTENCE_BACKEND_CONF.copy()) \
            as persistence:

        with job_backends.backend('my-board', JOB_BACKEND_CONF.copy(),
                                  persistence=persistence) \
                as board:

            while True:
                print "test loop %d" % (count)
                job_name = "Job #%d" % (count)
                book = logbook.LogBook(job_name)
                details = {
                    'store': {
                        'vm_id': count,
                        'vm_name': "VM(%d)" % (count),
                    }
                }
                persistence.get_connection().save_logbook(book)
                job = board.post(job_name, book=book, details=details)
                print "%s posted" % (job)
                sleep(1)
                count += 1

if __name__ == "__main__":
    sys.exit(main())
