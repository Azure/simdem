SIMDEM_VERSION = "2.0.0"

# Logging
import logging
LOG_FILE = "simdem.log"
LOG_LEVEL = logging.DEBUG

# When in demo mode we insert a small random delay between characters.
# TYPING DELAY is the upper bound of this delay.
TYPING_DELAY = 0.2

# Prompt to use in the console
CONSOLE_PROMPT = "$ "

# ------------------------------------------------------------------ #
# Danger zone
#
# Do not change anything after this notice,
# unless you know what you are doing
# ------------------------------------------------------------------ #

# Set is_debug to True if you want to run in debug mode. This setting
# can be overriden in the command like with the `--debug true` option.
is_debug = False