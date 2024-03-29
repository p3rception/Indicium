<img src="https://i.imgur.com/LzEkelN.png" width=300>
<hr>

## Features
* Monitors the battery level of your macOS device.
* Sends notifications when the battery level falls below a low threshold (default: 20%) or rises above a high threshold (default: 80%).
* Provides customization options for adjusting threshold levels.

## Usage

To use this script, follow these steps:

1. Open a terminal.
2. Navigate to the directory where the script is located.
3. Run the script with the following command: `python battery_monitor.py -l <low_threshold> -ht <high_threshold>`, replacing `<low_threshold>` and `<high_threshold>` with your desired low and high battery thresholds.

## (Optional)

To run this script on startup, you can create an `indicium.sh` file with the following content and add it to the Login Items:

```bash
#!/bin/bash

python3 /path/to/Indicium/indicium.py
```

## Author

Dimitris Pergelidis ([p3rception](https://github.com/p3rception))

## License

This project is licensed under the MIT License - see the LICENSE file for details.
