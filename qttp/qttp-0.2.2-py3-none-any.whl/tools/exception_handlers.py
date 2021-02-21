from qttp.tools.log import setup_custom_logger

logger = setup_custom_logger("Exception Handlers")

def exception_handler_01(func):
    def inner_function(*args, **kwargs):
        try:
            return_value = func(*args, **kwargs)
            if args[0].log:
                done_message = (
                    f"{args[0].api} - {args[0].market} - "
                    f"{func.__name__.upper():<13s} -  "
                    f"{return_value}"
                )
                logger.info(done_message)
            return return_value
        except (ccxt.NetworkError, ccxt.InsufficientFunds) as e:
            error_message = (
                        f"{args[0].api}, {args[0].market}, "
                        f"{func.__name__.upper()}, {type(e).__name__}"
                    )
            logger.info(error_message)
    return inner_function
