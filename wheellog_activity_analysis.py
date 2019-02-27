import pickle
import os.path
import io
import sys
import asciichartpy
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError as gclient_HttpError

import simpledate 

import pandas
import numpy

# build the service object - authorizing, if necessary
def build_service():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    if not os.path.exists('credentials.json'):
        print('Create and download the Google Drive API credentials JSON file to "credentials.json", or this command cannot run.')
        sys.exit(1)

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def find_wheellog_folder(service):
    results = service.files().list( q='name = "WheelLog Logs"' ).execute()
    results = results.get('files', [])
    if len(results) == 0:
        sys.stderr.print("No folder called 'WheelLog Logs' found. Unable to proceed.\n")
        sys.exit(1)
    if len(results) > 1:
        sys.stderr.print("Too many folders called 'WheelLog Logs' found. Unable to proceed.\n")
        sys.exit(1)

    return results[0]['id']

def find_log_files(service, folder_id, file_name=None):
    files = []

    page_token = None
    while True:
        query = "'%s' in parents and fileExtension = 'csv' and mimeType = 'text/plain' and trashed = false" % folder_id
        if file_name is not None:
            query = query + " and name = '%s'" % ( file_name )

        results = service.files().list( 
                            pageSize=100, 
                            fields="nextPageToken, files(id, name)", 
                            q = query,
                            pageToken=page_token
        ).execute()

        files = files + results.get('files', [])

        page_token = results.get('nextPageToken')
        if not page_token: break

    return files

def download_file( service, file_id ):
    request = service.files().get_media(fileId=file_id)
    with io.BytesIO() as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download %d%%." % int(status.progress() * 100))

        return fh.getvalue()

def dt_fmt_human( dt ):
    return simpledate.SimpleDate( dt, format= "%Y-%m-%dT%H:%M:%S %Z" )

def dt_fmt_machine( dt ):
    return simpledate.SimpleDate( dt, format= "%Y-%m-%dT%H:%M:%S.%f%z" )

def analyze_file( service, file_id, file_name, dt ):
    groupby_freq = '10s'
    seconds = (dt.index.max()-dt.index.min()).total_seconds() 
    if  seconds > 90*60:
        groupby_freq = '1 min'
    if  seconds > 30*60:
        groupby_freq = '30s'
    elif seconds > 30*60:
        groupby_freq = '10s'

    print("Data grouped in %s intervals" % groupby_freq)

    print("Speeds (mph):")
    speeds_mph = ( dt.speed/1.609 ).groupby(pandas.Grouper(freq=groupby_freq)).max().fillna(0)
    print( asciichartpy.plot( speeds_mph, {"height":10} ) )
    print("\n")

    print("System Temp (F):")
    system_temp = ( (dt.system_temp * 9/5) + 32 ).groupby(pandas.Grouper(freq=groupby_freq)).max().fillna(0)
    print( asciichartpy.plot( system_temp, {"height":10} ) )
    print("\n")

    print("CPU Temp (F):")
    cpu_temp = ( (dt.cpu_temp * 9/5) + 32 ).groupby(pandas.Grouper(freq=groupby_freq)).max().fillna(0)
    print( asciichartpy.plot( cpu_temp, {"height":10} ) )
    print("\n")

    print("Power")
    power = dt.power.groupby(pandas.Grouper(freq=groupby_freq)).max().fillna(0)
    print( asciichartpy.plot( power, {"height":10, "max": 2000} ) )
    print("\n")

    print("Current")
    current = dt.current.groupby(pandas.Grouper(freq=groupby_freq)).max().fillna(0)
    print( asciichartpy.plot( current, {"height":10} ) )
    print("\n")

    print("Tilt")
    tilt = dt.tilt.groupby(pandas.Grouper(freq=groupby_freq)).mean().fillna(0)
    print( asciichartpy.plot( tilt, {"height":10} ) )
    print("\n")

    print("Roll")
    roll = dt.roll.groupby(pandas.Grouper(freq=groupby_freq)).mean().fillna(0)
    print( asciichartpy.plot( roll, {"height":10} ) )
    print("\n")

def download_csv( service, file_id, file_name, dt ):
    with open (file_name, "w") as f:
        f.write( contents )

    print("Wrote CSV file to %s" % file_name)


