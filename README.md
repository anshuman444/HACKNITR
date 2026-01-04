# AuditFlow – Real-time M&A Due Diligence Engine

**AuditFlow** is a powerful AI-driven intelligence engine designed for live M&A due diligence. It monitors financial filings, parses complex PDF data with layout awareness, and uses a **Master Agent** architecture to identify risks in real-time.

## 🚀 Key Features
- **Real-time Monitoring**: Automatically watches local folders for new financial PDFs.
- **Layout-Aware Parsing**: Uses `Docling` specifically tuned for high-fidelity markdown extraction.
- **Master Agent Architecture**: Consolidated analysis combining Litigation, Covenant Breaches, and Verification in a single, high-speed API call.
- **Rate-Limit Resilient**: Built-in exponential backoff and "Extreme Patience" logic for reliable performance on Gemini Free Tier.
- **Interactive Dashboard**: Streamlit-based UI for live document feed and risk analysis.

## 🛠️ Tech Stack
- **Framework**: Streamlit
- **LLM**: Google Gemini 1.5 Flash (via `google-generativeai`)
- **Parsing**: Docling
- **Indexing**: Custom JSON-based Document Store
- **Language**: Python 3.10+

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd HACKNITR
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Data**:
   Place your PDF filings in `data/filings/` and run the ingestion:
   ```bash
   python main.py
   ```

## 🖥️ Usage

Start the dashboard:
```bash
streamlit run ui/dashboard.py
```
Open your browser to `http://localhost:8501`.

## 📂 Project Structure
- `/agents`: Intelligent LLM agents (Litigation, Covenant, Verifier, and Master).
- `/parsing`: High-fidelity PDF to Markdown conversion.
- `/ui`: Streamlit dashboard and user interface.
- `/config`: Global configurations and LLM retry logic.
- `/data`: Storage for filings and processed indices.

---
Built for **HACKNITR** 🚀
