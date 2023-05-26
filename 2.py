import logging
import random
import threading
import time
from threading import Lock

TOTAL_TICKETS = 100
TOTAL_PRINTED_TICKETS = 20

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Typographer(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_printed = 0

    def run(self):
        global TOTAL_TICKETS
        global TOTAL_PRINTED_TICKETS
        is_running = True
        while is_running:
            if TOTAL_TICKETS <= 0:
                is_running = False
            elif TOTAL_PRINTED_TICKETS < 4:
                with self.sem:
                    logger.info(f'typographer prints tickets')
                    self.random_sleep()
                    printed_tickets = random.randint(1, TOTAL_TICKETS)
                    TOTAL_PRINTED_TICKETS += printed_tickets
                    logger.info(f'{self.getName()} - printed ticket;  {TOTAL_PRINTED_TICKETS} number of printed tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        global TOTAL_PRINTED_TICKETS
        is_running = True
        while is_running:
            if TOTAL_PRINTED_TICKETS > 3:
                self.random_sleep()
                with self.sem:
                    if TOTAL_TICKETS <= 0:
                        break
                    self.tickets_sold += 1
                    TOTAL_PRINTED_TICKETS -= 1
                    TOTAL_TICKETS -= 1
                    logger.info(f'{self.getName()} sold one;  {TOTAL_TICKETS} left')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    semaphore = threading.Semaphore()
    sellers = []
    typographers = []

    for _ in range(3):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for _ in range(1):
        typographer = Typographer(semaphore)
        typographer.start()
        typographers.append(typographer)


if __name__ == '__main__':
    main()