# ML Video Search Dashboard

This project builds a complete AWS + NLP + Gradio dashboard for Machine Learning course videos.
The system downloads videos from S3, transcribes them, normalizes text, extracts key phrases and topics,
builds a metadata CSV, and provides a fully searchable video dashboard.

---

## 🚀 Features

### 🔹 AWS S3 Integration
- Videos stored in S3  
- Transcriptions, normalized text, and key-phrase/topic metadata saved to S3  
- Signed URLs used for secure streaming  

### 🔹 NLP Pipeline
1. Extract audio from MP4  
2. Convert audio → text  
3. Normalize text  
4. Extract:
   - TF-IDF key phrases  
   - LDA topics  
5. Save metadata to JSON + CSV  

### 🔹 Dashboard
- Search by **topic** or **key phrase**  
- Embedded video player  
- Signed URL video access  
- Full HTML formatting in Gradio  

---

## 📁 Project Structure
```
ml-video-search-dashboard/
│
├── src/
│   ├── transcribe_videos.py
│   ├── normalize_transcriptions.py
│   ├── extract_key_phrases_topics.py
│   ├── build_csv.py
│   └── dashboard.py
│
├── data/        # optional local data folders
│
└── README.md
```

---

## 🔧 Installation

### 1. Install requirements
```bash
pip install -r requirements.txt
```
### 2.Configure AWS credentials
aws configure

## Run the Full Pipeline
Step 1 — Transcribe videos
```bash
python src/transcribe_videos.py
```
<img width="836" height="244" alt="image" src="https://github.com/user-attachments/assets/63b7e371-3f7d-4dbd-b07e-4eb659b46a1f" />


Step 2 — Normalize text
```bash
python src/normalize_transcriptions.py
```
Step 3 — Extract key phrases + topics
```bash
python src/extract_key_phrases_topics.py
```
Step 4 — Build CSV metadata
```bash
python src/build_csv.py
```
🌐 Run the Dashboard
```bash
python src/dashboard.py
```

This will open a shareable Gradio app link.

<img width="1281" height="402" alt="image" src="https://github.com/user-attachments/assets/d445e332-16f2-4517-a857-b652c3cc2b8c" />

<img width="1265" height="382" alt="image" src="https://github.com/user-attachments/assets/2a881be1-9a77-4b7b-b7f9-5a9d8b5190d4" />


