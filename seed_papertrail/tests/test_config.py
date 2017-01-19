from unittest import TestCase
from seed_papertrail.config import handler, formatter


class ConfigTestCase(TestCase):

    def test_handler(self):
        handler_config = handler(
            'foo', 123, level='DEBUG',
            handler_class='foo.Handler',
            formatter='formatter')
        self.assertEqual(handler_config, {
            'level': 'DEBUG',
            'class': 'foo.Handler',
            'formatter': 'formatter',
            'address': ('foo', 123),
        })

    def test_formatter(self):
        formatter_config = formatter('sender_name', 'program_name')
        self.assertEqual(
            set(formatter_config.keys()),
            set(['format', 'datefmt']))
        self.assertEqual(
            formatter_config['format'] % {'asctime': 'foo', 'message': 'bar'},
            'foo sender_name program_name: bar')
