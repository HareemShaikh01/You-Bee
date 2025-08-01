from youtube_transcript_api import YouTubeTranscriptApi

def getTranscript(video_id):
    transcript_lists = YouTubeTranscriptApi().list(video_id)
    langs = list(transcript_lists._manually_created_transcripts.keys()) + list(transcript_lists._generated_transcripts.keys())
    # to get only unique values
    langs = list(set(langs))  
    transcript_object = YouTubeTranscriptApi().fetch(video_id,languages=langs)

    transcript = ""

    for snippet in transcript_object.snippets:
        transcript+=snippet.text
        
    return transcript



