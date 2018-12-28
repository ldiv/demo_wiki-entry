import logging


wiki_logger = logging.getLogger('wiki_logger')
file_handler = logging.FileHandler('application.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
wiki_logger.addHandler(file_handler)
wiki_logger.setLevel(logging.INFO)


def log_crud(operation, result, entry):
    wiki_logger.info("ENTRY {} {} for {}".format(operation, result["status"], entry))
