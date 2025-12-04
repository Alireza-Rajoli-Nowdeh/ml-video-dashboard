# placeholder
import boto3
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

s3 = boto3.client("s3")
BUCKET = "YOUR_S3_BUCKET_NAME"

NORM_PREFIX = "output/normalized_transcriptions/"
KP_PREFIX = "output/key_phrases_and_topics/"

def list_files(prefix):
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]

files = list_files(NORM_PREFIX)

texts = {}
for key in files:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    data = json.loads(obj["Body"].read().decode("utf-8"))
    texts[os.path.basename(key)] = data["normalized_transcription"]

vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
tfidf = vectorizer.fit_transform(texts.values())
features = vectorizer.get_feature_names_out()

lda = LatentDirichletAllocation(n_components=3, random_state=42)
lda_matrix = lda.fit_transform(tfidf)

for i, (filename, text) in enumerate(texts.items()):
    row = tfidf[i].toarray()[0]

    top_kp = [features[idx] for idx in row.argsort()[-5:][::-1]]

    topics = []
    for topic in lda.components_:
        top_words = topic.argsort()[-5:][::-1]
        topics.append([features[i] for i in top_words])

    data = {
        "Key Phrases": top_kp,
        "Topics": topics[0]
    }

    save_key = f"{KP_PREFIX}{filename.replace('.json','')}.json"
    s3.put_object(Bucket=BUCKET, Key=save_key, Body=json.dumps(data))

    print("Saved:", save_key)

print("Key phrases and topics extracted.")
