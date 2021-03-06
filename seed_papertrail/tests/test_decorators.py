from unittest import TestCase
from seed_papertrail.decorators import papertrail
from testfixtures import log_capture


class DecoratorTestCase(TestCase):

    @log_capture()
    def test_default_papertrail(self, l):

        @papertrail('foo', level='INFO')
        def testing():
            return 1

        self.assertEqual(testing(), 1)
        first_line, second_line = str(l).strip().split('\n')
        self.assertTrue(first_line.startswith('papertrail INFO'))
        self.assertTrue(
            '%s.%s' % (testing.__module__, testing.__name__) in second_line)
        print str(l)
        self.assertTrue(
            second_line.endswith('foo, threshold:OK, sampling:1.0'))

    @log_capture()
    def test_papertrail_error(self, l):

        @papertrail.error('eep')
        def testing():
            return 1

        self.assertEqual(testing(), 1)
        self.assertTrue(str(l).startswith('papertrail ERROR'))
        self.assertTrue('eep' in str(l))
        self.assertTrue(
            '%s.%s' % (testing.__module__, testing.__name__) in str(l))

    @log_capture()
    def test_papertrail_error_naked(self, l):

        @papertrail.error
        def testing():
            return 1

        self.assertEqual(testing(), 1)
        self.assertTrue(str(l).startswith('papertrail ERROR'))
        self.assertTrue(
            '%s.%s' % (testing.__module__, testing.__name__) in str(l))

    @log_capture()
    def test_papertrail_timer(self, l):

        with papertrail.timer('foo', level='ERROR'):
            True

        self.assertTrue(str(l).startswith('papertrail ERROR'))
        self.assertTrue('foo' in str(l))

    @log_capture()
    def test_papertrail_timer_with_logger(self, l):

        with papertrail.timer('foo', level='ERROR') as trail:
            trail.debug('ello!')

        self.assertTrue(str(l).startswith('papertrail DEBUG'))
        self.assertTrue('papertrail ERROR' in str(l))
        self.assertTrue('foo' in str(l))
        self.assertTrue('ello!' in str(l))
