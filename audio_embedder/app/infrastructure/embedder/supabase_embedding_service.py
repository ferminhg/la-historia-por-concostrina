import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client, Client

from ...application.services.embedding_service import EmbeddingService
from ...domain.entities.embedding import Embedding
from ...domain.entities.transcription import Transcription
from ...shared.semantic_chunker import SemanticChunker
from ...shared.logger import get_logger


class SupabaseEmbeddingService(EmbeddingService):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        
        # Configurar OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configurar Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados")
        
        self.supabase_client: Client = create_client(supabase_url, supabase_key)
        self.vector_store = SupabaseVectorStore(
            client=self.supabase_client,
            embedding=self.embeddings,
            table_name="podcast_embeddings",
            query_name="match_documents"
        )
        self.chunker = SemanticChunker()
    
    def extract_episode_metadata(self, transcription: Transcription) -> Dict[str, Any]:
        """Extrae metadatos del episodio desde la transcripción"""
        return {
            "episode_id": transcription.episode_id,
            "title": transcription.title or transcription.episode_id,
            "duration": transcription.duration or 0,
            "language": transcription.language or "es",
            "file_path": transcription.file_path or "",
        }
    
    def create_embeddings(self, transcription: Transcription) -> list[Embedding]:
        """Crea embeddings usando chunking semántico y los guarda en Supabase"""
        try:
            episode_metadata = self.extract_episode_metadata(transcription)
            chunks = self.chunker.chunk_transcript(transcription.text, episode_metadata)
            
            if not chunks:
                self.logger.warning(f"No chunks generated for {transcription.episode_id}")
                return []
            
            self.logger.info(f"Generated {len(chunks)} chunks for {transcription.episode_id}")
            
            # Procesar en batches para Supabase
            embeddings = []
            batch_size = 50
            
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                batch_texts = [chunk["content"] for chunk in batch_chunks]
                batch_metadatas = [chunk["metadata"] for chunk in batch_chunks]
                
                try:
                    # Enviar a Supabase
                    self.vector_store.add_texts(
                        texts=batch_texts,
                        metadatas=batch_metadatas
                    )
                    
                    # Crear objetos Embedding para el resultado
                    for j, chunk in enumerate(batch_chunks):
                        embedding = Embedding(
                            episode_id=transcription.episode_id,
                            transcription_id=transcription.episode_id,
                            vector=[],  # Vector vacío ya que está en Supabase
                            model_name="text-embedding-3-small",
                            created_at=datetime.now(),
                            chunk_index=chunk["metadata"]["chunk_index"],
                            chunk_text=chunk["content"],
                            metadata=chunk["metadata"],
                        )
                        embeddings.append(embedding)
                    
                    batch_num = (i // batch_size) + 1
                    total_batches = (len(chunks) + batch_size - 1) // batch_size
                    self.logger.info(f"Batch {batch_num}/{total_batches} processed successfully")
                    
                except Exception as e:
                    self.logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                    continue
            
            self.logger.info(f"Successfully created {len(embeddings)} embeddings for {transcription.episode_id}")
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error creating embeddings for {transcription.episode_id}: {str(e)}")
            return []
    
    def create_query_embedding(self, query_text: str) -> list[float]:
        """Crea embedding para una consulta"""
        try:
            embedding_vector = self.embeddings.embed_query(query_text)
            return embedding_vector
        except Exception as e:
            self.logger.error(f"Error creating query embedding: {str(e)}")
            return []
    
    def search_episodes(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Busca episodios similares usando Supabase"""
        try:
            self.logger.info(f"Searching for: '{query}' with k={k}")
            
            docs = self.vector_store.similarity_search(query=query, k=k)
            self.logger.info(f"Search successful, found {len(docs)} documents")
            
            results = []
            for doc in docs:
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in search: {str(e)}")
            return []