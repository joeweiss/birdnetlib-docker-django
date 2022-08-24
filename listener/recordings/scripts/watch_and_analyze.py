# This example requires arecord, which is available on most Linux systems.
# Record to 15 second files with arecord, then analyze with two analyzers.

from datetime import datetime
from pprint import pprint
import os

from django.conf import settings

from birdnetlib.watcher import DirectoryWatcher
from birdnetlib.analyzer_lite import LiteAnalyzer
from birdnetlib.analyzer import Analyzer
from recordings.utils import import_from_recording

RECORDING_DIR = settings.INGEST_WAV_FILE_DIRECTORY
DELETE_IF_NO_DETECTIONS = True
PROCESS_EXISTING_BEFORE_WATCHING = True


def on_analyze_complete(recording):
    print("on_analyze_complete")
    # Each analyzation as it is completed.
    print(recording.path, recording.analyzer.name)
    pprint(recording.detections)


def on_analyze_file_complete(recording_list):
    print("---------------------------")
    print("on_analyze_file_complete")
    print("---------------------------")
    # All analyzations are completed. Results passed as a list of Recording objects.
    num_detections = 0
    for recording in recording_list:
        rec_obj = import_from_recording(recording)
        print(rec_obj, recording.filename, recording.date, recording.analyzer.name)
        pprint(recording.detections)
        num_detections = num_detections + len(recording.detections)
        print("---------------------------")
    if num_detections == 0 and DELETE_IF_NO_DETECTIONS:
        print("Deleting", recording.path)
        os.remove(recording.path)


def on_error(recording, error):
    print("An exception occurred: {}".format(error))
    print(recording.path)


def preanalyze(recording):
    # Used to modify the recording object before analyzing.
    filename = recording.filename
    # 2022-08-15-birdnet-21:05:51.wav, as an example, use BirdNET-Pi's preferred format for testing.
    dt = datetime.strptime(filename, "%Y-%m-%d-%H:%M:%S.wav")
    # Modify the recording object here as needed.
    # For testing, we're changing the date. We could also modify lat/long here.
    recording.date = dt


def main():

    recording_dir = RECORDING_DIR

    print("Starting Analyzers")

    directory = recording_dir

    analyzer_lite = LiteAnalyzer()
    analyzer = Analyzer()
    analyzers = [analyzer, analyzer_lite]

    lon = -77.3664
    lat = 35.6127
    min_conf = 0.70

    if PROCESS_EXISTING_BEFORE_WATCHING:
        directory_analyzer = DirectoryAnalyzer(
            directory,
            analyzers=analyzers,
            lon=-77.3664,
            lat=35.6127,
            min_conf=0.70,
        )
        directory_analyzer.recording_preanalyze = preanalyze
        directory_analyzer.on_analyze_complete = on_analyze_complete
        directory_analyzer.on_analyze_file_complete = on_analyze_file_complete
        directory_analyzer.on_error = on_error
        directory_analyzer.run()

    print("Starting Watcher")

    watcher = DirectoryWatcher(
        directory,
        analyzers=analyzers,
        lon=-77.3664,
        lat=35.6127,
        min_conf=0.70,
    )
    watcher.recording_preanalyze = preanalyze
    watcher.on_analyze_complete = on_analyze_complete
    watcher.on_analyze_file_complete = on_analyze_file_complete
    watcher.on_error = on_error
    watcher.watch()


def run():
    print("watch_and_analyze")
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print("Exception")
        print(e)