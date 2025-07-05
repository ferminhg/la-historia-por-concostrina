#!/usr/bin/env python3

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.infrastructure.transcriptor.openai_audio_transcriptor import OpenAIAudioTranscriptor
from app.domain.entities.episode import Episode


def main():
    # Verificar que existe la variable de entorno OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("   Set it with: export OPENAI_API_KEY='your-api-key'")
        return 1
    
    # Crear un episodio de ejemplo
    episode = Episode(
        title="Test Episode",
        description="Example episode for testing OpenAI transcription",
        url="https://example.com/test.mp3",
        published_date=datetime.now(),
        duration=900,  # 15 minutos
        file_size=36000000,  # ~36MB
        local_file_path="../audios/2025_06_18_19.mp3"  # Usar un archivo real si existe
    )
    
    # Verificar que el archivo de audio existe
    if not os.path.exists(episode.local_file_path):
        print(f"❌ Error: Audio file not found: {episode.local_file_path}")
        print("   Make sure to run podcast_crawler first to download audio files")
        return 1
    
    print(f"🎵 Transcribing audio file: {episode.local_file_path}")
    print(f"📝 Episode: {episode.title}")
    
    # Crear el transcriptor de OpenAI
    transcriptor = OpenAIAudioTranscriptor()
    
    # Transcribir el episodio
    transcription = transcriptor.transcribe(episode)
    
    if transcription:
        print(f"✅ Transcription completed successfully!")
        print(f"📊 Text length: {len(transcription.text)} characters")
        print(f"🌍 Language: {transcription.language}")
        print(f"⏱️  Duration: {transcription.duration} seconds")
        print(f"📅 Created at: {transcription.created_at}")
        print("\n📝 Transcription preview (first 500 characters):")
        print("-" * 60)
        print(transcription.text[:500])
        if len(transcription.text) > 500:
            print("...")
        print("-" * 60)
        
        # Guardar la transcripción en un archivo
        output_file = f"transcription_example_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcription.text)
        print(f"💾 Transcription saved to: {output_file}")
        
    else:
        print("❌ Transcription failed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())