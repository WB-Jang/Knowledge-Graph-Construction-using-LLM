"""
Embedder for generating embeddings from text using sentence transformers
Optimized for RTX-4080 8GB VRAM
"""
from typing import List, Optional

import torch
from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Generate embeddings from text using sentence transformers
    Optimized for RTX-4080 with 8GB VRAM
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
        batch_size: int = 32,
    ):
        """
        Initialize Embedder

        Args:
            model_name: Name of the sentence transformer model
            device: Device to use ('cuda', 'cpu', or None for auto)
            batch_size: Batch size for encoding
        """
        self.model_name = model_name
        self.batch_size = batch_size

        # Auto-detect device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        print(f"Initializing embedder with model: {model_name}")
        print(f"Using device: {self.device}")

        # Load model
        self.model = SentenceTransformer(model_name, device=self.device)

        # Optimize for 8GB VRAM
        if self.device == "cuda":
            # Enable memory efficient attention if available
            if hasattr(torch, "cuda") and torch.cuda.is_available():
                torch.cuda.empty_cache()

        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Embedding dimension: {self.embedding_dim}")

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Input text

        Returns:
            List of floats representing the embedding
        """
        embedding = self.model.encode(text, convert_to_tensor=False, show_progress_bar=False)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of input texts

        Returns:
            List of embeddings
        """
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_tensor=False,
            show_progress_bar=True,
        )
        return embeddings.tolist()

    def get_embedding_dim(self) -> int:
        """Get the dimension of the embeddings"""
        return self.embedding_dim

    def clear_cache(self):
        """Clear CUDA cache to free memory"""
        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("CUDA cache cleared")
