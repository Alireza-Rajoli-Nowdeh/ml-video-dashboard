import boto3
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import contractions

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

s3 = boto3.client("s3")
BUCKET = "alireza-rajoli-nowdeh-project"

TRANS_PREFIX = "output/transcriptions/"
NORM_PREFIX = "output/normalized_transcriptions/"

def list_files(prefix):
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]

def normalize(text):
    text = text.lower()
    text = contractions.fix(text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords.words("english")]

    lem = WordNetLemmatizer()
    tokens = [lem.lemmatize(t) for t in tokens]

    return " ".join(tokens)

files = list_files(TRANS_PREFIX)

for key in files:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    raw = json.loads(obj["Body"].read().decode("utf-8"))

    cleaned = normalize(raw["transcription"])

    norm_key = key.replace("transcriptions", "normalized_transcriptions")

    s3.put_object(
        Bucket=BUCKET,
        Key=norm_key,
        Body=json.dumps({"normalized_transcription": cleaned})
    )

    print("Normalized:", key)

print("All text normalized.")
# placeholder
