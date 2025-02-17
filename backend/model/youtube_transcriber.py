import json
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, TooManyRequests

def get_transcript_one(video_id):
    try:
        print(f"Fetching transcript for video: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = JSONFormatter()
        json_formatted = formatter.format_transcript(transcript)
        
        with open('data/single.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_formatted)

        print(f"✅ Single transcript generated successfully for video: {video_id}")

    except TranscriptsDisabled:
        print(f"❌ Error: Transcripts are disabled for video {video_id}.")
    except NoTranscriptFound:
        print(f"❌ Error: No transcript found for video {video_id}.")
    except TooManyRequests:
        print("❌ Error: Too many requests. Please wait and try again later.")
    except Exception as e:
        print(f"❌ Unexpected error for video {video_id}: {e}")

def get_transcript_all(video_ids):
    json_file_path = 'data/multi.json'
    
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                transcripts = json.load(file)
                if not isinstance(transcripts, list):
                    transcripts = []
        else:
            transcripts = []
    except (FileNotFoundError, json.JSONDecodeError):
        transcripts = []
    
    formatter = JSONFormatter()
    
    for video_id in video_ids:
        try:
            print(f"Fetching transcript for video: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            json_formatted = json.loads(formatter.format_transcript(transcript))
            transcripts.extend(json_formatted)

            print(f"✅ Transcript added for video: {video_id}")

        except TranscriptsDisabled:
            print(f"❌ Error: Transcripts are disabled for video {video_id}. Skipping...")
        except NoTranscriptFound:
            print(f"❌ Error: No transcript found for video {video_id}. Skipping...")
        except TooManyRequests:
            print("❌ Error: Too many requests. Please wait and try again later.")
            break
        except Exception as e:
            print(f"❌ Unexpected error for video {video_id}: {e}. Skipping...")

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(transcripts, json_file, ensure_ascii=False, indent=4)
    
    print("✅ Multi transcript JSON updated successfully!")
