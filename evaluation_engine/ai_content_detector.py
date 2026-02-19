"""
AI-Generated Content Detection Module
Detects AI-generated submissions with high precision using linguistic analysis and pattern recognition.
"""

import re
import math
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import Counter, defaultdict
import numpy as np
from datetime import datetime


@dataclass
class AIGenerationIndicators:
    """Indicators of AI-generated content"""
    perplexity_score: float = 0.0
    burstiness_score: float = 0.0
    repetition_patterns: float = 0.0
    semantic_consistency: float = 0.0
    style_uniformity: float = 0.0
    coherence_markers: float = 0.0
    lexical_diversity: float = 0.0
    syntactic_regularity: float = 0.0
    semantic_entropy: float = 0.0
    pattern_predictability: float = 0.0


@dataclass
class DetectionResult:
    """Result of AI detection analysis"""
    is_ai_generated: bool
    confidence: float
    probability_score: float
    indicators: AIGenerationIndicators
    evidence: List[str]
    explanation: str


class AIGeneratedContentDetector:
    """
    Advanced detector for AI-generated content in student submissions.
    Uses multiple linguistic and statistical indicators for high-precision detection.
    """
    
    def __init__(self):
        # Detection thresholds
        self.thresholds = {
            "high_confidence": 0.85,
            "moderate_confidence": 0.70,
            "low_confidence": 0.50,
            "minimum_for_flagging": 0.65
        }
        
        # AI generation patterns (commonly observed in GPT outputs)
        self.ai_patterns = {
            "transitions": [
                "furthermore", "moreover", "additionally", "consequently", "therefore",
                "in conclusion", "to summarize", "in other words", "it is important to note",
                "it is worth noting", "it should be noted", "needless to say"
            ],
            "hedging": [
                "it is likely that", "it seems that", "appears to be", "suggests that",
                "indicates that", "demonstrates that", "shows that"
            ],
            "formality_markers": [
                "indeed", "thus", "hence", "thereby", "wherein", "herein", "therein",
                "notwithstanding", "aforementioned", "heretofore"
            ],
            "list_introducers": [
                "firstly", "secondly", "thirdly", "lastly", "finally",
                "first", "second", "third", "in the first place", "in the second place"
            ],
            "generic_openings": [
                "in recent years", "in today's world", "in the modern era",
                "with the advent of", "in the context of", "given the fact that"
            ],
            "concluding_phrases": [
                "in summary", "to conclude", "in closing", "to wrap up",
                "all in all", "taking everything into account"
            ]
        }
        
        # Perplexity baseline for human vs AI text
        self.perplexity_baselines = {
            "human_typical": (40, 80),  # Lower perplexity = more predictable
            "ai_typical": (20, 50),     # AI often has lower perplexity
            "suspicious_low": 15        # Very low perplexity is suspicious
        }
        
        # Burstiness patterns (AI tends to be more uniform)
        self.burstiness_thresholds = {
            "high_burstiness": 0.6,     # More human-like variation
            "low_burstiness": 0.3,      # More AI-like uniformity
            "suspicious_uniform": 0.2   # Very uniform is suspicious
        }
        
        # Repetitive patterns common in AI
        self.repetitive_patterns = {
            "sentence_starts": [
                "The", "This", "It", "In", "As", "However", "Therefore",
                "Furthermore", "Moreover", "Additionally"
            ],
            "consecutive_same_start": 3  # Flag if 3+ consecutive sentences start same way
        }
        
        # Semantic consistency patterns
        self.semantic_patterns = {
            "topic_drift_tolerance": 0.3,
            "coherence_threshold": 0.7
        }
        
    async def detect_ai_content(
        self,
        text: str,
        content_type: str = "report",
        additional_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Main detection method for AI-generated content
        
        Args:
            text: Content to analyze
            content_type: "report", "code", or "mixed"
            additional_context: Optional context about submission
            
        Returns:
            Comprehensive detection results
        """
        if not text or len(text.strip()) < 100:
            return {
                "error": "Text too short for reliable analysis",
                "is_ai_generated": False,
                "confidence": 0.0
            }
        
        # Calculate all indicators
        indicators = self._calculate_indicators(text, content_type)
        
        # Determine if AI-generated
        detection_result = self._determine_ai_generated(indicators)
        
        # Generate detailed analysis
        analysis = self._generate_detailed_analysis(indicators, text)
        
        # Compile evidence
        evidence = self._compile_evidence(indicators, text)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(detection_result, indicators)
        
        return {
            "is_ai_generated": detection_result.is_ai_generated,
            "confidence": round(detection_result.confidence, 3),
            "probability_score": round(detection_result.probability_score, 3),
            "detection_level": self._get_detection_level(detection_result.confidence),
            "indicators": {
                "perplexity_score": round(indicators.perplexity_score, 3),
                "burstiness_score": round(indicators.burstiness_score, 3),
                "repetition_patterns": round(indicators.repetition_patterns, 3),
                "semantic_consistency": round(indicators.semantic_consistency, 3),
                "style_uniformity": round(indicators.style_uniformity, 3),
                "lexical_diversity": round(indicators.lexical_diversity, 3),
                "syntactic_regularity": round(indicators.syntactic_regularity, 3),
                "pattern_predictability": round(indicators.pattern_predictability, 3)
            },
            "evidence": evidence,
            "detailed_analysis": analysis,
            "recommendations": recommendations,
            "verification_suggestions": self._get_verification_suggestions(detection_result),
            "content_type": content_type,
            "text_statistics": self._get_text_statistics(text),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _calculate_indicators(self, text: str, content_type: str) -> AIGenerationIndicators:
        """Calculate all AI detection indicators"""
        
        # Perplexity analysis (measures predictability)
        perplexity = self._calculate_perplexity(text)
        
        # Burstiness analysis (measures variation in sentence structure)
        burstiness = self._calculate_burstiness(text)
        
        # Repetition pattern analysis
        repetition = self._analyze_repetition_patterns(text)
        
        # Semantic consistency
        semantic_consistency = self._analyze_semantic_consistency(text)
        
        # Style uniformity
        style_uniformity = self._analyze_style_uniformity(text)
        
        # Coherence markers
        coherence = self._analyze_coherence_markers(text)
        
        # Lexical diversity
        lexical_diversity = self._calculate_lexical_diversity(text)
        
        # Syntactic regularity
        syntactic_regularity = self._analyze_syntactic_regularity(text)
        
        # Semantic entropy
        semantic_entropy = self._calculate_semantic_entropy(text)
        
        # Pattern predictability
        pattern_predictability = self._calculate_pattern_predictability(text)
        
        return AIGenerationIndicators(
            perplexity_score=perplexity,
            burstiness_score=burstiness,
            repetition_patterns=repetition,
            semantic_consistency=semantic_consistency,
            style_uniformity=style_uniformity,
            coherence_markers=coherence,
            lexical_diversity=lexical_diversity,
            syntactic_regularity=syntactic_regularity,
            semantic_entropy=semantic_entropy,
            pattern_predictability=pattern_predictability
        )
    
    def _calculate_perplexity(self, text: str) -> float:
        """
        Calculate perplexity-like measure for text predictability
        Lower perplexity = more predictable = more likely AI
        """
        sentences = self._get_sentences(text)
        
        if len(sentences) < 3:
            return 50.0  # Neutral for short text
        
        # Calculate sentence length variance
        lengths = [len(s.split()) for s in sentences]
        avg_length = np.mean(lengths)
        
        # Predictability based on regular patterns
        predictable_patterns = 0
        total_sentences = len(sentences)
        
        for pattern_list in self.ai_patterns.values():
            for pattern in pattern_list:
                count = text.lower().count(pattern)
                predictable_patterns += count
        
        # Normalize
        pattern_density = predictable_patterns / len(text.split())
        
        # Length regularity (AI tends to be more regular)
        length_std = np.std(lengths)
        length_regularity = 1 / (1 + length_std / 5)  # Normalize
        
        # Combined perplexity score (lower = more predictable)
        perplexity = 50 * (1 - pattern_density * 2) * (0.5 + length_regularity * 0.5)
        
        return max(10, min(100, perplexity))
    
    def _calculate_burstiness(self, text: str) -> float:
        """
        Calculate burstiness - measure of variation in text
        AI tends to have lower burstiness (more uniform)
        """
        sentences = self._get_sentences(text)
        
        if len(sentences) < 5:
            return 0.5  # Neutral
        
        # Measure sentence length variation
        lengths = [len(s.split()) for s in sentences]
        
        # Calculate coefficient of variation
        mean_len = np.mean(lengths)
        std_len = np.std(lengths)
        
        cv = std_len / mean_len if mean_len > 0 else 0
        
        # Burstiness score (higher = more human-like variation)
        burstiness = min(cv * 2, 1.0)
        
        return burstiness
    
    def _analyze_repetition_patterns(self, text: str) -> float:
        """Analyze repetitive patterns in text"""
        sentences = self._get_sentences(text)
        
        if len(sentences) < 3:
            return 0.5
        
        # Check for repetitive sentence starts
        starts = [s.split()[0] if s.split() else "" for s in sentences if s.strip()]
        
        # Count consecutive identical starts
        consecutive_matches = 0
        max_consecutive = 0
        
        for i in range(1, len(starts)):
            if starts[i] == starts[i-1]:
                consecutive_matches += 1
                max_consecutive = max(max_consecutive, consecutive_matches)
            else:
                consecutive_matches = 0
        
        # Check for repetitive phrases
        phrases = self._get_ngrams(text, 3)
        phrase_counts = Counter(phrases)
        repetitive_phrases = sum(1 for count in phrase_counts.values() if count > 2)
        
        # Combine metrics
        start_repetition = min(max_consecutive / 5, 1.0)  # Normalize
        phrase_repetition = min(repetitive_phrases / 10, 1.0)
        
        # High repetition score = more AI-like
        repetition_score = (start_repetition * 0.6 + phrase_repetition * 0.4)
        
        return repetition_score
    
    def _analyze_semantic_consistency(self, text: str) -> float:
        """Analyze semantic consistency across the text"""
        paragraphs = self._get_paragraphs(text)
        
        if len(paragraphs) < 2:
            return 0.5
        
        # Extract key terms from each paragraph
        paragraph_terms = []
        for para in paragraphs:
            terms = self._extract_key_terms(para)
            paragraph_terms.append(set(terms))
        
        # Calculate semantic consistency between consecutive paragraphs
        consistencies = []
        for i in range(len(paragraph_terms) - 1):
            if paragraph_terms[i] and paragraph_terms[i+1]:
                # Jaccard similarity
                intersection = len(paragraph_terms[i] & paragraph_terms[i+1])
                union = len(paragraph_terms[i] | paragraph_terms[i+1])
                similarity = intersection / union if union > 0 else 0
                consistencies.append(similarity)
        
        # High consistency = more AI-like
        avg_consistency = np.mean(consistencies) if consistencies else 0.5
        
        return avg_consistency
    
    def _analyze_style_uniformity(self, text: str) -> float:
        """Analyze uniformity in writing style"""
        sentences = self._get_sentences(text)
        
        if len(sentences) < 5:
            return 0.5
        
        # Analyze sentence complexity
        complexities = []
        for sentence in sentences:
            words = sentence.split()
            # Simple complexity metric: clauses (commas, conjunctions)
            clauses = sentence.count(',') + sentence.count(';')
            clauses += len(re.findall(r'\b(and|but|or|nor|for|so|yet)\b', sentence))
            complexities.append(clauses)
        
        # Measure uniformity in complexity
        complexity_std = np.std(complexities)
        
        # Low variance = more uniform = more AI-like
        uniformity = 1 / (1 + complexity_std)
        
        # Check for consistent transitions
        transition_count = sum(text.lower().count(t) for t in self.ai_patterns["transitions"])
        transition_density = transition_count / len(sentences)
        
        # Combine metrics
        style_uniformity = (uniformity * 0.6 + min(transition_density * 3, 1.0) * 0.4)
        
        return style_uniformity
    
    def _analyze_coherence_markers(self, text: str) -> float:
        """Analyze coherence markers in text"""
        text_lower = text.lower()
        
        # Count coherence markers
        coherence_markers = {
            "transitions": sum(text_lower.count(t) for t in self.ai_patterns["transitions"]),
            "hedging": sum(text_lower.count(h) for h in self.ai_patterns["hedging"]),
            "list_introducers": sum(text_lower.count(l) for l in self.ai_patterns["list_introducers"]),
            "concluding_phrases": sum(text_lower.count(c) for c in self.ai_patterns["concluding_phrases"])
        }
        
        total_words = len(text.split())
        
        # Calculate density of coherence markers
        total_markers = sum(coherence_markers.values())
        marker_density = total_markers / total_words if total_words > 0 else 0
        
        # High density of coherence markers = more AI-like
        coherence_score = min(marker_density * 20, 1.0)
        
        return coherence_score
    
    def _calculate_lexical_diversity(self, text: str) -> float:
        """Calculate lexical diversity (type-token ratio)"""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        if len(words) < 10:
            return 0.5
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # TTR (Type-Token Ratio)
        ttr = unique_words / total_words
        
        # Normalize: Human text typically has higher diversity
        # AI tends to reuse words more
        diversity_score = 1 - ttr  # Invert: lower diversity = higher score
        
        return diversity_score
    
    def _analyze_syntactic_regularity(self, text: str) -> float:
        """Analyze regularity in sentence syntax"""
        sentences = self._get_sentences(text)
        
        if len(sentences) < 5:
            return 0.5
        
        # Analyze sentence patterns
        patterns = []
        for sentence in sentences:
            # Create pattern: word length sequence
            words = sentence.split()
            pattern = tuple(len(w) for w in words[:5])  # First 5 words
            patterns.append(pattern)
        
        # Count pattern frequencies
        pattern_counts = Counter(patterns)
        
        # Calculate entropy of patterns
        total = len(patterns)
        entropy = 0
        for count in pattern_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Normalize entropy (max for uniform distribution)
        max_entropy = math.log2(len(pattern_counts)) if len(pattern_counts) > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        # Low entropy = high regularity = AI-like
        regularity = 1 - normalized_entropy
        
        return regularity
    
    def _calculate_semantic_entropy(self, text: str) -> float:
        """Calculate semantic entropy (topic variation)"""
        paragraphs = self._get_paragraphs(text)
        
        if len(paragraphs) < 2:
            return 0.5
        
        # Extract semantic signatures
        signatures = []
        for para in paragraphs:
            words = re.findall(r'\b[a-zA-Z]{4,}\b', para.lower())
            word_freq = Counter(words)
            signature = tuple(sorted([w for w, _ in word_freq.most_common(10)]))
            signatures.append(signature)
        
        # Calculate variation between signatures
        variations = []
        for i in range(len(signatures) - 1):
            set1 = set(signatures[i])
            set2 = set(signatures[i + 1])
            if set1 or set2:
                jaccard = len(set1 & set2) / len(set1 | set2)
                variations.append(1 - jaccard)  # Variation = 1 - similarity
        
        avg_variation = np.mean(variations) if variations else 0.5
        
        # Low variation = low entropy = AI-like
        entropy_score = 1 - avg_variation
        
        return entropy_score
    
    def _calculate_pattern_predictability(self, text: str) -> float:
        """Calculate how predictable the writing patterns are"""
        text_lower = text.lower()
        
        # Count AI-specific patterns
        ai_pattern_count = 0
        for category, patterns in self.ai_patterns.items():
            for pattern in patterns:
                ai_pattern_count += text_lower.count(pattern)
        
        # Normalize by text length
        word_count = len(text.split())
        pattern_density = ai_pattern_count / word_count if word_count > 0 else 0
        
        # Check for formulaic structures
        formulaic_indicators = 0
        
        # Check for "In conclusion" type endings
        if re.search(r'in\s+conclusion[,:;]', text_lower):
            formulaic_indicators += 1
        
        # Check for numbered lists
        if re.search(r'\b(first|second|third)[\s,]', text_lower):
            formulaic_indicators += 1
        
        # Check for generic openings
        generic_openings = [
            r'in\s+recent\s+years',
            r'in\s+today\'s\s+world',
            r'with\s+the\s+advent\s+of',
            r'in\s+the\s+modern\s+era'
        ]
        for opening in generic_openings:
            if re.search(opening, text_lower):
                formulaic_indicators += 0.5
        
        # Combine metrics
        predictability = min(pattern_density * 15 + formulaic_indicators * 0.2, 1.0)
        
        return predictability
    
    def _determine_ai_generated(self, indicators: AIGenerationIndicators) -> DetectionResult:
        """Determine if content is AI-generated based on indicators"""
        
        # Weights for different indicators
        weights = {
            "perplexity": 0.15,
            "burstiness": 0.20,
            "repetition": 0.15,
            "semantic_consistency": 0.10,
            "style_uniformity": 0.15,
            "coherence": 0.10,
            "lexical_diversity": 0.10,
            "syntactic_regularity": 0.10,
            "pattern_predictability": 0.15
        }
        
        # Normalize perplexity (invert: low perplexity = high AI probability)
        normalized_perplexity = 1 - (indicators.perplexity_score / 100)
        
        # Invert burstiness (high burstiness = low AI probability)
        normalized_burstiness = 1 - indicators.burstiness_score
        
        # Calculate weighted score
        score = (
            normalized_perplexity * weights["perplexity"] +
            normalized_burstiness * weights["burstiness"] +
            indicators.repetition_patterns * weights["repetition"] +
            indicators.semantic_consistency * weights["semantic_consistency"] +
            indicators.style_uniformity * weights["style_uniformity"] +
            indicators.coherence_markers * weights["coherence"] +
            indicators.lexical_diversity * weights["lexical_diversity"] +
            indicators.syntactic_regularity * weights["syntactic_regularity"] +
            indicators.pattern_predictability * weights["pattern_predictability"]
        )
        
        # Normalize to 0-1
        probability = min(score / sum(weights.values()), 1.0)
        
        # Determine if AI-generated
        is_ai = probability > self.thresholds["minimum_for_flagging"]
        
        # Calculate confidence
        if probability > self.thresholds["high_confidence"]:
            confidence = 0.90 + (probability - self.thresholds["high_confidence"]) * 0.1
        elif probability > self.thresholds["moderate_confidence"]:
            confidence = 0.75 + (probability - self.thresholds["moderate_confidence"]) * 0.15
        else:
            confidence = 0.50 + probability * 0.25
        
        # Generate evidence list
        evidence = []
        if normalized_perplexity > 0.7:
            evidence.append("Unusually low perplexity (high predictability)")
        if normalized_burstiness > 0.6:
            evidence.append("Low burstiness (uniform sentence structure)")
        if indicators.repetition_patterns > 0.6:
            evidence.append("Repetitive sentence patterns detected")
        if indicators.style_uniformity > 0.7:
            evidence.append("Highly uniform writing style")
        if indicators.pattern_predictability > 0.7:
            evidence.append("Predictable AI-specific patterns detected")
        
        # Generate explanation
        if is_ai:
            if confidence > 0.85:
                explanation = "High confidence AI-generated content detected. Multiple indicators show strong AI patterns."
            else:
                explanation = "Moderate confidence AI-generated content. Some AI patterns detected but with lower certainty."
        else:
            if confidence < 0.6:
                explanation = "Content appears to be human-written. Low AI pattern indicators detected."
            else:
                explanation = "Content shows some AI-like characteristics but not conclusive of AI generation."
        
        return DetectionResult(
            is_ai_generated=is_ai,
            confidence=confidence,
            probability_score=probability,
            indicators=indicators,
            evidence=evidence,
            explanation=explanation
        )
    
    def _generate_detailed_analysis(self, indicators: AIGenerationIndicators, text: str) -> Dict[str, Any]:
        """Generate detailed analysis of indicators"""
        
        sentences = self._get_sentences(text)
        paragraphs = self._get_paragraphs(text)
        
        # Perplexity analysis
        perplexity_analysis = {
            "score": round(indicators.perplexity_score, 3),
            "interpretation": "Low" if indicators.perplexity_score < 30 else "Medium" if indicators.perplexity_score < 60 else "High",
            "meaning": "Low perplexity suggests predictable patterns, common in AI text"
        }
        
        # Burstiness analysis
        burstiness_analysis = {
            "score": round(indicators.burstiness_score, 3),
            "interpretation": "Low" if indicators.burstiness_score < 0.3 else "Medium" if indicators.burstiness_score < 0.6 else "High",
            "meaning": "Low burstiness indicates uniform structure, more typical of AI"
        }
        
        # Detect specific AI patterns
        detected_patterns = self._detect_specific_patterns(text)
        
        # Sentence structure analysis
        structure_analysis = self._analyze_sentence_structures(sentences)
        
        return {
            "perplexity": perplexity_analysis,
            "burstiness": burstiness_analysis,
            "detected_patterns": detected_patterns,
            "sentence_structure": structure_analysis,
            "paragraph_flow": self._analyze_paragraph_flow(paragraphs),
            "vocabulary_analysis": self._analyze_vocabulary_patterns(text)
        }
    
    def _detect_specific_patterns(self, text: str) -> Dict[str, Any]:
        """Detect specific AI-specific patterns"""
        text_lower = text.lower()
        
        detected = {}
        for category, patterns in self.ai_patterns.items():
            found = []
            for pattern in patterns:
                count = text_lower.count(pattern)
                if count > 0:
                    found.append({"pattern": pattern, "count": count})
            
            if found:
                detected[category] = {
                    "count": len(found),
                    "patterns": found[:5]  # Top 5
                }
        
        return detected
    
    def _analyze_sentence_structures(self, sentences: List[str]) -> Dict[str, Any]:
        """Analyze sentence structures for AI patterns"""
        if not sentences:
            return {}
        
        # Analyze sentence lengths
        lengths = [len(s.split()) for s in sentences]
        
        # Analyze sentence starters
        starters = [s.split()[0] if s.split() else "" for s in sentences]
        starter_freq = Counter(starters)
        
        # Analyze sentence complexity (punctuation, clauses)
        complexities = []
        for sentence in sentences:
            complexity = sentence.count(',') + sentence.count(';') + sentence.count(':')
            complexities.append(complexity)
        
        return {
            "average_length": round(np.mean(lengths), 2),
            "length_variance": round(np.var(lengths), 2),
            "most_common_starters": starter_freq.most_common(5),
            "average_complexity": round(np.mean(complexities), 2),
            "length_distribution": {
                "short": len([l for l in lengths if l < 10]),
                "medium": len([l for l in lengths if 10 <= l <= 25]),
                "long": len([l for l in lengths if l > 25])
            }
        }
    
    def _analyze_paragraph_flow(self, paragraphs: List[str]) -> Dict[str, Any]:
        """Analyze flow between paragraphs"""
        if len(paragraphs) < 2:
            return {"message": "Insufficient paragraphs for flow analysis"}
        
        # Analyze transition words between paragraphs
        transition_words = ["furthermore", "moreover", "additionally", "however", "therefore", "consequently", "meanwhile", "similarly"]
        
        transitions_found = 0
        for i in range(len(paragraphs) - 1):
            para_end = paragraphs[i][-100:].lower() if len(paragraphs[i]) > 100 else paragraphs[i].lower()
            para_start = paragraphs[i+1][:100].lower() if len(paragraphs[i+1]) > 100 else paragraphs[i+1].lower()
            
            for word in transition_words:
                if word in para_end or word in para_start:
                    transitions_found += 1
        
        # Calculate flow score
        transition_rate = transitions_found / (len(paragraphs) - 1) if len(paragraphs) > 1 else 0
        
        return {
            "paragraph_count": len(paragraphs),
            "transition_words_found": transitions_found,
            "transition_rate": round(transition_rate, 3),
            "interpretation": "High" if transition_rate > 0.5 else "Medium" if transition_rate > 0.3 else "Low"
        }
    
    def _analyze_vocabulary_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze vocabulary patterns"""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Word frequency analysis
        word_freq = Counter(words)
        
        # Most common words
        most_common = word_freq.most_common(20)
        
        # Vocabulary richness
        unique_ratio = len(set(words)) / len(words) if words else 0
        
        # Academic vocabulary
        academic_words = ["analysis", "method", "approach", "system", "framework", "algorithm", "implementation", "evaluation"]
        academic_count = sum(1 for word in words if word in academic_words)
        academic_ratio = academic_count / len(words) if words else 0
        
        return {
            "total_words": len(words),
            "unique_words": len(set(words)),
            "vocabulary_richness": round(unique_ratio, 3),
            "academic_vocabulary_ratio": round(academic_ratio, 3),
            "most_common_words": most_common[:10],
            "lexical_sophistication": "High" if unique_ratio > 0.6 else "Medium" if unique_ratio > 0.4 else "Low"
        }
    
    def _compile_evidence(self, indicators: AIGenerationIndicators, text: str) -> List[Dict[str, Any]]:
        """Compile specific evidence of AI generation"""
        evidence = []
        
        # Pattern-based evidence
        text_lower = text.lower()
        
        # Check for formulaic phrases
        formulaic_phrases = [
            ("in conclusion", "Common AI conclusion marker"),
            ("furthermore", "Overused AI transition"),
            ("it is important to note", "AI hedging phrase"),
            ("as mentioned earlier", "Generic AI reference"),
            ("needless to say", "Verbose AI phrase"),
        ]
        
        for phrase, description in formulaic_phrases:
            count = text_lower.count(phrase)
            if count > 0:
                evidence.append({
                    "type": "formulaic_phrase",
                    "pattern": phrase,
                    "count": count,
                    "description": description,
                    "severity": "high" if count > 3 else "medium"
                })
        
        # Check for repetitive structures
        sentences = self._get_sentences(text)
        sentence_starts = [s.split()[0] if s.split() else "" for s in sentences]
        start_counts = Counter(sentence_starts)
        
        for start, count in start_counts.most_common(3):
            if count > 3:
                evidence.append({
                    "type": "repetitive_structure",
                    "pattern": f"Sentences starting with '{start}'",
                    "count": count,
                    "description": f"{count} sentences begin with the same word",
                    "severity": "high" if count > 5 else "medium"
                })
        
        # Check for unusual uniformity
        if indicators.style_uniformity > 0.8:
            evidence.append({
                "type": "uniformity",
                "pattern": "Writing style uniformity",
                "score": round(indicators.style_uniformity, 3),
                "description": "Unusually uniform writing style across document",
                "severity": "high"
            })
        
        return evidence
    
    def _generate_recommendations(self, result: DetectionResult, indicators: AIGenerationIndicators) -> List[str]:
        """Generate recommendations based on detection results"""
        recommendations = []
        
        if result.is_ai_generated:
            if result.confidence > 0.85:
                recommendations.append("**HIGH PRIORITY**: Content appears to be AI-generated with high confidence.")
                recommendations.append("Consider requiring student to submit work-in-progress drafts or process documentation.")
                recommendations.append("Request an oral defense or explanation of the work.")
            else:
                recommendations.append("**MODERATE CONCERN**: Some AI-generation indicators detected.")
                recommendations.append("Review content manually and compare with student's previous work.")
        
        else:
            recommendations.append("Content appears to be original human-written work.")
        
        # General recommendations
        recommendations.append("Always use multiple detection methods for conclusive results.")
        recommendations.append("Consider implementing draft submission requirements for major assignments.")
        
        return recommendations
    
    def _get_verification_suggestions(self, result: DetectionResult) -> List[str]:
        """Get suggestions for verifying AI detection results"""
        suggestions = []
        
        if result.is_ai_generated:
            suggestions.append("Request intermediate drafts or version history")
            suggestions.append("Conduct an oral examination on the content")
            suggestions.append("Compare with student's known writing samples")
            suggestions.append("Ask for explanation of specific technical decisions")
            suggestions.append("Request code walkthrough or live demonstration")
        
        return suggestions
    
    def _get_text_statistics(self, text: str) -> Dict[str, Any]:
        """Get basic text statistics"""
        words = text.split()
        sentences = self._get_sentences(text)
        paragraphs = self._get_paragraphs(text)
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "average_word_length": round(np.mean([len(w) for w in words]), 2) if words else 0,
            "average_sentence_length": round(len(words) / len(sentences), 2) if sentences else 0
        }
    
    def _get_detection_level(self, confidence: float) -> str:
        """Get detection level string"""
        if confidence >= 0.85:
            return "HIGH"
        elif confidence >= 0.70:
            return "MODERATE"
        elif confidence >= 0.50:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _get_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Preserve abbreviations
        text = re.sub(r'(Mr|Mrs|Dr|Prof|Sr|Jr|vs|Vol|vol|pp|et al)\.', r'\1<DOT>', text)
        
        sentences = re.split(r'[.!?]+\s+', text)
        sentences = [s.replace('<DOT>', '.').strip() for s in sentences]
        sentences = [s for s in sentences if len(s) > 10]
        
        return sentences
    
    def _get_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]
        return paragraphs
    
    def _get_ngrams(self, text: str, n: int) -> List[str]:
        """Extract n-grams from text"""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        ngrams = []
        
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = Counter(words)
        
        # Return most frequent terms
        return [term for term, _ in word_freq.most_common(15)]


# Export for use in other modules
__all__ = ['AIGeneratedContentDetector', 'AIGenerationIndicators', 'DetectionResult']
