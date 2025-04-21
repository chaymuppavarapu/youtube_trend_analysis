# YouTube Trends Analysis Dashboard

A real-time dashboard that analyzes trending YouTube videos across different regions. Built with Python, Streamlit, and the YouTube Data API.

## Features

- Real-time trending videos data
- Multi-region support
- Interactive visualizations
- Engagement analytics
- Detailed video statistics

## Setup

1. Clone the repository:
```bash
git clone https://github.com/chaymuppavarapu/youtube-trends-dashboard.git
cd youtube-trends-dashboard
```

2. Create a virtual environment and activate it:
```bash
python -m venv yt_env
# On Windows:
.\yt_env\Scripts\activate
# On Unix or MacOS:
source yt_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your YouTube API key:
```
YOUTUBE_API_KEY="your-api-key-here"
```

5. Run the dashboard:
```bash
streamlit run dashboard.py
```

## Deployment

The dashboard can be deployed to Streamlit Cloud:

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy the app

Make sure to add your `YOUTUBE_API_KEY` to the Streamlit Cloud secrets.

## Environment Variables

- `YOUTUBE_API_KEY`: Your YouTube Data API key (required)

## License

MIT License 