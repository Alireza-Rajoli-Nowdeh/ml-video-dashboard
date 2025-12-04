import boto3
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import tempfile
import os
import json

# S3 configuration
s3 = boto3.client("s3")
SOURCE_BUCKET = "aws-tc-largeobjects"
DEST_BUCKET = "YOUR_S3_BUCKET_NAME"

INPUT_PREFIX = "CUR-TF-200-ACMNLP-1/video/"
AUDIO_PREFIX = "output/audio/"
TRANS_PREFIX = "output/transcriptions/"

def list_s3_files(bucket, prefix):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"].split("/")[-1] for obj in response.get("Contents", [])]

videos = list_s3_files(SOURCE_BUCKET, INPUT_PREFIX)
existing_transcriptions = set(
    name.lower() for name in list_s3_files(DEST_BUCKET, TRANS_PREFIX)
)

to_process = [
    v for v in videos if v.lower() + ".json" not in existing_transcriptions
]

print("Videos to process:", to_process)

recognizer = sr.Recognizer()

for video_name in to_process:
    print(f"Processing video: {video_name}")

    # Download video
    video_key = f"{INPUT_PREFIX}{video_name}"
    obj = s3.get_object(Bucket=SOURCE_BUCKET, Key=video_key)
    video_bytes = obj["Body"].read()

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(video_bytes)
        video_path = temp.name

    # Extract audio
    video = mp.VideoFileClip(video_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = f"{tmpdir}/{video_name}.wav"
        video.audio.write_audiofile(audio_path)

        # Upload audio
        s3.upload_file(audio_path, DEST_BUCKET, f"{AUDIO_PREFIX}{video_name}.wav")

        # Chunk audio
        audio = AudioSegment.from_file(audio_path)
        chunks = make_chunks(audio, 30000)

        transcription = ""
        for i, chunk in enumerate(chunks):
            chunk_path = f"{tmpdir}/chunk{i}.wav"
            chunk.export(chunk_path, format="wav")

            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)
                transcription += text + " "
            except:
                pass

        # Save transcription
        trans_key = f"{TRANS_PREFIX}{video_name}.json"
        data = {"transcription": transcription}

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=trans_key,
            Body=json.dumps(data)
        )

    os.remove(video_path)

print("All transcriptions complete.")# placeholder
