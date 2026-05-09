import numpy as np
import ollama


class EmbeddingService:
    
    NOMIC_MODEL_NAME="nomic-embed-text"
    


    @staticmethod
    def generate_embedding(text: str) -> list[float]:
        """Converts a string into a list of floats using Ollama."""
        response: ollama.EmbedResponse = ollama.embed(model= EmbeddingService.NOMIC_MODEL_NAME, input=text)
        return response.embeddings[0]
    
    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        """Calculates similarity between two vectors (1.0 is identical)."""
        if vec_a is None or vec_b is None:
            return 0.0
            
        a = np.array(vec_a)
        b = np.array(vec_b)
        
        # Pure math: dot(a, b) / (||a|| * ||b||)
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        return dot_product / (norm_a * norm_b)