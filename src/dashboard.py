import gradio as gr
import boto3
import pandas as pd
import os

BUCKET = "alireza-rajoli-nowdeh-project"
CSV_KEY = "output/key_phrases_and_topics.csv"

s3 = boto3.client("s3")

local_csv = "key_phrases_and_topics.csv"
s3.download_file(BUCKET, CSV_KEY, local_csv)

df = pd.read_csv(local_csv)

def get_signed_url(video):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": video},
        ExpiresIn=3600
    )

def search(query):
    query = query.lower()
    results = df[
        df["Key Phrases"].str.contains(query, case=False, na=False) |
        df["Topics"].str.contains(query, case=False, na=False)
    ]

    if results.empty:
        return "<h3>No matching videos found.</h3>"

    html = "<h2>Search Results</h2>"
    for _, row in results.iterrows():
        video = row["Video Name"] + ".mp4"
        url = get_signed_url(video)

        html += f"""
        <div style='border:1px solid #ccc; padding:15px; margin-bottom:20px;'>
        <h3>{row['Video Name']}</h3>
        <p><b>Key Phrases:</b> {row['Key Phrases']}</p>
        <p><b>Topics:</b> {row['Topics']}</p>
        <video width="320" height="240" controls>
            <source src="{url}" type="video/mp4">
        </video>
        </div>
        """

    return html

iface = gr.Interface(
    fn=search,
    inputs=gr.Textbox(label="Search key phrase or topic"),
    outputs="html",
    title="ML Video Search Dashboard",
    description="Search ML course videos by topics or key phrases."
)

iface.launch(share=True)
