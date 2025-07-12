import os
from typing import List, Dict, Any

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client, Client

from ...shared.logger import get_logger


class SearchSupabaseUseCase:
    """Caso de uso para búsquedas semánticas directas en Supabase"""
    
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
    
    def execute(self, query: str, k: int = 5, filter_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una búsqueda semántica en Supabase
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a devolver
            filter_metadata: Filtros opcionales para metadatos (e.g., {"episode_id": "20240520_190000"})
        
        Returns:
            Lista de resultados con contenido, metadatos y score de similitud
        """
        try:
            self.logger.info(f"🔍 Buscando en Supabase: '{query}' con k={k}")
            
            if filter_metadata:
                self.logger.info(f"📋 Aplicando filtros: {filter_metadata}")
            
            # Realizar búsqueda con filtros opcionales
            if filter_metadata:
                docs = self.vector_store.similarity_search(
                    query=query, 
                    k=k,
                    filter=filter_metadata
                )
            else:
                docs = self.vector_store.similarity_search(
                    query=query, 
                    k=k
                )
            
            self.logger.info(f"✅ Búsqueda exitosa, encontrados {len(docs)} documentos")
            
            results = []
            i = 0
            for doc in docs:
                i += 1
                result = {
                    "rank": i,
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    # "similarity_score": float(score),
                    "episode_id": doc.metadata.get("episode_id", "unknown"),
                    "title": doc.metadata.get("title", "unknown"),
                    "chunk_type": doc.metadata.get("chunk_type", "unknown"),
                    "estimated_timestamp_minutes": doc.metadata.get("estimated_timestamp_minutes", 0),
                }
                results.append(result)
                
                content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                self.logger.info(f"  [{i}] | Episodio: {result['episode_id']} | Contenido: {content_preview}")
            
            return results
            
        except Exception as e:
            import traceback
            self.logger.error(f"❌ Error en búsqueda Supabase: {str(e)}")
            self.logger.error(f"Tipo de error: {type(e).__name__}")
            self.logger.error(f"Traceback completo:\n{traceback.format_exc()}")
            return []
    
    def search_by_episode(self, query: str, episode_id: str, k: int = 5) -> List[Dict[str, Any]]:
        """Busca solo dentro de un episodio específico"""
        filter_metadata = {"episode_id": episode_id}
        return self.execute(query, k, filter_metadata)
    
    def search_by_date_range(self, query: str, start_date: str, end_date: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Busca en un rango de fechas específico
        
        Args:
            query: Consulta de búsqueda
            start_date: Fecha inicio en formato YYYYMMDD
            end_date: Fecha fin en formato YYYYMMDD
            k: Número de resultados
        """
        # Nota: Esta funcionalidad requeriría lógica adicional en Supabase
        # Por ahora, implementamos una búsqueda básica
        self.logger.warning("Búsqueda por rango de fechas no implementada completamente, usando búsqueda general")
        return self.execute(query, k)
    
    def get_episode_summary(self, episode_id: str) -> Dict[str, Any]:
        """Obtiene un resumen de chunks disponibles para un episodio"""
        try:
            # Búsqueda general para obtener todos los chunks del episodio
            results = self.search_by_episode("", episode_id, k=100)  # Buscar muchos chunks
            
            if not results:
                return {"episode_id": episode_id, "chunks_count": 0, "error": "No chunks found"}
            
            # Calcular estadísticas
            chunk_types = {}
            total_words = 0
            timestamps = []
            
            for result in results:
                chunk_type = result.get("chunk_type", "unknown")
                chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
                
                metadata = result.get("metadata", {})
                word_count = metadata.get("word_count", 0)
                total_words += word_count
                
                timestamp = metadata.get("estimated_timestamp_minutes", 0)
                if timestamp:
                    timestamps.append(timestamp)
            
            summary = {
                "episode_id": episode_id,
                "title": results[0].get("title", "unknown"),
                "chunks_count": len(results),
                "chunk_types": chunk_types,
                "total_words": total_words,
                "duration_minutes": max(timestamps) if timestamps else 0,
                "avg_chunk_words": total_words / len(results) if results else 0
            }
            
            self.logger.info(f"📊 Resumen del episodio {episode_id}: {summary['chunks_count']} chunks, {summary['total_words']} palabras")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error obteniendo resumen del episodio {episode_id}: {str(e)}")
            return {"episode_id": episode_id, "error": str(e)}