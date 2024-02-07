import csv
import sys
import time
import whisper
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):

    def __init__(self):

        # Full file path, e.g. /home/user/blah.csv
        # CSV format is https://github.com/lwvmobile/dsd-fme/blob/audio_work/examples/group.csv
        self.talkgrouppath = ''

        self.model = whisper.load_model("base")

        self.talkgroups = {}

        if self.talkgrouppath:
            with open(self.talkgrouppath) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.talkgroups[row['Decimal']] = row['Name']

    def on_closed(self, event):

        if event.is_directory:
            return None

        filename = event.src_path.split(' ')

        audio = whisper.load_audio(event.src_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        options = whisper.DecodingOptions(language='en', fp16=False)
        res = whisper.decode(self.model, mel, options=options)

        if filename[8] in self.talkgroups:
            src = self.talkgroups[filename[8]]
        else:
            src = filename[8]

        print(f"TG {src} RID {filename[11][:-4]}: {res.text}", flush=True)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f'start watching directory {path!r}')
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
