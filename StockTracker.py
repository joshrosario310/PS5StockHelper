# Stock tracker base class
# Author: Tyler Gamvrelis

# Standard library imports
import logging
from threading import Event, Semaphore, Thread


# Globals
logger = logging.getLogger(__name__)


class StockTracker(Thread):
    """Functionalities and logic implemented by all stock trackers."""

    def __init__(self, group=None, target=None, name=None):
        super(StockTracker, self).__init__(group=group, target=target, name=name)
        self._name = name
        self._stock_check_sem = Semaphore(0)
        self._stop_event = Event()
        self._callback = self._default_callback
        self._is_test_mode = False

    def stop(self):
        """
        Prevents any more stock checks from executing, and causes the thread to
        exit when the current request (if any) is done executing.
        """
        self._stop_event.set()
        self.request_stock_check() # So that thread isn't blocked
        logger.debug('Stop requested for {0}'.format(self._name))

    def enable_test_mode(self):
        """
        Test mode allows us to see the behaviour of this object during a
        simulated drop.
        """
        self._is_test_mode = True

    def disable_test_mode(self):
        """
        Test mode allows us to see the behaviour of this object during a
        simulated drop.
        """
        self._is_test_mode = False

    def _has_stopped(self):
        """Check whether this thread has been stopped."""
        return self._stop_event.is_set()

    def request_stock_check(self):
        """Makes stock checker perform a request."""
        self._stock_check_sem.release()

    def set_callback(self, callback):
        """Attaches a function to be called after a stock check is preformed."""
        self._callback = callback

    def _default_callback(self):
        """Default callback function for processing stock check results."""
        logger.warning('Callback unimplemented for {0}'.format(self._name))

    def _do_stock_check(self):
        """
        Performs the stock check.

        Returns:
            None if no new stock, else a populted DropResult.
        """
        if type(self) is StockTracker:
            raise Exception('StockTracker is an abstract class and cannot be instantiated directly')

    def run(self):
        while True:
            self._stock_check_sem.acquire()
            if self._has_stopped():
                break
            result = self._do_stock_check()
            self._callback(result)
        logger.debug('Exiting thread {0}'.format(self._name))


class DropResult:
    """Container to organize drop results."""
    def __init__(self, date, links, info):
        self.date = date
        self.links = links # List of links
        self.info = info

    def __str__(self):
        st = 'Drop info:\n'
        st += '\tDate: ' + str(self.date) + '\n'
        st += '\tInfo: ' + self.info + '\n'
        st += '\tLinks:\n'
        for link in self.links:
            st += '\t\t' + link + '\n'
        return st
