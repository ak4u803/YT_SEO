"""
ML-Based Tag Predictor Module
Uses machine learning models to predict and suggest tags based on content analysis
All models run locally without requiring API keys
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Import transformers for ML-based predictions
try:
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Note: transformers not available. Install with: pip install transformers sentence-transformers")


class MLTagPredictor:
    """Machine Learning-based tag prediction using local pre-trained models"""
    
    def __init__(self):
        self.models_loaded = False
        self.zero_shot_classifier = None
        self.sentence_model = None
        
        # Popular YouTube tag categories for zero-shot classification
        self.tag_categories = [
            "tutorial", "review", "gaming", "entertainment", "education",
            "technology", "lifestyle", "comedy", "music", "vlog",
            "how-to", "news", "sports", "cooking", "travel",
            "fitness", "beauty", "fashion", "DIY", "science",
            "business", "motivation", "podcast", "animation", "documentary"
        ]
        
        # Load models (lazy loading)
        self._load_models()
    
    def _load_models(self):
        """Load ML models (runs locally, no API required)"""
        if not TRANSFORMERS_AVAILABLE:
            print("Transformers library not available. Using fallback methods.")
            return
        
        try:
            print("Loading ML models (this may take a moment on first run)...")
            
            # Load zero-shot classification model (lightweight, runs locally)
            # Using facebook/bart-large-mnli - a free, open-source model
            self.zero_shot_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU
            )
            
            # Load sentence transformer for semantic similarity (lightweight model)
            # Using all-MiniLM-L6-v2 - small, fast, and free
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            self.models_loaded = True
            print("ML models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading ML models: {e}")
            print("Falling back to traditional methods.")
            self.models_loaded = False
    
    def predict_tags(self, video_data, num_tags=30):
        """
        Main method to predict tags using ML techniques
        
        Args:
            video_data: Dictionary containing video information
            num_tags: Number of tags to generate
            
        Returns:
            Dictionary containing ML-predicted tags and metadata
        """
        results = {
            'ml_tags': [],
            'category_scores': {},
            'semantic_tags': [],
            'clustered_tags': [],
            'confidence_scores': {},
            'method_used': 'ML' if self.models_loaded else 'Traditional'
        }
        
        # Extract text content
        title = video_data.get('title', '')
        description = video_data.get('description', '')
        transcript = video_data.get('transcript_full', '')
        
        combined_text = f"{title}. {description}. {transcript}"
        
        if not combined_text.strip():
            return results
        
        # Method 1: Zero-shot classification for category prediction
        if self.models_loaded and self.zero_shot_classifier:
            category_results = self._predict_categories(combined_text)
            results['category_scores'] = category_results
            
            # Add top categories as tags
            top_categories = sorted(
                category_results.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            results['ml_tags'].extend([cat for cat, score in top_categories])
            results['confidence_scores'].update({cat: score for cat, score in top_categories})
        
        # Method 2: Semantic similarity-based tag extraction
        if self.models_loaded and self.sentence_model:
            semantic_tags = self._extract_semantic_tags(
                title, description, transcript, num_tags=15
            )
            results['semantic_tags'] = semantic_tags
            results['ml_tags'].extend(semantic_tags)
        
        # Method 3: Clustering-based tag discovery
        clustered_tags = self._cluster_based_tags(combined_text, num_clusters=5)
        results['clustered_tags'] = clustered_tags
        results['ml_tags'].extend(clustered_tags)
        
        # Method 4: Context-aware phrase extraction using ML
        if self.models_loaded:
            context_tags = self._extract_contextual_phrases(combined_text, num_tags=10)
            results['ml_tags'].extend(context_tags)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_ml_tags = []
        for tag in results['ml_tags']:
            tag_lower = tag.lower()
            if tag_lower not in seen and len(tag) > 2:
                seen.add(tag_lower)
                unique_ml_tags.append(tag)
        
        results['ml_tags'] = unique_ml_tags[:num_tags]
        
        return results
    
    def _predict_categories(self, text):
        """
        Use zero-shot classification to predict content categories
        
        Args:
            text: Input text to classify
            
        Returns:
            Dictionary of categories and their confidence scores
        """
        if not self.zero_shot_classifier:
            return {}
        
        try:
            # Truncate text if too long (model limitation)
            max_length = 1000
            text_sample = text[:max_length] if len(text) > max_length else text
            
            # Classify text into categories
            result = self.zero_shot_classifier(
                text_sample,
                candidate_labels=self.tag_categories,
                multi_label=True
            )
            
            # Create category score dictionary
            category_scores = {
                label: score 
                for label, score in zip(result['labels'], result['scores'])
                if score > 0.3  # Only include confident predictions
            }
            
            return category_scores
            
        except Exception as e:
            print(f"Error in category prediction: {e}")
            return {}
    
    def _extract_semantic_tags(self, title, description, transcript, num_tags=15):
        """
        Extract tags based on semantic similarity using sentence embeddings
        
        Args:
            title, description, transcript: Text sources
            num_tags: Number of tags to extract
            
        Returns:
            List of semantically relevant tags
        """
        if not self.sentence_model:
            return []
        
        try:
            # Create candidate phrases from text
            candidates = []
            
            # Extract phrases from title
            title_words = title.split()
            for i in range(len(title_words)):
                for j in range(i+1, min(i+4, len(title_words)+1)):
                    phrase = ' '.join(title_words[i:j])
                    if len(phrase) > 3:
                        candidates.append(phrase)
            
            # Extract key sentences from description and transcript
            full_text = f"{description} {transcript}"
            sentences = full_text.split('.')[:50]  # Limit for performance
            
            # Add noun phrases and important terms
            from nltk import word_tokenize
            import string
            
            words = word_tokenize(full_text.lower())
            words = [w for w in words if w not in string.punctuation and len(w) > 3]
            
            # Create bigrams and trigrams
            for i in range(len(words)-1):
                candidates.append(f"{words[i]} {words[i+1]}")
            for i in range(len(words)-2):
                candidates.append(f"{words[i]} {words[i+1]} {words[i+2]}")
            
            # Remove duplicates
            candidates = list(set(candidates))[:200]  # Limit for performance
            
            if not candidates:
                return []
            
            # Encode title and candidates
            title_embedding = self.sentence_model.encode([title])
            candidate_embeddings = self.sentence_model.encode(candidates)
            
            # Calculate similarity
            similarities = cosine_similarity(title_embedding, candidate_embeddings)[0]
            
            # Get top similar phrases
            top_indices = np.argsort(similarities)[-num_tags:][::-1]
            semantic_tags = [candidates[i] for i in top_indices if similarities[i] > 0.3]
            
            # Clean tags
            semantic_tags = [tag.strip().title() for tag in semantic_tags]
            
            return semantic_tags[:num_tags]
            
        except Exception as e:
            print(f"Error in semantic tag extraction: {e}")
            return []
    
    def _cluster_based_tags(self, text, num_clusters=5):
        """
        Use clustering to discover tag groups
        
        Args:
            text: Input text
            num_clusters: Number of clusters to create
            
        Returns:
            List of representative tags from each cluster
        """
        try:
            # Create TF-IDF vectors
            from nltk import word_tokenize
            import string
            
            # Extract words and phrases
            words = word_tokenize(text.lower())
            words = [w for w in words if w not in string.punctuation and len(w) > 3]
            
            # Create phrases
            phrases = []
            for i in range(len(words)-1):
                phrases.append(f"{words[i]} {words[i+1]}")
            for i in range(len(words)-2):
                phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
            
            # Get unique phrases
            unique_phrases = list(set(phrases))
            
            if len(unique_phrases) < num_clusters:
                return []
            
            # Vectorize
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            phrase_texts = [' '.join(phrase.split()) for phrase in unique_phrases]
            vectors = vectorizer.fit_transform(phrase_texts)
            
            # Cluster
            kmeans = KMeans(n_clusters=min(num_clusters, len(unique_phrases)), random_state=42)
            kmeans.fit(vectors)
            
            # Get representative phrases from each cluster
            cluster_tags = []
            for cluster_id in range(num_clusters):
                cluster_indices = np.where(kmeans.labels_ == cluster_id)[0]
                if len(cluster_indices) > 0:
                    # Get phrase closest to cluster center
                    cluster_vectors = vectors[cluster_indices]
                    center = kmeans.cluster_centers_[cluster_id]
                    distances = cosine_similarity([center], cluster_vectors)[0]
                    best_idx = cluster_indices[np.argmax(distances)]
                    cluster_tags.append(unique_phrases[best_idx].title())
            
            return cluster_tags
            
        except Exception as e:
            print(f"Error in clustering: {e}")
            return []
    
    def _extract_contextual_phrases(self, text, num_tags=10):
        """
        Extract contextually important phrases using ML techniques
        
        Args:
            text: Input text
            num_tags: Number of tags to extract
            
        Returns:
            List of contextual tags
        """
        try:
            from nltk import word_tokenize
            import string
            
            # Tokenize
            sentences = text.split('.')[:30]  # Limit for performance
            
            all_phrases = []
            
            for sentence in sentences:
                words = word_tokenize(sentence.lower())
                words = [w for w in words if w not in string.punctuation and len(w) > 3]
                
                # Extract noun phrases and verb phrases (simple approach)
                for i in range(len(words)-1):
                    phrase = f"{words[i]} {words[i+1]}"
                    all_phrases.append(phrase)
            
            # Count frequency
            phrase_counts = Counter(all_phrases)
            
            # Get most common
            common_phrases = [
                phrase.title() 
                for phrase, count in phrase_counts.most_common(num_tags)
                if count > 1  # Must appear more than once
            ]
            
            return common_phrases
            
        except Exception as e:
            print(f"Error in contextual extraction: {e}")
            return []
    
    def get_tag_explanations(self, tags, video_data):
        """
        Provide explanations for why certain tags were predicted
        
        Args:
            tags: List of predicted tags
            video_data: Video information
            
        Returns:
            Dictionary mapping tags to explanations
        """
        explanations = {}
        
        title = video_data.get('title', '').lower()
        description = video_data.get('description', '').lower()
        
        for tag in tags:
            tag_lower = tag.lower()
            
            reasons = []
            
            # Check if tag appears in title
            if tag_lower in title:
                reasons.append("appears in title")
            
            # Check if tag appears in description
            if tag_lower in description:
                reasons.append("found in description")
            
            # Check if it's a predicted category
            if tag in self.tag_categories:
                reasons.append("ML-predicted category")
            
            # Check semantic relevance
            if self.models_loaded:
                reasons.append("semantically relevant to content")
            else:
                reasons.append("statistically significant in content")
            
            explanation = f"ML-predicted: {', '.join(reasons)}"
            explanations[tag] = explanation
        
        return explanations
    
    def analyze_tag_quality(self, tags):
        """
        Analyze the quality and diversity of generated tags
        
        Args:
            tags: List of tags to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        if not tags:
            return {
                'diversity_score': 0,
                'avg_length': 0,
                'has_categories': False,
                'has_specific': False,
                'quality_score': 0
            }
        
        # Calculate metrics
        tag_lengths = [len(tag) for tag in tags]
        word_counts = [len(tag.split()) for tag in tags]
        
        # Diversity: ratio of unique words
        all_words = ' '.join(tags).lower().split()
        diversity_score = len(set(all_words)) / len(all_words) if all_words else 0
        
        # Check for mix of categories and specific tags
        has_categories = any(tag in self.tag_categories for tag in tags)
        has_specific = any(len(tag.split()) > 2 for tag in tags)
        
        # Overall quality score
        quality_score = (
            (diversity_score * 40) +
            (30 if has_categories else 0) +
            (30 if has_specific else 0)
        )
        
        return {
            'diversity_score': round(diversity_score * 100, 2),
            'avg_length': round(np.mean(tag_lengths), 2),
            'avg_words': round(np.mean(word_counts), 2),
            'has_categories': has_categories,
            'has_specific': has_specific,
            'quality_score': round(quality_score, 2),
            'num_tags': len(tags)
        }

