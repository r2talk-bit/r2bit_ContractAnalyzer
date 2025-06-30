# R2Bit Contract Analyzer

A Streamlit-based web application for analyzing legal contracts using AI. This tool helps users upload and analyze legal documents, extracting key information and providing insights through natural language processing.

## Features

- **PDF Document Processing**: Extract text from uploaded PDF documents
- **AI-Powered Analysis**: Utilizes OpenAI's language models for contract analysis
- **User-Friendly Interface**: Simple and intuitive web interface built with Streamlit
- **Secure**: API key management through environment variables or Streamlit secrets
- **Responsive Design**: Works on both desktop and mobile devices

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd r2bit_ContractAnalyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Option 1: Set as environment variable:
     ```bash
     set OPENAI_API_KEY=your-api-key-here  # Windows
     export OPENAI_API_KEY=your-api-key-here  # macOS/Linux
     ```
   - Option 2: Create a `.streamlit/secrets.toml` file with:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Upload a PDF document using the file uploader

4. Wait for the document to be processed and analyzed

5. View the analysis results and extracted information

## Project Structure

```
r2bit_ContractAnalyzer/
├── .streamlit/
│   └── secrets.toml          # For storing API keys (gitignored)
├── utils/
│   ├── llm.py               # LLM API interaction logic
│   └── prompt.py            # Prompt engineering utilities
├── assets/
│   └── style.css           # Custom styling
├── example/                  # Example documents
├── .gitignore
├── Dockerfile               # For containerization
├── README.md                # This file
├── requirements.txt         # Python dependencies
└── streamlit_app.py         # Main application file
```

## Dependencies

- streamlit==1.46.1
- openai==1.70.0
- anthropic==0.8.1
- python-dotenv==1.1.0
- pandas==2.2.3
- numpy==1.26.4
- matplotlib==3.8.0
- pdfplumber==0.11.6
- python-docx==1.2.0
- watchdog==6.0.0

## Docker Support

The application includes a Dockerfile for containerized deployment. To build and run with Docker:

```bash
docker build -t r2bit-contract-analyzer .
docker run -p 8501:8501 -e OPENAI_API_KEY=your-api-key-here r2bit-contract-analyzer
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository.
