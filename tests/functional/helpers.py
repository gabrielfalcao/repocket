# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from repocket import configure
from sure import scenario


def prepare_redis(context):
    context.pool = configure.connection_pool(
        hostname='localhost',
        port=6379
    )
    context.connection = context.pool.get_connection()
    sweep_redis(context)

def sweep_redis(context):
    context.connection.flushall()


clean_slate = scenario([prepare_redis], [sweep_redis])
