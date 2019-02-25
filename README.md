# About
Tool for downloading and analyzing WheelLog data from your Google Drive account.
Searches for the WheelLog Logs folder, downloads files, and provides charts / summary information
about your rides.

WheelLog Android:  https://play.google.com/store/apps/details?id=com.cooper.wheellog
Android store listing references: https://github.com/JumpMaster/WheelLogAndroid
But the version available is actually the latest from: https://github.com/palachzzz/WheelLogAndroid

# Setup

Create a virtual environment under `.env/`:

```
$ python3 -mvenv .env/
$ .env/bin/pip install -r requirements.txt
```

Downlad the Google Drive credentials JSON file to `credentials.json`.

Once the credentials are set up (use https://developers.google.com/drive/api/v3/quickstart/python for instructions),
run the command, and it will walk you through the OAuth process to authorize access to your Google Drive folder.

# List Mode

## Auto-discovery of WheelLog Logs folder
From then, you can run the utility in list mode:

```bash
$ python3 wheellog_activity_analysis.py
Looking for WheelLog Logs folder
Files available in WheelLog Logs folder:
    2019_02_02_10_41_43.csv (id:1Y78DhPPWN0cBg193UX0cDCkRwslDcLVC)
    2019_02_08_13_06_35.csv (id:1AlSEvV9i1dx2_uplQ1hZ4Xr6IQaMFn0f)
    [...]
    2019_02_23_08_51_30.csv (id:1ToZI_UfscYS9oXMyUZFg4qci9Pmk1Z1s)
    2019_02_24_17_08_38.csv (id:1wkFthxdNAm-_sW2bbAQIJh4RNlQBuj0e)

Re-run command with desired filename as the first argument.
```

## Specify the logs folder ID manually

For a specific folder ID:

```bash
$ python3 wheellog_activity_analysis.py folder:FOLDERID
Looking for WheelLog Logs folder
Files available in WheelLog Logs folder:
    2019_02_02_10_41_43.csv (id:1Y78DhPPWN0cBg193UX0cDCkRwslDcLVC)
    2019_02_08_13_06_35.csv (id:1AlSEvV9i1dx2_uplQ1hZ4Xr6IQaMFn0f)
    [...]
    2019_02_23_08_51_30.csv (id:1ToZI_UfscYS9oXMyUZFg4qci9Pmk1Z1s)
    2019_02_24_17_08_38.csv (id:1wkFthxdNAm-_sW2bbAQIJh4RNlQBuj0e)

Re-run command with desired filename as the first argument.
```

# Download and analyze a file

## By Name

```bash
$ python3 wheellog_activity_analysis.py 2019_02_02_10_41_43.csv
```

## By File ID

```bash
$ python3 wheellog_activity_analysis.py id:1wkFthxdNAm-_sW2bbAQIJh4RNlQBuj0e
```

## Output

```
Downloading unknown file (id:1ToZI_UfscYS9oXMyUZFg4qci9Pmk1Z1s)
Log File from 2019-02-23 08:51:30.521000 to 2019-02-23 09:46:10.376000 ( 0 days 00:54:39.855000 )
Activity from 2019-02-23 08:51:30.786000 to 2019-02-23 09:46:05.079000 ( 0 days 00:54:34.293000 )

Data grouped in 30s intervals
Speeds (mph):
   18.91  ┼
   17.21  ┤ ╭╮╭╮╭╮  ╭──╮
   15.50  ┤ │╰╯╰╯╰──╯  │  ╭╮╭────╮ ╭╮                   ╭───╮╭╮    ╭─────╮                    ╭─────╮  ╭─╮ ╭─╮     ╭╮
   13.80  ┤ │          ╰──╯││    ╰─╯│           ╭╮╭╮ ╭─╮│   ╰╯╰╮   │     ╰╮╭─╮ ╭─╮  ╭╮  ╭─╮ ╭─╯     ╰──╯ ╰─╯ ╰────╮│╰─╮
   12.10  ┤ │              ╰╯       │ ╭─╮   ╭─╮╭╯╰╯╰╮│ ╰╯      │   │      ╰╯ ╰─╯ ╰╮╭╯╰─╮│ │╭╯                     ╰╯  ╰╮
   10.39  ┤ │                       │╭╯ ╰───╯ ││    ╰╯         │   │              ││   ╰╯ ││                           │
    8.69  ┤╭╯                       ╰╯        ││               │  ╭╯              ╰╯      ││                           │
    6.98  ┤│                                  ╰╯               │  │                       ╰╯                           │
    5.28  ┤│                                                   │  │                                                    │
    3.58  ┤│                                                   │  │                                                    │
    1.87  ┤│                                                   ╰─╮│                                                    │
    0.17  ┼╯                                                     ╰╯                                                    ╰


System Temp (F):
   77.00  ┤
   75.69  ┤                                                                        ╭─╮  ╭─╮
   74.38  ┤                                   ╭╮     ╭╮                       ╭╮ ╭─╯ │ ╭╯ │
   73.07  ┤                                  ╭╯│╭────╯│              ╭╮       │╰─╯   ╰─╯  ╰───╮ ╭╮
   71.76  ┤                                 ╭╯ ╰╯     ╰╮             ││     ╭─╯               ╰─╯│        ╭─╮
   70.45  ┤                                 │          │             ││     │                    │        │ │
   69.15  ┤                            ╭╮ ╭─╯          ╰─╮        ╭──╯╰───╮╭╯                    ╰─╮   ╭╮ │ ╰╮        ╭╮
   67.84  ┤ ╭──╮╭───╮                 ╭╯╰─╯              ╰────────╯       ╰╯                       ╰───╯╰─╯  ╰─╮╭─────╯╰
   66.53  ┤╭╯  ╰╯   ╰─╮  ╭╮         ╭─╯                                                                        ╰╯
   65.22  ┤│          ╰──╯╰─────────╯
   63.91  ┤│
   62.60  ┼╯


CPU Temp (F):
   93.20  ┤                                                                            ╭─────────╮╭╮ ╭─╮
   92.05  ┤                                      ╭─╮           ╭───────────────────────╯         ╰╯╰─╯ ╰───────────────╮
   90.91  ┤                                      │ │           │                                                       │
   89.76  ┤                  ╭╮         ╭────────╯ ╰───────────╯                                                       ╰
   88.62  ┤      ╭───╮╭──────╯╰─────────╯
   87.47  ┤      │   ││
   86.33  ┤   ╭──╯   ╰╯
   85.18  ┤╭──╯
   84.04  ┤│
   82.89  ┤│
   81.75  ┤╯
   80.60  ┼


Power
 1761.30  ┼
 1601.26  ┤                                                           ╭╮        ╭╮    ╭╮
 1441.22  ┤  ╭╮          ╭╮      ╭╮    ╭╮                 ╭╮ ╭╮       ││╭╮ ╭╮   │╰╮  ╭╯│   ╭╮ ╭╮
 1281.17  ┤╭╮││  ╭──╮    ││   ╭╮ ││    ││       ╭╮╭╮╭─╮   │╰╮││     ╭─╯│││ ││ ╭╮│ ╰╮ │ ╰──╮││ ││      ╭─╮ ╭╮     ╭╮╭╮
 1121.13  ┤│╰╯╰╮╭╯  ╰╮╭╮╭╯│ ╭─╯╰─╯╰─╮  ││   ╭─╮╭╯││││ │╭╮╭╯ ╰╯│     │  ╰╯│ │╰─╯││  │╭╯    ││╰╮│╰──╮   │ │ ││╭╮   │╰╯╰──╮
  961.09  ┤│   ╰╯    ╰╯╰╯ │╭╯       │╭╮│╰───╯ ││ ││││ ││╰╯    ╰╮    │    ╰─╯   ╰╯  ╰╯     ││ ╰╯   ╰───╯ ╰─╯╰╯╰╮╭╮│     │
  801.05  ┤│              ╰╯        ╰╯╰╯      ││ ╰╯││ ╰╯       │  ╭─╯                     ││                  ╰╯╰╯     │
  641.01  ┤│                                  ││   ╰╯          │  │                       ││                           │
  480.97  ┤│                                  ╰╯               │  │                       ╰╯                           │
  320.92  ┤│                                                   ╰╮ │                                                    │
  160.88  ┤│                                                    ╰╮│                                                    │
    0.84  ┼╯                                                     ╰╯                                                    ╰


Current
   23.31  ┼
   21.19  ┤                                                                     ╭╮    ╭╮
   19.07  ┤                                                  ╭╮       ╭╮╭╮ ╭╮ ╭╮│╰╮  ╭╯│   ╭╮ ╭╮       ╭╮ ╭╮     ╭╮
   16.96  ┤  ╭╮  ╭╮      ╭╮      ╭╮    ╭╮           ╭╮    ╭─╮││     ╭─╯│││ ││ │││ ╰╮ │ ╰──╮││ │╰╮╭╮   ╭╯│ ││╭╮   ││╭╮ ╭╮
   14.84  ┤╭╮││ ╭╯╰─╮ ╭╮ ││  ╭─╮╭╯╰╮   ││   ╭╮  ╭╮╭╮│╰╮  ╭╯ ╰╯│     │  ╰╯│ │╰─╯││  │╭╯    ││╰╮│ ╰╯╰─╮╭╯ │ │╰╯╰╮  │╰╯╰─╯│
   12.72  ┤│╰╯╰─╯   ╰─╯╰─╯│╭─╯ ╰╯  ╰╮╭╮││  ╭╯╰╮╭╯││││ │╭╮│    ╰╮    │    ╰─╯   ╰╯  ╰╯     ││ ╰╯     ╰╯  ╰─╯   │╭─╯     │
   10.60  ┤│              ╰╯        ╰╯╰╯╰──╯  ││ ╰╯││ ╰╯╰╯     │  ╭─╯                     ││                  ╰╯       │
    8.48  ┤│                                  ││   ╰╯          │  │                       ││                           │
    6.36  ┤│                                  ╰╯               │  │                       ╰╯                           │
    4.25  ┤│                                                   ╰╮ │                                                    │
    2.13  ┤│                                                    ╰╮│                                                    │
    0.01  ┼╯                                                     ╰╯                                                    ╰
```
