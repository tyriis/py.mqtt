import paho.mqtt.client as mqtt

from score.init import ConfiguredModule, ConfigurationError, parse_list, parse_bool, extract_conf
from time import time
import inspect
import logging
from functools import partial


log = logging.getLogger(__name__)

defaults = {
    'ctx.member': 'mqtt',
    'host': None,
    'port': 1883,
    'keepalive': 60
}


def init(confdict, ctx=None):
    """
    Initializes this module acoording to :ref:`our module initialization
    guidelines <module_initialization>` with the following configuration keys:
    """
    conf = defaults.copy()
    conf.update(confdict)
    if not conf['host']:
        raise ConfigurationError(score.mqtt, 'No host configured')
    client = mqtt.Client()
    mqtt_conf = ConfiguredMQTTModule(ctx, client, host=conf['host'], port=conf['port'], keepalive=conf['keepalive'])

    return mqtt_conf


class ConfiguredMQTTModule(ConfiguredModule):
    """
    This module's :class:`configuration class
    <score.init.ConfiguredModule>`.
    """

    def __init__(self, ctx, client, *, host=None, port=None, keepalive=None):
        self.ctx = ctx
        self.client = client
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topics = set()
        self.callbacks = dict()
        #self.topics.add('$SYS/broker/uptime')
        #client.connect("192.168.1.4", 1883, 60)
        #client.connect(host, port, keepalive)
        #client.loop_start()

    def on_connect(self, client, userdate, flags, rc):
        log.info('mqtt connected')
        for topic in self.topics:
            self.client.subscribe(topic)

    def subscribe(self, topic, callback=None):
        if callback and topic not in self.callbacks:
            self.callbacks[topic] = list()
        if callback:
            self.callbacks[topic].append(callback)
        self.topics.add(topic)
        if self.client._state != 1:
            return
        self.client.subscribe(topic)

    def on_message(self, client, userdate, msg):
        log.debug({'topic':msg.topic, 'payload': msg.payload, 'timestamp': msg.timestamp})
        self.userdate = userdate
        if msg.topic in self.callbacks:
            for callback in self.callbacks[msg.topic]:
                with self.ctx.Context() as ctx:
                    callback(ctx, msg)

    def get_serve_runners(self):
        if not hasattr(self, '_serve_runners'):

            class Runner:

                def __init__(runner, client, host, port, keepalive):
                    runner.client = client
                    runner.host = host
                    runner.port = port
                    runner.keepalive = keepalive

                def start(runner):
                    runner.client.connect(runner.host, runner.port, runner.keepalive)
                    return runner.client.loop_start()

                def stop(runner):
                    runner.client.disconnect()

            self._serve_runners = [Runner(self.client, self.host, self.port, self.keepalive)]

        return self._serve_runners
