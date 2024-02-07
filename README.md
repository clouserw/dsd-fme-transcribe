# dsd-fme-transcribe
Transcribe audio files from DSD FME.

## Install
```
pip install -r requirements.txt
```
If you want to see talk groups and you have a CSV already, you should edit the dsd-fme-transcribe.py file to add the path to the `self.talkgrouppath`.

## Run
```
python dsd-fme-transcribe.py /path/to/audio/files
```
Only new files will be processed.