def create_gpx( service, file_id, file_name, dt ):
    gpx_file = file_name.replace(".csv", ".gpx")
    with open (gpx_file, "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
            <gpx version="1.0" creator="wheellog-utils" xmlns="http://www.topografix.com/GPX/1/0">
              <time>%(start_time)s</time>
              <bounds minlat="%(min_lat)s" minlon="%(min_lon)s" maxlat="%(max_lat)s" maxlon="%(max_lon)s"/>
              <trk>
                <name>WheelLog - %(name)s</name>
                <type>18</type> <!-- Strava type for eBike ride -->
                <trkseg>
        """ % { 
            "name":       file_name.replace(".csv", ""),
            "start_time": dt_fmt_machine( dt.index[0].isoformat() ),
            "min_lat":    dt.latitude.min(),
            "min_lon":    dt.longitude.min(),
            "max_lat":    dt.latitude.max(),
            "max_lon":    dt.longitude.max()
        }  )

        falls = dt.query("not alert.isnull() and alert.str.contains('Fall')", engine="python")
        for index,point in falls.iterrows():
            f.write("""
              <wpt lat="%(latitude).6f" lon="%(longitude).6f">
                <ele>%(gps_alt).4f</ele>
                <time>%(time)s</time>
                <name>%(name)s</name>
              </wpt>""" % {
                "time":        dt_fmt_machine( index.isoformat() ),
                "latitude":    point.latitude,
                "longitude":   point.longitude,
                "gps_alt":     point.gps_alt,
                "name":        point.alert
            })


        for index,point in dt.iterrows():
            f.write("""
              <trkpt lat="%(latitude).6f" lon="%(longitude).6f">
                <ele>%(gps_alt).4f</ele>
                <time>%(time)s</time>
                <speed>%(wheel_speed).2f</speed>
              </trkpt>""" % {
                "time":        dt_fmt_machine( index.isoformat() ),
                "latitude":    point.latitude,
                "longitude":   point.longitude,
                "gps_alt":     point.gps_alt,
                "wheel_speed": point.speed/1.609,
            })
        
        f.write("""
                </trkseg>
          </trk>
        """)

        f.write("</gpx>")

    print("Wrote GPX file to %s" % gpx_file)

def main():
    service = build_service()
    
    command   = "analyze"
    folder_id = None
    file_id   = None
    file_name = None
    if len(sys.argv) > 1:
        sys.argv.pop(0) # remove the program name argument

        if len(sys.argv) and sys.argv[0] in ["analyze", "gpx", "csv"]:
            command = sys.argv.pop(0)
        if len(sys.argv) and sys.argv[0].startswith("folder:"):
            folder_id = sys.argv.pop(0).split(":")[1]
        if len(sys.argv) and sys.argv[0].startswith("id:"):
            file_id   = sys.argv.pop(0).split(":")[1]
        if len(sys.argv):
            file_name = sys.argv.pop(0)

    if folder_id is None and file_id is None:
        print("Looking for WheelLog Logs folder")
        folder_id = find_wheellog_folder(service)

    if file_id is None and file_name is None:
        files = find_log_files(service, folder_id)
        files = sorted(files, key=lambda x:x['name'])

        print("Files available in WheelLog Logs folder:")
        for file in files:
            print("    %s (id:%s)" % ( file['name'], file['id'] ))
        if len(files) == 0:
            print("    No files found.")
        print("")
        print("Re-run command with desired filename as the first argument.")
        sys.exit(0)
    elif file_id is None and file_name == 'latest':
        files = find_log_files(service, folder_id)
        files = sorted(files, key=lambda x:x['name'])
        
        if len(files) == 0:
            print("No WheelLog Logs files found.")
            sys.exit(1)
        
        file_id = files[-1]['id']
        file_name = files[-1]['name']
        print("Using most recent file in WheelLog Logs folder: %s (id:%s)" % ( file_name, file_id ))

    if file_name is not None and file_id is None:
        print("Searching for %s in WheelLog folder" % file_name)
        files = find_log_files(service, folder_id, file_name)
        if len(files) == 0:
            print("File [%s] not found in WheelLog folder." % file_name)
            sys.exit(1)
        if len(files) > 1:
            print("Multiple files named [%s] found in WheelLog folder - using first file (%s)." % ( file_name, files[0]['id'] ) )

        file_id   = files[0]['id']
        file_name = files[0]['name']
  
    if file_name is None and file_id is not None:
        file = service.files().get(fileId=file_id).execute()
        if not file:
            print("Unable to locate a file with the specified ID (%s)" % file_id)
            sys.exit(1)
        file_name = file['name']

    print("Downloading %s (id:%s)" % (file_name or "unknown file", file_id))
    try:
        contents = download_file( service, file_id )
    except gclient_HttpError as ex:
        print("Unable to open file [id:%s]: %s" % (file_id, ex._get_reason()))
        sys.exit(1)

    dt = None
    with io.BytesIO(contents) as f:
        dtypes = {
            "latitude":          numpy.float64,
            "longitude":         numpy.float64,
            "gps_speed":         numpy.float64,
            "gps_alt":           numpy.float64,
            "gps_heading":       numpy.float64,
            "gps_distance":      numpy.float64,
            "speed":             numpy.float64,
            "voltage":           numpy.float64,
            "current":           numpy.float64,
            "power":             numpy.float64,
            "battery_level":     numpy.float64,
            "distance":          numpy.float64,
            "totaldistance":     numpy.float64,
            "system_temp":       numpy.float64,
            "cpu_temp":          numpy.float64,
            "tilt":              numpy.float64,
            "roll":              numpy.float64,
            "mode":              str,
            "alert":             str,
        }
        dt = pandas.read_csv(f, sep=',', error_bad_lines=False, dtype=dtypes, encoding='utf-8', parse_dates={'datetime': ['date', 'time']}, index_col='datetime')

    print("")
    print("Log File from %s to %s ( %s )" % ( dt_fmt_human( dt.index.min() ), dt_fmt_human( dt.index.max() ), (dt.index.max()-dt.index.min())))

    # filter out the rows from the first Drive event to the last non-Shutdown event (which might be "Idle")
    dt = dt.loc[ dt.query('mode == "Drive"').head(1).index[0] : dt.query('mode != "Shutdown"').tail(1).index[0] ]
    print("Activity from %s to %s ( %s )" % ( dt_fmt_human( dt.index.min() ), dt_fmt_human( dt.index.max() ), (dt.index.max()-dt.index.min())))
    print("")

    if "analyze" == command:
        print("Analyzing specified log")
        analyze_file( service, file_id, file_name, dt )
        print("\n\n")
    elif "gpx" == command:
        print("Downloading and exporting GPX file for specified log")
        create_gpx( service, file_id, file_name, dt )
    elif "csv" == command:
        print("Downloading and exporting CSV file for specified log")
        create_csv( service, file_id, file_name, dt )
        

if __name__ == '__main__':
    main()
