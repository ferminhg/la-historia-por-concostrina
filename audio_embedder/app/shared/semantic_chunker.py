import re
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter


class SemanticChunker:
    """Chunker semántico especializado para transcripciones de podcast"""
    
    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""],
            keep_separator=True
        )
    
    def detect_topic_boundaries(self, text: str) -> List[int]:
        """Detecta límites de temas basado en patrones comunes en podcasts"""
        boundaries = [0]
        
        # Patrones que indican cambio de tema
        patterns = [
            r'\b(?:ahora|bueno|entonces|por otro lado|cambiando de tema|hablando de)\b',
            r'\b(?:siguiente pregunta|otra cosa|pasemos a|vamos a hablar)\b',
            r'\n\n',  # Párrafos nuevos
        ]
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for match in matches:
                boundaries.append(match.start())
        
        # Ordenar y eliminar duplicados
        boundaries = sorted(list(set(boundaries)))
        boundaries.append(len(text))
        
        return boundaries
    
    
    def chunk_transcript(self, text: str, episode_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Divide la transcripción en chunks semánticamente coherentes"""
        boundaries = self.detect_topic_boundaries(text)
        chunks = []
        
        # Estimar duración total (asumiendo ~150 palabras por minuto)
        total_words = len(text.split())
        estimated_duration_minutes = total_words / 150
        
        for i in range(len(boundaries) - 1):
            start_pos = boundaries[i]
            end_pos = boundaries[i + 1]
            
            segment = text[start_pos:end_pos].strip()
            
            if len(segment) < 100:  # Skip chunks muy pequeños
                continue
            
            # Si el segmento es muy largo, usar text_splitter tradicional
            if len(segment) > self.chunk_size:
                sub_chunks = self.text_splitter.split_text(segment)
                
                for j, sub_chunk in enumerate(sub_chunks):
                    # Calcular timestamp estimado
                    progress = (start_pos + j * len(sub_chunk)) / len(text)
                    estimated_timestamp = progress * estimated_duration_minutes
                    
                    chunk_metadata = {
                        **episode_metadata,
                        "chunk_index": len(chunks),
                        "estimated_timestamp_minutes": round(estimated_timestamp, 2),
                        "chunk_type": "semantic_sub",
                        "word_count": len(sub_chunk.split())
                    }
                    
                    chunks.append({
                        "content": sub_chunk,
                        "metadata": chunk_metadata
                    })
            else:
                # Calcular timestamp estimado
                progress = start_pos / len(text)
                estimated_timestamp = progress * estimated_duration_minutes
                
                chunk_metadata = {
                    **episode_metadata,
                    "chunk_index": len(chunks),
                    "estimated_timestamp_minutes": round(estimated_timestamp, 2),
                    "chunk_type": "semantic",
                    "word_count": len(segment.split())
                }
                
                chunks.append({
                    "content": segment,
                    "metadata": chunk_metadata
                })
        
        return chunks