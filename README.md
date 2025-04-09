# 🎵 Real-Time Music Streaming Analytics Pipeline

This project demonstrates a real-time data processing pipeline that ingests, enriches, and streams music playback events — just like how Spotify might track "Song of the Year" or "Artist of the Year".

Built with **Databricks**, **Apache Spark Structured Streaming**, and **Snowflake**.

---

## 🚀 Pipeline Overview

```
[JSON Playback Events]
        ⬇
  Databricks Auto Loader
        ⬇
Enrichment with Songs & Users Metadata (CSV)
        ⬇
 Streaming Join + Transformation
        ⬇
   Write to Snowflake Table
```

---

## 📂 Project Structure

```
.
├── notebooks/
│   └── music_streaming_pipeline.py
├── data/
│   ├── events/              # JSON streaming files
│   ├── songs.csv            # Static metadata
│   └── users.csv            # Static metadata
├── README.md
└── requirements.txt
```

---

## 📦 Technologies Used

- Apache Spark (Structured Streaming)  
- Databricks Auto Loader  
- Delta Lake  
- Snowflake  
- PySpark  
- DBFS (Databricks File System)

---

## 📥 Data Sources

- `songs.csv` – contains metadata about songs (title, artist, genre, etc.)
- `users.csv` – contains user info (country, subscription, device, etc.)
- `/tmp/music/events/` – directory where JSON playback events are streamed (e.g. song plays)

Sample JSON event:
```json
{
  "user_id": "U001",
  "song_id": "S001",
  "timestamp": "2025-04-09T10:00:00",
  "device": "mobile"
}
```

---

## 🧪 How It Works

1. Autoloader listens to `/tmp/music/events/` for incoming JSON event files  
2. Static reference data (`songs.csv`, `users.csv`) are loaded as DataFrames  
3. Streaming data is joined with reference data to enrich with metadata  
4. The final enriched stream is written into a Snowflake table: `MUSIC_EVENTS`

---

## 🧰 Setup Instructions

### 1. Upload Static Files to DBFS

```python
dbutils.fs.cp("file:/local/path/songs.csv", "dbfs:/tmp/music/songs.csv")
dbutils.fs.cp("file:/local/path/users.csv", "dbfs:/tmp/music/users.csv")
```

### 2. Stream Sample JSON Files

Drop JSON files into `/tmp/music/events/` directory in DBFS (or automate it).

### 3. Create Snowflake Table

```sql
CREATE TABLE MUSIC_EVENTS (
  song_id STRING,
  user_id STRING,
  device STRING,
  timestamp STRING,
  _rescued_data STRING,
  country STRING,
  subscription STRING,
  title STRING,
  artist STRING,
  genre STRING,
  duration INT,
  event_time TIMESTAMP
);
```

### 4. Configure Snowflake Connection in Notebook

```python
sfOptions = {
  "sfURL": "your_account.snowflakecomputing.com",
  "sfDatabase": "YOUR_DB",
  "sfSchema": "YOUR_SCHEMA",
  "sfWarehouse": "YOUR_WAREHOUSE",
  "sfRole": "YOUR_ROLE",
  "sfUser": "YOUR_USERNAME",
  "sfPassword": "YOUR_PASSWORD",
  "dbtable": "MUSIC_EVENTS"
}
```

### 5. Start the Streaming Job

```python
df_joined.writeStream     .foreachBatch(write_to_snowflake)     .option("checkpointLocation", "/tmp/music/checkpoints/snowflake")     .start()
```

---

## 📊 Future Enhancements

- Daily aggregation jobs: Artist of the Year, Song of the Year  
- Dashboarding via Databricks SQL or Tableau  
- Kafka or Kinesis as input source  
- Data quality validation with Great Expectations

---

## 🧑‍💻 Author

**Your Name**  
[GitHub](https://github.com/yourusername)  
[LinkedIn](https://linkedin.com/in/yourprofile)

---

## 📄 License

This project is licensed under the MIT License.
