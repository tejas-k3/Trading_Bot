"""
This is the core file executing project files.
"""
import INFO
import CONSTANT
from time import perf_counter
import multiprocessing
import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logging.config.fileConfig(fname='logger.conf')
LOGGER = logging.getLogger('root')

segments = INFO.marketSegments
if __name__ == '__main__':
    # Start time in seconds
    startTime = perf_counter()
    LOGGER.info("Started main process at {} with process limit {}".format(startTime, CONSTANT.processLimit))
    # Total companies to do analysis on
    companies = []
    # Set to handle duplications
    endTime = perf_counter()
    LOGGER.info("Total time taken for core process to run : {} minutes".format((endTime-startTime)/60))