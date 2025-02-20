import logging

def setup_logger():
    logging.basicConfig(filename='product_matching.log', level=logging.INFO)
    return logging.getLogger(__name__)