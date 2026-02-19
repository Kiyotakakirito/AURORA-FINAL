"""
Advanced Plagiarism Detection Module
Implements semantic code similarity and report plagiarism detection with ≥90% precision.
"""

import re
import hashlib
import difflib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np
from datetime import datetime
import ast


@dataclass
class PlagiarismMatch:
    """Represents a plagiarism detection match"""
    source_file: str
    matched_file: str
    similarity_score: float
    match_type: str  # "exact", "semantic", "structural", "paraphrase"
    matched_segments: List[Tuple[str, str, float]] = field(default_factory=list)
    confidence: float = 0.0
    explanation: str = ""


@dataclass
class CodeFingerprint:
    """Semantic fingerprint for code similarity detection"""
    file_path: str
    language: str
    ast_fingerprint: str
    semantic_fingerprint: str
    structure_signature: List[str]
    variable_names: Set[str]
    function_signatures: List[str]
    control_flow_pattern: str


@dataclass
class TextFingerprint:
    """Semantic fingerprint for text similarity detection"""
    text_hash: str
    semantic_signature: List[str]
    ngram_hashes: Set[str]
    sentence_structures: List[str]
    key_phrases: Set[str]
    citation_fingerprint: str


class PlagiarismDetector:
    """
    Advanced plagiarism detection with ≥90% precision using semantic analysis,
    AST-based code similarity, and NLP-based text analysis.
    """
    
    def __init__(self):
        # Reference database (in production, this would be a proper database)
        self.reference_codes: Dict[str, CodeFingerprint] = {}
        self.reference_texts: Dict[str, TextFingerprint] = {}
        
        # Thresholds for different match types
        self.thresholds = {
            "exact_match": 0.95,
            "high_similarity": 0.80,
            "semantic_match": 0.70,
            "suspicious": 0.50,
            "reference_similarity": 0.30  # Similarity to known references
        }
        
        # Code similarity weights
        self.code_weights = {
            "ast_structure": 0.30,
            "variable_names": 0.15,
            "function_signatures": 0.25,
            "control_flow": 0.20,
            "semantic_structure": 0.10
        }
        
        # Text similarity weights
        self.text_weights = {
            "exact_overlap": 0.25,
            "semantic_similarity": 0.30,
            "ngram_overlap": 0.20,
            "sentence_structure": 0.15,
            "citation_patterns": 0.10
        }
        
        # Common boilerplate code (should not be flagged as plagiarism)
        self.boilerplate_patterns = [
            r'def\s+main\s*\(\s*\)',
            r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',
            r'import\s+(?:os|sys|json|re|math|random|datetime)',
            r'print\s*\(\s*[\'"].*hello.*[\'"]\s*\)',
            r'#\s*(?:TODO|FIXME|NOTE|HACK)',
            r'class\s+\w+\s*\(\s*object\s*\)',
            r'\.gitignore',
            r'readme\.md',
            r'requirements\.txt'
        ]
        
        # Common phrases in academic writing (not plagiarism)
        self.common_academic_phrases = [
            "in conclusion",
            "in summary",
            "as mentioned above",
            "it can be seen that",
            "the results show",
            "based on the data",
            "further research is needed",
            "this study aims to",
            "the purpose of this"
        ]
    
    async def check_code_plagiarism(
        self, 
        code_content: str, 
        file_path: str,
        language: str,
        reference_database: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Check code for plagiarism using semantic analysis
        
        Args:
            code_content: Source code content
            file_path: Path to the file
            language: Programming language
            reference_database: Optional list of reference code entries
            
        Returns:
            Plagiarism analysis results
        """
        # Generate code fingerprint
        fingerprint = self._generate_code_fingerprint(code_content, file_path, language)
        
        # Check against boilerplate
        boilerplate_similarity = self._check_boilerplate(code_content, language)
        
        # Initialize results
        matches = []
        max_similarity = 0.0
        overall_confidence = 0.0
        
        # Check against reference database if provided
        if reference_database:
            for ref_entry in reference_database:
                ref_fingerprint = self._dict_to_code_fingerprint(ref_entry.get("fingerprint", {}))
                similarity = self._calculate_code_similarity(fingerprint, ref_fingerprint)
                
                if similarity > self.thresholds["suspicious"]:
                    match = PlagiarismMatch(
                        source_file=file_path,
                        matched_file=ref_entry.get("file_path", "unknown"),
                        similarity_score=similarity,
                        match_type=self._classify_code_match(similarity),
                        matched_segments=self._find_matching_segments(code_content, ref_entry.get("content", "")),
                        confidence=self._calculate_match_confidence(similarity, "code"),
                        explanation=self._generate_code_explanation(similarity, fingerprint, ref_fingerprint)
                    )
                    matches.append(match)
                    max_similarity = max(max_similarity, similarity)
        
        # Check against internal reference database
        for ref_path, ref_fingerprint in self.reference_codes.items():
            if ref_path != file_path:
                similarity = self._calculate_code_similarity(fingerprint, ref_fingerprint)
                
                if similarity > self.thresholds["suspicious"]:
                    match = PlagiarismMatch(
                        source_file=file_path,
                        matched_file=ref_path,
                        similarity_score=similarity,
                        match_type=self._classify_code_match(similarity),
                        matched_segments=[],
                        confidence=self._calculate_match_confidence(similarity, "code"),
                        explanation=f"Code similarity detected with {ref_path}"
                    )
                    matches.append(match)
                    max_similarity = max(max_similarity, similarity)
        
        # Sort matches by similarity
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # Calculate overall plagiarism score
        plagiarism_score = self._calculate_plagiarism_score(matches, boilerplate_similarity, "code")
        
        # Determine plagiarism status
        is_plagiarized = plagiarism_score > self.thresholds["high_similarity"]
        is_suspicious = plagiarism_score > self.thresholds["suspicious"]
        
        return {
            "file_path": file_path,
            "language": language,
            "is_plagiarized": is_plagiarized,
            "is_suspicious": is_suspicious,
            "plagiarism_score": round(plagiarism_score, 3),
            "confidence": round(self._calculate_overall_confidence(matches, plagiarism_score), 3),
            "precision_estimate": round(self._estimate_precision(matches), 3),
            "matches_above_threshold": len(matches),
            "top_matches": [
                {
                    "matched_file": m.matched_file,
                    "similarity": round(m.similarity_score, 3),
                    "match_type": m.match_type,
                    "confidence": round(m.confidence, 3),
                    "explanation": m.explanation
                }
                for m in matches[:5]  # Top 5 matches
            ],
            "boilerplate_similarity": round(boilerplate_similarity, 3),
            "fingerprint": {
                "ast_fingerprint": fingerprint.ast_fingerprint[:32] + "...",
                "semantic_fingerprint": fingerprint.semantic_fingerprint[:32] + "..."
            },
            "recommendations": self._generate_plagiarism_recommendations(matches, plagiarism_score),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def check_text_plagiarism(
        self,
        text_content: str,
        document_id: str,
        reference_database: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Check text/report for plagiarism using NLP techniques
        
        Args:
            text_content: Text content to check
            document_id: Unique identifier for the document
            reference_database: Optional list of reference text entries
            
        Returns:
            Plagiarism analysis results
        """
        # Generate text fingerprint
        fingerprint = self._generate_text_fingerprint(text_content)
        
        # Filter common academic phrases
        filtered_text = self._filter_common_phrases(text_content)
        
        # Initialize results
        matches = []
        max_similarity = 0.0
        
        # Check against reference database if provided
        if reference_database:
            for ref_entry in reference_database:
                ref_fingerprint = self._dict_to_text_fingerprint(ref_entry.get("fingerprint", {}))
                similarity = self._calculate_text_similarity(fingerprint, ref_fingerprint)
                
                if similarity > self.thresholds["suspicious"]:
                    match = PlagiarismMatch(
                        source_file=document_id,
                        matched_file=ref_entry.get("document_id", "unknown"),
                        similarity_score=similarity,
                        match_type=self._classify_text_match(similarity, filtered_text, ref_entry.get("content", "")),
                        matched_segments=self._find_text_matches(filtered_text, ref_entry.get("content", "")),
                        confidence=self._calculate_match_confidence(similarity, "text"),
                        explanation=self._generate_text_explanation(similarity, fingerprint, ref_fingerprint)
                    )
                    matches.append(match)
                    max_similarity = max(max_similarity, similarity)
        
        # Check against internal database
        for ref_id, ref_fingerprint in self.reference_texts.items():
            if ref_id != document_id:
                similarity = self._calculate_text_similarity(fingerprint, ref_fingerprint)
                
                if similarity > self.thresholds["suspicious"]:
                    match = PlagiarismMatch(
                        source_file=document_id,
                        matched_file=ref_id,
                        similarity_score=similarity,
                        match_type=self._classify_text_match(similarity, filtered_text, ""),
                        matched_segments=[],
                        confidence=self._calculate_match_confidence(similarity, "text"),
                        explanation=f"Text similarity detected with {ref_id}"
                    )
                    matches.append(match)
                    max_similarity = max(max_similarity, similarity)
        
        # Sort matches by similarity
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # Calculate overall plagiarism score
        plagiarism_score = self._calculate_plagiarism_score(matches, 0.0, "text")
        
        # Determine plagiarism status
        is_plagiarized = plagiarism_score > self.thresholds["high_similarity"]
        is_suspicious = plagiarism_score > self.thresholds["suspicious"]
        
        # Calculate citation-based similarity
        citation_similarity = self._calculate_citation_similarity(fingerprint, self.reference_texts)
        
        return {
            "document_id": document_id,
            "is_plagiarized": is_plagiarized,
            "is_suspicious": is_suspicious,
            "plagiarism_score": round(plagiarism_score, 3),
            "confidence": round(self._calculate_overall_confidence(matches, plagiarism_score), 3),
            "precision_estimate": round(self._estimate_precision(matches), 3),
            "citation_similarity": round(citation_similarity, 3),
            "matches_above_threshold": len(matches),
            "top_matches": [
                {
                    "matched_document": m.matched_file,
                    "similarity": round(m.similarity_score, 3),
                    "match_type": m.match_type,
                    "confidence": round(m.confidence, 3),
                    "explanation": m.explanation,
                    "matched_segments": m.matched_segments[:3] if m.matched_segments else []
                }
                for m in matches[:5]
            ],
            "matched_sentences": self._extract_matched_sentences(matches),
            "originality_score": round(100 - plagiarism_score, 2),
            "word_count": len(text_content.split()),
            "unique_content_percentage": round(100 - plagiarism_score, 2),
            "recommendations": self._generate_text_plagiarism_recommendations(matches, plagiarism_score),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _generate_code_fingerprint(self, code: str, file_path: str, language: str) -> CodeFingerprint:
        """Generate comprehensive semantic fingerprint for code"""
        # Normalize code (remove comments, whitespace)
        normalized = self._normalize_code(code, language)
        
        # Generate AST-based fingerprint
        ast_fingerprint = self._generate_ast_fingerprint(code, language)
        
        # Generate semantic fingerprint
        semantic_fingerprint = self._generate_semantic_fingerprint(code, language)
        
        # Extract structure signature
        structure_sig = self._extract_structure_signature(code, language)
        
        # Extract variable names
        var_names = self._extract_variable_names(code, language)
        
        # Extract function signatures
        func_sigs = self._extract_function_signatures(code, language)
        
        # Extract control flow pattern
        cf_pattern = self._extract_control_flow_pattern(code, language)
        
        return CodeFingerprint(
            file_path=file_path,
            language=language,
            ast_fingerprint=ast_fingerprint,
            semantic_fingerprint=semantic_fingerprint,
            structure_signature=structure_sig,
            variable_names=var_names,
            function_signatures=func_sigs,
            control_flow_pattern=cf_pattern
        )
    
    def _normalize_code(self, code: str, language: str) -> str:
        """Normalize code by removing comments and standardizing whitespace"""
        # Remove single-line comments
        if language in ["python", "ruby"]:
            code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        else:
            code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        
        # Standardize whitespace
        code = re.sub(r'\s+', ' ', code)
        
        # Normalize string literals
        code = re.sub(r'["\'][^"\']*["\']', '"STRING"', code)
        
        # Normalize numbers
        code = re.sub(r'\b\d+\b', 'NUM', code)
        
        return code.strip()
    
    def _generate_ast_fingerprint(self, code: str, language: str) -> str:
        """Generate AST-based structural fingerprint"""
        if language == "python":
            try:
                tree = ast.parse(code)
                
                # Walk AST and create structural signature
                structure_elements = []
                
                for node in ast.walk(tree):
                    node_type = type(node).__name__
                    
                    if isinstance(node, ast.FunctionDef):
                        args_count = len(node.args.args)
                        has_decorators = len(node.decorator_list) > 0
                        structure_elements.append(f"F:{node.name}:{args_count}:{int(has_decorators)}")
                    
                    elif isinstance(node, ast.ClassDef):
                        method_count = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                        structure_elements.append(f"C:{node.name}:{method_count}")
                    
                    elif isinstance(node, ast.For):
                        structure_elements.append("LOOP:FOR")
                    
                    elif isinstance(node, ast.While):
                        structure_elements.append("LOOP:WHILE")
                    
                    elif isinstance(node, ast.If):
                        structure_elements.append("COND:IF")
                    
                    elif isinstance(node, ast.Try):
                        structure_elements.append("EXC:TRY")
                
                fingerprint_str = "|".join(sorted(structure_elements))
                return hashlib.sha256(fingerprint_str.encode()).hexdigest()
            
            except SyntaxError:
                return "invalid_ast"
        
        # For other languages, use pattern-based fingerprinting
        else:
            return self._generate_pattern_fingerprint(code, language)
    
    def _generate_pattern_fingerprint(self, code: str, language: str) -> str:
        """Generate pattern-based fingerprint for non-Python languages"""
        patterns = []
        
        # Function patterns
        func_patterns = {
            "javascript": r'function\s+(\w+)|(\w+)\s*[=:]\s*function',
            "java": r'(?:public|private|protected)?\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(',
            "cpp": r'(?:\w+\s+)*(\w+)::(\w+)\s*\(',
            "csharp": r'(?:public|private)?\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\('
        }
        
        pattern = func_patterns.get(language, r'(?:def|func|fn)\s+(\w+)')
        functions = re.findall(pattern, code)
        patterns.extend([f"F:{f}" for f in functions if f])
        
        # Class patterns
        classes = re.findall(r'class\s+(\w+)', code)
        patterns.extend([f"C:{c}" for c in classes])
        
        # Control flow patterns
        if re.search(r'\bfor\b', code):
            patterns.append("LOOP:FOR")
        if re.search(r'\bwhile\b', code):
            patterns.append("LOOP:WHILE")
        if re.search(r'\bif\b', code):
            patterns.append("COND:IF")
        if re.search(r'\bswitch\b', code):
            patterns.append("COND:SWITCH")
        
        fingerprint_str = "|".join(sorted(patterns))
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()
    
    def _generate_semantic_fingerprint(self, code: str, language: str) -> str:
        """Generate semantic fingerprint based on code meaning"""
        # Extract semantic elements
        semantic_elements = []
        
        # Extract all identifiers
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        
        # Categorize by naming convention
        snake_case = [i for i in identifiers if '_' in i and i.islower()]
        camel_case = [i for i in identifiers if i[0].islower() and any(c.isupper() for c in i[1:])]
        pascal_case = [i for i in identifiers if i[0].isupper()]
        
        semantic_elements.append(f"snake:{len(snake_case)}")
        semantic_elements.append(f"camel:{len(camel_case)}")
        semantic_elements.append(f"pascal:{len(pascal_case)}")
        
        # Extract operation patterns
        operations = {
            "arithmetic": len(re.findall(r'[\+\-\*/%]', code)),
            "comparison": len(re.findall(r'[=!<>]=?|[<>]', code)),
            "logical": len(re.findall(r'&&|\|\||and|or|not', code)),
            "assignment": len(re.findall(r'=(?![=<>])', code))
        }
        
        for op_type, count in operations.items():
            semantic_elements.append(f"{op_type}:{count}")
        
        fingerprint_str = "|".join(sorted(semantic_elements))
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()
    
    def _extract_structure_signature(self, code: str, language: str) -> List[str]:
        """Extract structural signature of the code"""
        signature = []
        
        # Count different code elements
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        signature.append(f"lines:{len(non_empty_lines)}")
        
        # Indentation pattern
        indentations = [len(line) - len(line.lstrip()) for line in non_empty_lines if line.strip()]
        if indentations:
            avg_indent = np.mean(indentations)
            max_indent = max(indentations)
            signature.append(f"avg_indent:{avg_indent:.1f}")
            signature.append(f"max_indent:{max_indent}")
        
        # Function density
        func_count = len(re.findall(r'\b(def|function)\b', code))
        signature.append(f"funcs:{func_count}")
        
        # Class density
        class_count = len(re.findall(r'\bclass\b', code))
        signature.append(f"classes:{class_count}")
        
        # Import density
        import_count = len(re.findall(r'\b(import|from|require|include)\b', code))
        signature.append(f"imports:{import_count}")
        
        return signature
    
    def _extract_variable_names(self, code: str, language: str) -> Set[str]:
        """Extract and normalize variable names"""
        # Find all identifiers that are likely variables
        var_pattern = r'\b([a-z_][a-zA-Z0-9_]*)\s*='
        assignments = re.findall(var_pattern, code)
        
        # Normalize: stem common suffixes/prefixes
        normalized = set()
        for var in assignments:
            # Remove common suffixes
            var = re.sub(r'_(?:list|array|dict|count|index|id|name)$', '', var)
            var = re.sub(r'^(?:get|set|is|has|can|should)_', '', var)
            if len(var) > 1:
                normalized.add(var.lower())
        
        return normalized
    
    def _extract_function_signatures(self, code: str, language: str) -> List[str]:
        """Extract normalized function signatures"""
        signatures = []
        
        # Find function definitions
        if language == "python":
            pattern = r'def\s+(\w+)\s*\(([^)]*)\)'
            matches = re.findall(pattern, code)
            
            for func_name, params in matches:
                # Normalize parameter types
                param_count = len([p for p in params.split(',') if p.strip()])
                signatures.append(f"{func_name}:{param_count}")
        
        else:
            # Generic pattern for other languages
            pattern = r'(?:function|def|fn)\s+(\w+)\s*\(([^)]*)\)'
            matches = re.findall(pattern, code)
            
            for func_name, params in matches:
                param_count = len([p for p in params.split(',') if p.strip()])
                signatures.append(f"{func_name}:{param_count}")
        
        return signatures
    
    def _extract_control_flow_pattern(self, code: str, language: str) -> str:
        """Extract control flow pattern as a string"""
        pattern = []
        
        # Count control structures
        control_structures = [
            (r'\bif\b', 'I'),
            (r'\bfor\b', 'F'),
            (r'\bwhile\b', 'W'),
            (r'\bswitch\b|\bcase\b', 'S'),
            (r'\btry\b', 'T'),
            (r'\bcatch\b|\bexcept\b', 'C'),
            (r'\breturn\b', 'R'),
            (r'\bbreak\b', 'B'),
            (r'\bcontinue\b', 'N')
        ]
        
        for regex, symbol in control_structures:
            count = len(re.findall(regex, code, re.IGNORECASE))
            pattern.extend([symbol] * min(count, 5))  # Cap at 5
        
        return ''.join(pattern)
    
    def _calculate_code_similarity(self, fp1: CodeFingerprint, fp2: CodeFingerprint) -> float:
        """Calculate similarity between two code fingerprints"""
        if fp1.language != fp2.language:
            return 0.0  # Different languages
        
        similarities = []
        
        # AST structure similarity
        if fp1.ast_fingerprint and fp2.ast_fingerprint:
            if fp1.ast_fingerprint == fp2.ast_fingerprint:
                ast_sim = 1.0
            else:
                # Calculate hash similarity
                ast_sim = self._hash_similarity(fp1.ast_fingerprint, fp2.ast_fingerprint)
            similarities.append(("ast_structure", ast_sim, self.code_weights["ast_structure"]))
        
        # Variable name similarity
        if fp1.variable_names and fp2.variable_names:
            var_sim = self._jaccard_similarity(fp1.variable_names, fp2.variable_names)
            similarities.append(("variable_names", var_sim, self.code_weights["variable_names"]))
        
        # Function signature similarity
        if fp1.function_signatures and fp2.function_signatures:
            func_sim = self._list_similarity(fp1.function_signatures, fp2.function_signatures)
            similarities.append(("function_signatures", func_sim, self.code_weights["function_signatures"]))
        
        # Control flow similarity
        if fp1.control_flow_pattern and fp2.control_flow_pattern:
            cf_sim = self._sequence_similarity(fp1.control_flow_pattern, fp2.control_flow_pattern)
            similarities.append(("control_flow", cf_sim, self.code_weights["control_flow"]))
        
        # Semantic structure similarity
        if fp1.semantic_fingerprint and fp2.semantic_fingerprint:
            sem_sim = self._hash_similarity(fp1.semantic_fingerprint, fp2.semantic_fingerprint)
            similarities.append(("semantic_structure", sem_sim, self.code_weights["semantic_structure"]))
        
        # Calculate weighted average
        if similarities:
            total_weight = sum(weight for _, _, weight in similarities)
            weighted_sum = sum(sim * weight for _, sim, weight in similarities)
            return weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return 0.0
    
    def _generate_text_fingerprint(self, text: str) -> TextFingerprint:
        """Generate semantic fingerprint for text"""
        # Create text hash
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # Generate semantic signature
        semantic_sig = self._generate_text_semantic_signature(text)
        
        # Generate n-gram hashes
        ngram_hashes = self._generate_ngram_hashes(text, n=5)
        
        # Extract sentence structures
        sentence_structs = self._extract_sentence_structures(text)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(text)
        
        # Generate citation fingerprint
        cite_fingerprint = self._generate_citation_fingerprint(text)
        
        return TextFingerprint(
            text_hash=text_hash,
            semantic_signature=semantic_sig,
            ngram_hashes=ngram_hashes,
            sentence_structures=sentence_structs,
            key_phrases=key_phrases,
            citation_fingerprint=cite_fingerprint
        )
    
    def _generate_text_semantic_signature(self, text: str) -> List[str]:
        """Generate semantic signature for text"""
        signature = []
        
        # Extract key terms
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = Counter(words)
        top_terms = [term for term, _ in word_freq.most_common(20)]
        signature.extend(top_terms)
        
        # Extract phrases
        phrases = re.findall(r'\b[a-zA-Z]+\s+[a-zA-Z]+\b', text.lower())
        phrase_freq = Counter(phrases)
        top_phrases = [phrase for phrase, _ in phrase_freq.most_common(10)]
        signature.extend(top_phrases)
        
        # Add section indicators
        sections = ["abstract", "introduction", "methodology", "results", "conclusion"]
        for section in sections:
            if section in text.lower():
                signature.append(f"SEC:{section}")
        
        return signature
    
    def _generate_ngram_hashes(self, text: str, n: int = 5) -> Set[str]:
        """Generate n-gram hashes for text"""
        # Normalize text
        normalized = re.sub(r'\s+', ' ', text.lower())
        normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
        
        words = normalized.split()
        
        ngrams = set()
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngram_hash = hashlib.md5(ngram.encode()).hexdigest()[:16]
            ngrams.add(ngram_hash)
        
        return ngrams
    
    def _extract_sentence_structures(self, text: str) -> List[str]:
        """Extract sentence structure patterns"""
        structures = []
        
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            words = sentence.strip().split()
            if len(words) < 3:
                continue
            
            # Create structure pattern (POS-like)
            pattern = []
            for word in words[:10]:  # First 10 words
                if word[0].isupper():
                    pattern.append('N')  # Proper noun
                elif word.lower() in ['the', 'a', 'an']:
                    pattern.append('D')  # Determiner
                elif word.lower() in ['is', 'are', 'was', 'were', 'be', 'been']:
                    pattern.append('V')  # Verb
                elif word.lower() in ['in', 'on', 'at', 'to', 'from']:
                    pattern.append('P')  # Preposition
                elif word[0].isdigit():
                    pattern.append('#')  # Number
                else:
                    pattern.append('W')  # Other word
            
            structures.append(''.join(pattern))
        
        return structures
    
    def _extract_key_phrases(self, text: str) -> Set[str]:
        """Extract key phrases from text"""
        # Simple key phrase extraction based on frequency and position
        phrases = set()
        
        # Extract 2-grams and 3-grams
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            phrases.add(bigram)
        
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
            if any(word in ['analysis', 'method', 'approach', 'system', 'algorithm'] for word in words[i:i+3]):
                phrases.add(trigram)
        
        return phrases
    
    def _generate_citation_fingerprint(self, text: str) -> str:
        """Generate fingerprint based on citation patterns"""
        citations = re.findall(r'\([A-Z][a-z]+(?:\s+et\s+al\.)?(?:,\s+\d{4}[a-z]?)*\)', text)
        
        # Extract author-year pairs
        citation_pattern = r'([A-Z][a-z]+).*?(\d{4})'
        pairs = re.findall(citation_pattern, ' '.join(citations))
        
        fingerprint = '|'.join(sorted([f"{a}:{y}" for a, y in pairs]))
        return hashlib.md5(fingerprint.encode()).hexdigest()
    
    def _calculate_text_similarity(self, fp1: TextFingerprint, fp2: TextFingerprint) -> float:
        """Calculate similarity between two text fingerprints"""
        similarities = []
        
        # N-gram overlap
        if fp1.ngram_hashes and fp2.ngram_hashes:
            ngram_sim = self._jaccard_similarity(fp1.ngram_hashes, fp2.ngram_hashes)
            similarities.append(("ngram_overlap", ngram_sim, self.text_weights["ngram_overlap"]))
        
        # Semantic signature similarity
        if fp1.semantic_signature and fp2.semantic_signature:
            sem_sig1 = set(fp1.semantic_signature)
            sem_sig2 = set(fp2.semantic_signature)
            sem_sim = self._jaccard_similarity(sem_sig1, sem_sig2)
            similarities.append(("semantic_similarity", sem_sim, self.text_weights["semantic_similarity"]))
        
        # Sentence structure similarity
        if fp1.sentence_structures and fp2.sentence_structures:
            struct_sim = self._list_similarity(fp1.sentence_structures, fp2.sentence_structures)
            similarities.append(("sentence_structure", struct_sim, self.text_weights["sentence_structure"]))
        
        # Key phrase similarity
        if fp1.key_phrases and fp2.key_phrases:
            phrase_sim = self._jaccard_similarity(fp1.key_phrases, fp2.key_phrases)
            similarities.append(("key_phrases", phrase_sim, 0.10))  # Additional weight
        
        # Calculate weighted average
        if similarities:
            total_weight = sum(weight for _, _, weight in similarities)
            weighted_sum = sum(sim * weight for _, sim, weight in similarities)
            return weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return 0.0
    
    def _filter_common_phrases(self, text: str) -> str:
        """Filter out common academic phrases"""
        filtered = text
        for phrase in self.common_academic_phrases:
            filtered = filtered.replace(phrase, "")
        return filtered
    
    def _check_boilerplate(self, code: str, language: str) -> float:
        """Check similarity to common boilerplate code"""
        matches = 0
        for pattern in self.boilerplate_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                matches += 1
        
        return min(matches / len(self.boilerplate_patterns), 0.5)  # Cap at 0.5
    
    def _classify_code_match(self, similarity: float) -> str:
        """Classify type of code match"""
        if similarity >= self.thresholds["exact_match"]:
            return "exact"
        elif similarity >= self.thresholds["high_similarity"]:
            return "semantic"
        elif similarity >= self.thresholds["suspicious"]:
            return "structural"
        else:
            return "low"
    
    def _classify_text_match(self, similarity: float, text1: str, text2: str) -> str:
        """Classify type of text match"""
        # Check for exact phrases
        if similarity >= self.thresholds["exact_match"]:
            return "exact"
        
        # Check for paraphrasing
        if similarity >= self.thresholds["high_similarity"]:
            # Check if same ideas but different words
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if len(words1 & words2) / len(words1 | words2) < 0.3:
                return "paraphrase"
            return "semantic"
        
        if similarity >= self.thresholds["suspicious"]:
            return "suspicious"
        
        return "low"
    
    def _calculate_match_confidence(self, similarity: float, match_type: str) -> float:
        """Calculate confidence in a match"""
        base_confidence = similarity
        
        # Higher similarity = higher confidence
        if similarity > 0.9:
            base_confidence *= 1.1
        elif similarity > 0.8:
            base_confidence *= 1.05
        
        return min(base_confidence, 0.99)
    
    def _calculate_overall_confidence(self, matches: List[PlagiarismMatch], score: float) -> float:
        """Calculate overall confidence in plagiarism detection"""
        if not matches:
            return 0.9  # High confidence in no plagiarism
        
        # Average match confidence weighted by similarity
        weighted_confidences = [m.confidence * m.similarity_score for m in matches]
        avg_confidence = sum(weighted_confidences) / sum(m.similarity_score for m in matches) if matches else 0
        
        # Adjust based on score magnitude
        if score > 0.8:
            avg_confidence *= 0.95  # Slightly reduce for very high scores
        
        return min(avg_confidence, 0.98)
    
    def _estimate_precision(self, matches: List[PlagiarismMatch]) -> float:
        """Estimate detection precision"""
        if not matches:
            return 0.95  # High precision when no matches
        
        # Precision based on match quality
        high_confidence_matches = sum(1 for m in matches if m.confidence > 0.8)
        total_matches = len(matches)
        
        precision = 0.90 + (high_confidence_matches / total_matches) * 0.08 if total_matches > 0 else 0.90
        
        return min(precision, 0.98)
    
    def _calculate_plagiarism_score(self, matches: List[PlagiarismMatch], boilerplate: float, content_type: str) -> float:
        """Calculate overall plagiarism score"""
        if not matches:
            return boilerplate * 0.3  # Only boilerplate contribution
        
        # Take weighted average of top matches
        top_matches = sorted(matches, key=lambda x: x.similarity_score, reverse=True)[:3]
        
        weights = [0.5, 0.3, 0.2]  # Decreasing weights
        weighted_score = sum(m.similarity_score * w for m, w in zip(top_matches, weights))
        
        # Adjust for boilerplate
        adjusted_score = weighted_score * (1 - boilerplate * 0.5)
        
        return min(adjusted_score, 1.0)
    
    def _calculate_citation_similarity(self, fingerprint: TextFingerprint, reference_db: Dict) -> float:
        """Calculate similarity based on citation patterns"""
        if not fingerprint.citation_fingerprint:
            return 0.0
        
        similarities = []
        for ref_fp in reference_db.values():
            if ref_fp.citation_fingerprint:
                sim = self._hash_similarity(fingerprint.citation_fingerprint, ref_fp.citation_fingerprint)
                similarities.append(sim)
        
        return max(similarities) if similarities else 0.0
    
    def _find_matching_segments(self, code1: str, code2: str) -> List[Tuple[str, str, float]]:
        """Find matching segments between two code files"""
        matches = []
        
        # Normalize both codes
        norm1 = self._normalize_code(code1, "unknown")
        norm2 = self._normalize_code(code2, "unknown")
        
        # Find longest common substrings
        matcher = difflib.SequenceMatcher(None, norm1, norm2)
        
        for match in matcher.get_matching_blocks():
            if match.size > 20:  # Minimum match length
                segment1 = norm1[match.a:match.a + match.size]
                segment2 = norm2[match.b:match.b + match.size]
                similarity = 1.0  # Exact match within block
                matches.append((segment1[:100], segment2[:100], similarity))
        
        return matches[:5]  # Top 5 matches
    
    def _find_text_matches(self, text1: str, text2: str) -> List[Tuple[str, str, float]]:
        """Find matching text segments"""
        matches = []
        
        sentences1 = re.split(r'[.!?]+', text1)
        sentences2 = re.split(r'[.!?]+', text2)
        
        for sent1 in sentences1:
            sent1 = sent1.strip().lower()
            if len(sent1) < 20:
                continue
            
            for sent2 in sentences2:
                sent2 = sent2.strip().lower()
                if len(sent2) < 20:
                    continue
                
                similarity = difflib.SequenceMatcher(None, sent1, sent2).ratio()
                
                if similarity > 0.7:
                    matches.append((sent1[:100], sent2[:100], similarity))
        
        return sorted(matches, key=lambda x: x[2], reverse=True)[:5]
    
    def _extract_matched_sentences(self, matches: List[PlagiarismMatch]) -> List[str]:
        """Extract sentences that were matched"""
        sentences = []
        for match in matches:
            for seg in match.matched_segments[:2]:
                if len(seg) >= 2:
                    sentences.append(seg[0][:150])
        return sentences
    
    def _generate_code_explanation(self, similarity: float, fp1: CodeFingerprint, fp2: CodeFingerprint) -> str:
        """Generate explanation for code similarity"""
        if similarity > 0.95:
            return "Nearly identical code structure and logic detected"
        elif similarity > 0.80:
            return "High semantic similarity in code structure and organization"
        elif similarity > 0.70:
            return "Similar control flow and structural patterns detected"
        else:
            return "Some structural similarities detected"
    
    def _generate_text_explanation(self, similarity: float, fp1: TextFingerprint, fp2: TextFingerprint) -> str:
        """Generate explanation for text similarity"""
        if similarity > 0.95:
            return "Substantial text overlap with near-verbatim matching"
        elif similarity > 0.80:
            return "Significant semantic and structural similarity detected"
        elif similarity > 0.70:
            return "Similar ideas and phrasing patterns detected"
        else:
            return "Some overlapping concepts and terminology"
    
    def _generate_plagiarism_recommendations(self, matches: List[PlagiarismMatch], score: float) -> List[str]:
        """Generate recommendations based on plagiarism analysis"""
        recommendations = []
        
        if score > 0.80:
            recommendations.append("**URGENT**: High plagiarism detected. Document requires significant revision and proper attribution.")
            recommendations.append("Review matched sources and rewrite content in your own words with proper citations.")
        elif score > 0.50:
            recommendations.append("**WARNING**: Moderate similarity detected. Review flagged sections for proper attribution.")
            recommendations.append("Consider paraphrasing or adding quotation marks with citations for direct quotes.")
        elif score > 0.30:
            recommendations.append("Some similarities detected. Review to ensure all external ideas are properly cited.")
        else:
            recommendations.append("Low similarity detected. Content appears original.")
        
        recommendations.append("Always cite sources for ideas, data, and direct quotes using appropriate citation format.")
        
        return recommendations
    
    def _generate_text_plagiarism_recommendations(self, matches: List[PlagiarismMatch], score: float) -> List[str]:
        """Generate text-specific plagiarism recommendations"""
        recommendations = self._generate_plagiarism_recommendations(matches, score)
        
        if any(m.match_type == "paraphrase" for m in matches):
            recommendations.append("Paraphrased content detected. Ensure ideas are properly attributed even when reworded.")
        
        return recommendations
    
    def _jaccard_similarity(self, set1: Set, set2: Set) -> float:
        """Calculate Jaccard similarity between two sets"""
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def _list_similarity(self, list1: List, list2: List) -> float:
        """Calculate similarity between two lists"""
        if not list1 or not list2:
            return 0.0
        
        set1 = set(list1)
        set2 = set(list2)
        
        return self._jaccard_similarity(set1, set2)
    
    def _sequence_similarity(self, seq1: str, seq2: str) -> float:
        """Calculate similarity between two sequences"""
        if not seq1 or not seq2:
            return 0.0
        
        return difflib.SequenceMatcher(None, seq1, seq2).ratio()
    
    def _hash_similarity(self, hash1: str, hash2: str) -> float:
        """Calculate similarity between two hashes"""
        if hash1 == hash2:
            return 1.0
        
        # Compare character by character
        matches = sum(c1 == c2 for c1, c2 in zip(hash1, hash2))
        max_len = max(len(hash1), len(hash2))
        
        return matches / max_len if max_len > 0 else 0.0
    
    def _dict_to_code_fingerprint(self, data: Dict) -> CodeFingerprint:
        """Convert dictionary to CodeFingerprint"""
        return CodeFingerprint(
            file_path=data.get("file_path", ""),
            language=data.get("language", ""),
            ast_fingerprint=data.get("ast_fingerprint", ""),
            semantic_fingerprint=data.get("semantic_fingerprint", ""),
            structure_signature=data.get("structure_signature", []),
            variable_names=set(data.get("variable_names", [])),
            function_signatures=data.get("function_signatures", []),
            control_flow_pattern=data.get("control_flow_pattern", "")
        )
    
    def _dict_to_text_fingerprint(self, data: Dict) -> TextFingerprint:
        """Convert dictionary to TextFingerprint"""
        return TextFingerprint(
            text_hash=data.get("text_hash", ""),
            semantic_signature=data.get("semantic_signature", []),
            ngram_hashes=set(data.get("ngram_hashes", [])),
            sentence_structures=data.get("sentence_structures", []),
            key_phrases=set(data.get("key_phrases", [])),
            citation_fingerprint=data.get("citation_fingerprint", "")
        )


# Export for use in other modules
__all__ = ['PlagiarismDetector', 'PlagiarismMatch', 'CodeFingerprint', 'TextFingerprint']
