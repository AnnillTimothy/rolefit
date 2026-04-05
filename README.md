# RoleFit

> **Know your fit before you apply.**

RoleFit is an AI-powered career match platform built with Flask. Upload your resume (PDF), paste a job description (or URL), and receive an instant match score, honest analysis, and a tailored cover letter — all in seconds.

---

## Features

- **Match Scoring** — Weighted algorithm evaluates skills, experience, education, and industry alignment.
- **AI Analysis** — Brutally honest breakdown of strengths, gaps, and competitiveness.
- **Cover Letter Generation** — Personalized, non-generic cover letter tailored to the specific role.
- **PDF Parsing** — Extracts text from uploaded PDF resumes using `pdfplumber`.
- **URL Extraction** — Optionally paste a job posting URL instead of raw text.
- **Minimalist UI** — Clean, whitespace-driven design with GSAP scroll animations.
- **Loading Experience** — Animated SVG logo on first load; breathing logo overlay during analysis.

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python · Flask                      |
| AI        | Mistral AI (`mistral-large-latest`) |
| PDF       | pdfplumber                          |
| Scraping  | BeautifulSoup · requests            |
| Frontend  | HTML · CSS · Vanilla JS · GSAP     |
| Fonts     | Inter (Google Fonts)                |

---

## Getting Started

### Prerequisites

- Python 3.9+
- A [Mistral AI](https://mistral.ai) API key

### Installation

```bash
git clone https://github.com/AnnillTimothy/rolefit.git
cd rolefit
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
MISTRAL_API_KEY=your_mistral_api_key_here
SECRET_KEY=your_secret_key_here
```

### Run

```bash
python application.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Project Structure

```
rolefit/
├── application.py          # Flask app — routes, AI calls, scoring logic
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── styles.css      # Complete design system
│   └── js/
│       └── main.js         # GSAP animations, UI interactions
├── templates/
│   ├── index.html          # Landing page + upload form
│   └── result.html         # Results page (score, analysis, cover letter)
└── README.md
```

---

## How It Works

1. **Upload** your PDF resume.
2. **Paste** a job description or URL.
3. **Receive** a match score (0–100), detailed analysis, and a tailored cover letter.

The scoring algorithm weights:
- Required skills match (40%)
- Preferred skills match (10%)
- Years of experience (25%)
- Education alignment (5%)
- Industry overlap (10%)

---

## License

This project is provided as-is for personal and educational use.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<sub>Front end by Claude, back end by me and GPT(annilltimothy.dev/margaret)</sub>
