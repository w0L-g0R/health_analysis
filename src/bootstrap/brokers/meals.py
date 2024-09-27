import logging

from src.config.config import CONFIG_DICT, setup_logging
from src.containers.meals_container import MealsContainer

setup_logging()
logger = logging.getLogger(__name__)


meals_container = MealsContainer()
meals_container.config.from_dict(CONFIG_DICT)
meals_container.init_resources()
meals_broker = meals_container.broker()

# if __name__ == "__main__":
#     cmd = [
#         sys.executable,
#         "-m",
#         "taskiq",
#         "worker",
#         f"{get_module_path(__file__)}:meals_broker",
#     ]
#     process = None

#     try:
#         process = subprocess.Popen(cmd)
#         process.wait()

#     except KeyboardInterrupt:
#         logger.info("Keyboard interrupt received. Terminating the worker process.")
#         if process:
#             process.terminate()
#             process.wait()

#     except RuntimeError as re:
#         logger.error(f"A runtime error occurred: {re}")
#         if process:
#             process.terminate()
#             process.wait()
#         raise BrokerRuntimeError(f"Runtime error in broker: {re}")

#     except Exception as e:
#         logger.error(f"An unexpected error occurred: {e}")
#         if process:
#             process.terminate()
#             process.wait()
#         raise BrokerStartupError(f"Unexpected error in broker startup: {e}")

#     finally:
#         if process and process.poll() is None:
#             logger.info("Shutting down the worker process.")
#             process.terminate()
#             process.wait()
#             raise BrokerShutdownError("Error during broker shutdown.")
