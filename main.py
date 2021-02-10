from threading import Thread
from jobs import truecar_job
from helpers import db_helper
from utils.logger import logger

BRANDS = ['Dodge', 'Nissan', 'Lamborghini', 'Ferrari'] 


logger.log_info("Initialize database")
db_helper.create_table()

threads = []
for brand in BRANDS:
    logger.log_info("Launch jobs for brand: {}".format(brand))
    #threads.append(Thread(target=truecar_job, args=(brand, True)))
    #threads.append(Thread(target=truecar_job, args=(brand, False)))
    #threads.append(Thread(target=truecar_job, args=(brand, False)))
    threads.append(Thread(target=autotrader_job, args=(brand, False)))
for thread in threads:
    thread.start()

logger.log_info("Wait for all jobs to finish")
for thread in threads:
    thread.join()
