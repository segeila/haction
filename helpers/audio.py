from gtts import gTTS
from pydub import AudioSegment

def generate_audio(summary_text, path):
    # Create a gTTS object
    tts = gTTS(text = summary_text, lang='en')

    # Save the audio in memory
    tts.save("media/voice.mp3")

def add_background_music(voice_path, music_path, output_path, delay_seconds=5, volume_adjustment=-20):
    """
    Adds background music to a voice layover with a specified delay.
    
    Parameters:
        voice_path (str): Path to the voice layover audio file.
        music_path (str): Path to the background music audio file.
        output_path (str): Path to save the combined audio.
        delay_seconds (int): The delay for the voice layover in seconds.
        volume_adjustment (int): Amount to adjust the volume of the background music. Negative to reduce volume.
    
    Returns:
        None: The combined audio is saved to `output_path`.
    """
    # Load voice and music
    voice = AudioSegment.from_file(voice_path, format="mp3")
    music = AudioSegment.from_file(music_path, format="mp3")[3*1000:]
    
    # Ensure both audio clips have the same frame rate and number of channels
    voice = voice.set_frame_rate(music.frame_rate).set_channels(music.channels)
    
    # Optionally, lower the volume of the music
    music = music + volume_adjustment
    
    # Add delay to voice layover
    delay_time = delay_seconds * 1000  # Convert to milliseconds
    voice = AudioSegment.silent(duration=delay_time) + voice + AudioSegment.silent(duration=delay_time)
    
    # Calculate lengths and make sure they match
    voice_length = len(voice)
    music_length = len(music)
    
    # If the music is shorter/longer, you might have to loop/cut it
    if music_length < voice_length:
        loops = voice_length // music_length + 1
        music = music * loops

    music = music[:voice_length]
    
    # Overlay voice on music
    combined = music.overlay(voice)
    
    # Export the mixed audio
    combined.export(output_path, format="mp3")

import requests