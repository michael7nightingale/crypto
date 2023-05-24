from crypto import Crypto
import sys
from logger import log_twice


if __name__ == '__main__':
    """Running the program."""
    settings = {                # default settings
        "time_trigger": 1,
        "percents_trigger": 1,
        "request_data_limit": 4
    }
    commands = {"-p": "percents_trigger", '-t': "time_trigger", '-r': "request_data_limit"}
    args = sys.argv[1:]
    if not args:    # then use default settings
        pass
    elif not all(arg in commands for arg in args[::2]) or len(args) % 2 == 1:   # incorrect amount or order
        log_twice("error", "Commands are written in format: [-command1 arg1 -command2 arg2 -command3 arg3]")
        sys.exit()
    else:   # order and amount are correct
        try:
            settings_got = dict(
                zip(args[::2], args[1::2])
            )
            settings.update(**{commands[com_]: float(arg_) for com_, arg_ in settings_got.items()})
        except Exception as e:  # exceptions if data itself is invalid
            log_twice("error", str(e))
            sys.exit()

    # crypto class definition and running
    cryptoWorker = Crypto(**settings)
    cryptoWorker.run()

