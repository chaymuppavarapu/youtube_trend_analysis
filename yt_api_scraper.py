from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from the .env file
load_dotenv(dotenv_path="C:/Users/schai/OneDrive/Desktop/youtube-trend-analysis/.env")

# Access the API key from the environment
api_key = os.getenv("YOUTUBE_API_KEY")

# Check if the API key is loaded correctly
if not api_key:
    raise ValueError("API key not found. Make sure it's in your .env file.")

def get_trending_videos(max_results=10, region_code="US"):
    """
    Fetch trending videos from YouTube.
    
    Args:
        max_results (int): Number of videos to fetch (default: 10)
        region_code (str): Country code for trending videos (default: "US")
    
    Returns:
        list: List of dictionaries containing video information
    """
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()

        # Parse and return the trending videos
        trending_videos = []
        for item in response['items']:
            video_data = {
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'description': item['snippet']['description'],
                'video_id': item['id'],
                'url': f"https://www.youtube.com/watch?v={item['id']}",
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'duration': item['contentDetails']['duration']
            }
            trending_videos.append(video_data)
        return trending_videos

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    trending = get_trending_videos(max_results=10)
    if trending:
        for video in trending:
            print(f"Title: {video['title']}")
            print(f"Channel: {video['channel']}")
            print(f"Views: {video['view_count']:,}")
            print(f"Likes: {video['like_count']:,}")
            print(f"Comments: {video['comment_count']:,}")
            print(f"URL: {video['url']}")
            print("-" * 50)
    else:
        print("Failed to fetch trending videos.")
