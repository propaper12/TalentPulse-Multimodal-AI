# TalentPulse ⚡
### Multimodal AI Proctoring & Real-Time Big Data Analytics Lakehouse

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![.NET](https://img.shields.io/badge/.NET-8.0%20(C%23)-512BD4.svg?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com)
[![DuckDB](https://img.shields.io/badge/DuckDB-Columnar%20OLAP-FFF000.svg?logo=duckdb&logoColor=black)](https://duckdb.org)
[![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-Edge%20AI-FF6F00.svg?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/js)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Acoustic%20DSP-007808.svg?logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Industry Problem & Vision:** In modern high-volume automated recruitment platforms (e.g., **HumanOre**), concurrent video and audio interviews overwhelm central servers with massive video ingestion and GPU inference bottlenecks. **TalentPulse** decouples and solves this through **Client-Side Edge AI** (BlazeFace 3D & COCO-SSD), **Acoustic Digital Signal Processing (DSP)**, **In-Memory Event Streaming**, and a **DuckDB Columnar Lakehouse** queried in sub-20ms latency and consumed via **C# .NET 8 LINQ**.

---

## 🏗️ System Architecture

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                    CLIENT-SIDE EDGE AI (Browser WebGL)                 │
 │  WebCam Stream ──► BlazeFace 3D (Yaw/Pitch Gaze) ──► Reticle & Gaze    │
 │                ──► COCO-SSD (Phone Detection)     ──► Auto-Freeze Modal│
 │  Audio Stream  ──► Web Audio API (16kHz FFT DSP)  ──► Real-Time SNR    │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ WebM Video + Telemetry Stream
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      FASTAPI STREAM INGESTION ENGINE                   │
 │                Decoupled In-Memory Topic Stream (Pub/Sub)              │
 └─────────────────┬────────────────────────────────────┬─────────────────┘
                   │ Video/Audio Stream                 │ Metadata & Telemetry
                   ▼                                    ▼
 ┌───────────────────────────────────┐    ┌───────────────────────────────┐
 │       FFMPEG DSP DEMUXER          │    │     DUCKDB COLUMNAR OLAP      │
 │  • Demux WebM -> 16kHz Mono WAV   │    │  • Sub-20ms Analytical Queries│
 │  • Acoustic SNR & Volumedetect    │───►│  • Multi-topic Breach Logs    │
 │  • Speech WPM & Silence Ratio     │    │  • 100+ Session Aggregations  │
 └───────────────────────────────────┘    └───────────────┬───────────────┘
                                                          │
                   ┌──────────────────────────────────────┴───────────────┐
                   ▼                                                      ▼
 ┌───────────────────────────────────┐                  ┌───────────────────────────────────┐
 │      ENTERPRISE C# .NET 8         │                  │      AUTONOMOUS REACT HR AGENT    │
 │  • Strongly Typed DTO Client      │                  │  • Observation & Reasoning Loop   │
 │  • LINQ Integrity Breach Filters  │                  │  • Unscripted Live Probe Questions│
 │  • Real-Time Recruitment Radar    │                  │  • Dynamic Interview Copilot      │
 └───────────────────────────────────┘                  └───────────────────────────────────┘
```

---

## 🚀 Key Engineering Pillars

### 1. 👁️ Client-Side Edge AI (BlazeFace 3D & COCO-SSD)
* **Zero-GPU Server Cost:** Face tracking and object detection execute directly inside the candidate's browser via WebGL/WebAssembly at ~5 FPS (200ms loop).
* **Realistic Screen Gaze Tolerance:** Rather than forcing unnatural, rigid webcam stare, BlazeFace extracts 6 facial 3D landmarks. Horizontal yaw ratio ($0.28 \le \text{ratio} \le 0.72$) grants full natural screen viewing freedom.
* **Instant Breach Flagging:**
  * **Head Turn (Yaw):** Detects looking away at secondary monitors or off-screen notes (`⚠️ SAĞA/SOLA BAKIŞ`).
  * **Head Tilt (Pitch):** Detects looking down at desk notes or lap (`⚠️ AŞAĞI BAKIŞ`).
  * **Phone Detection:** Real-time **COCO-SSD** flags unauthorized cell phones (`🚨 TELEFON: %98`), freezes the interview timer, sounds an alert, and launches an AI integrity verification modal.

### 2. 🎙️ Acoustic Signal Processing (FFmpeg DSP & STT)
* **Demuxing Pipeline:** FFmpeg splits incoming WebM media containers into pure 16kHz mono `.wav` audio channels and `.jpg` thumbnail keyframes.
* **Acoustic Signal Metrics:**
  * **Signal-to-Noise Ratio (SNR dB):** Filters ambient room noise from spoken voice.
  * **Speech Tempo (WPM):** Calculates words per minute to evaluate confidence and fluency.
  * **Silence Ratio (%):** Detects excessive pausing and hesitation.
* **Dynamic Keyword Interception:** Real-time 16kHz speech recognition detects key technical concepts (C#, OOP, LINQ, SQL) and triggers context-aware follow-up questions on the fly.

### 3. ⚡ DuckDB Columnar OLAP Analytics Lakehouse
* **High-Throughput Analytics:** Replaces slow transactional RDBMS with **DuckDB In-Memory Columnar OLAP**.
* **Vectorized Execution:** Processes multi-dimensional queries across 100+ candidate sessions with sub-20ms query latency.
* **Two-Tier Storage:**
  * Raw unstructured media files stored in `media_storage/` (`.webm`, `.wav`, `.jpg`).
  * Structured acoustic, proctoring, and evaluation signals stored in `talent_pulse_analytics.duckdb`.

### 4. 💻 Enterprise C# .NET 8 Integration (LINQ)
* Native integration client for corporate recruitment systems (e.g., **HumanOre**).
* Uses asynchronous HTTP clients and strongly typed DTOs.
* Employs **C# LINQ (`Where` + `OrderByDescending`)** to filter candidates by multimodal composite scores and instantly isolate integrity breaches in red/amber alerts.

### 5. 🤖 Autonomous ReAct HR Agent
* Gathers multi-modal metrics (technical score, audio clarity, gaze %, breach counts).
* Runs an autonomous **Observation -> Reasoning -> Action** loop.
* Synthesizes tailored, unscripted interview questions for technical leads (e.g., Tech Lead İsa Kedikoğlu) based on candidate weaknesses.

---

## 📊 Benchmarks & Performance

| Metric | Target | TalentPulse Result | Technology |
|---|---|---|---|
| **Client-Side Face Inference** | < 50ms | **15 - 20 ms** | TensorFlow.js BlazeFace (WebGL) |
| **Edge Phone Object Detection** | < 100ms | **35 - 45 ms** | TensorFlow.js COCO-SSD |
| **Audio Demux & DSP Extraction** | < 500ms | **210 ms** | FFmpeg Native Subprocess |
| **DuckDB OLAP Aggregation (100+ Sessions)** | < 50ms | **14.6 ms** | DuckDB Columnar Engine |
| **C# .NET 8 LINQ Processing** | < 100ms | **28 ms** | .NET 8 AOT-ready Runtime |

---

## 🛠️ Quickstart & Local Setup

### Prerequisites
* **Python 3.10+**
* **.NET 8.0 SDK** (Optional for C# console)
* **FFmpeg** installed and accessible in system `PATH`

### 1. Clone & Install
```bash
git clone https://github.com/propaper12/TalentPulse-Multimodal-AI.git
cd TalentPulse-Multimodal-AI
pip install -r requirements.txt
```

### 2. Start the Server & Studio
```bash
python main.py
```
Open your browser at: **`http://127.0.0.1:8000`**

* Click **`🎥 Canlı Aday Mülakat Odası`** to test real-time WebCam BlazeFace gaze tracking, audio visualizer, and phone detection!
* Click **`20 Aday (Büyük Veri Testi)`** to ingest simulated stream batches and observe the live DuckDB OLAP charts.

### 3. Run the C# .NET 8 Integration Client
```bash
cd HumanOreIntegration
dotnet run
```

---

## 📂 Project Directory Structure

```text
├── main.py                     # FastAPI application & REST endpoints
├── storage.py                  # DuckDB columnar OLAP schema & query engine
├── media_processor.py          # FFmpeg video/audio demuxing & acoustic SNR DSP
├── agent_engine.py             # ReAct Autonomous HR Agent (Observation & Action)
├── dynamic_questions.py        # Real-time keyword catcher & contextual questions
├── queue_stream.py             # In-Memory multi-topic event stream (Pub/Sub)
├── config.py                   # Role competency matrix & database configuration
├── dashboard.html              # Modern responsive UI with Tailwind & Chart.js
├── requirements.txt            # Python dependencies
├── HumanOreIntegration/        # C# .NET 8 Enterprise Console
│   ├── Program.cs              # LINQ analytics consumer & radar reporter
│   ├── EvaluationResultDto.cs  # Strongly typed multimodal DTOs
│   └── HumanOreIntegration.csproj
└── media_storage/              # Recorded WebM, demuxed WAVs, and thumbnails
```

---

## 👨‍💻 Author

**Ömer Çakan**  
*Management Information Systems (YBS / MIS) Graduate • Data & AI Engineer*  
* **GitHub:** [@propaper12](https://github.com/propaper12)  
* **LinkedIn:** [linkedin.com/in/ömer-çakan-819751261](https://www.linkedin.com/in/%C3%B6mer-%C3%A7akan-819751261)  
* **Email:** omercakan5@gmail.com

---

## 📜 License
Distributed under the **MIT License**. See `LICENSE` for more information.
