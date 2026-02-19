import PyPDF2
import io
import os
import tempfile
from typing import Dict, List, Any, Optional
import re
from pathlib import Path

class PDFProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    async def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process PDF report and extract analysis data"""
        try:
            text_content = await self._extract_text(pdf_path)
            if not text_content:
                return {
                    "error": "Could not extract text from PDF",
                    "text": "",
                    "page_count": 0,
                    "word_count": 0,
                    "sections": []
                }
            
            page_count = await self._get_page_count(pdf_path)
            word_count = len(text_content.split())
            structure = await self._analyze_structure(text_content)
            
            analysis = {
                "text": text_content,
                "text_content": text_content,
                "page_count": page_count,
                "word_count": word_count,
                "sections": [s["name"] for s in structure.get("sections", [])],
                "structure_analysis": structure,
                "content_analysis": await self._analyze_content(text_content),
                "quality_metrics": await self._calculate_quality_metrics(text_content)
            }
            
            return analysis
            
        except Exception as e:
            return {
                "error": f"Failed to process PDF: {str(e)}",
                "text": "",
                "page_count": 0,
                "word_count": 0,
                "sections": []
            }
    
    async def extract_text(self, pdf_path: str) -> Dict[str, Any]:
        """Public method to extract text from PDF and return with metadata"""
        try:
            text = await self._extract_text(pdf_path)
            return {
                "text": text,
                "success": True,
                "word_count": len(text.split()) if text else 0
            }
        except Exception as e:
            return {
                "text": "",
                "success": False,
                "error": str(e)
            }
    
    async def _extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
        
        return text
    
    async def _get_page_count(self, pdf_path: str) -> int:
        """Get number of pages in PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except:
            return 0
    
    async def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze document structure"""
        structure = {
            "has_title": False,
            "has_abstract": False,
            "has_introduction": False,
            "has_conclusion": False,
            "has_references": False,
            "headings": [],
            "sections": []
        }
        
        # Check for common sections
        text_lower = text.lower()
        
        structure["has_title"] = bool(re.search(r'^[A-Z\s]{10,}$', text, re.MULTILINE))
        structure["has_abstract"] = "abstract" in text_lower
        structure["has_introduction"] = any(term in text_lower for term in ["introduction", "overview", "background"])
        structure["has_conclusion"] = any(term in text_lower for term in ["conclusion", "summary", "results"])
        structure["has_references"] = any(term in text_lower for term in ["references", "bibliography", "citations"])
        
        # Extract headings (simple pattern matching)
        heading_patterns = [
            r'^[A-Z][A-Za-z\s]{5,}$',  # All caps headings
            r'^\d+\.\s+[A-Z][A-Za-z\s]+$',  # Numbered headings
            r'^[A-Z][a-z]+[A-Z][A-Za-z\s]+$',  # CamelCase headings
        ]
        
        for pattern in heading_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            structure["headings"].extend(matches)
        
        # Identify sections
        section_keywords = [
            "introduction", "background", "methodology", "approach", "implementation",
            "results", "discussion", "conclusion", "summary", "references", "appendix"
        ]
        
        for keyword in section_keywords:
            if keyword in text_lower:
                # Find section start
                pattern = rf"(?i){keyword}[:\s]*[\n]*"
                match = re.search(pattern, text)
                if match:
                    structure["sections"].append({
                        "name": keyword.title(),
                        "position": match.start()
                    })
        
        return structure
    
    async def _analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze content quality and relevance"""
        content_analysis = {
            "technical_terms": [],
            "methodology_mentions": [],
            "code_references": 0,
            "diagram_references": 0,
            "citation_count": 0,
            "readability_score": 0,
            "technical_depth": 0
        }
        
        # Technical terms commonly found in project reports
        technical_terms = [
            "algorithm", "implementation", "architecture", "design", "framework",
            "database", "api", "interface", "module", "function", "class",
            "method", "variable", "library", "dependency", "testing", "debugging",
            "optimization", "performance", "security", "scalability", "usability"
        ]
        
        text_lower = text.lower()
        
        # Count technical terms
        for term in technical_terms:
            count = text_lower.count(term)
            if count > 0:
                content_analysis["technical_terms"].append({"term": term, "count": count})
        
        # Methodology mentions
        methodology_terms = [
            "waterfall", "agile", "scrum", "kanban", "prototype", "mvp",
            "iterative", "incremental", "spiral", "devops"
        ]
        
        for term in methodology_terms:
            if term in text_lower:
                content_analysis["methodology_mentions"].append(term)
        
        # Code references
        code_patterns = [
            r'```[\s\S]*?```',  # Code blocks
            r'`[^`]+`',  # Inline code
            r'\b(main|function|class|def|import|include)\b',  # Code keywords
        ]
        
        for pattern in code_patterns:
            content_analysis["code_references"] += len(re.findall(pattern, text, re.IGNORECASE))
        
        # Diagram references
        diagram_patterns = [
            r'figure\s+\d+',
            r'diagram\s+\d+',
            r'chart\s+\d+',
            r'graph\s+\d+',
            r'table\s+\d+'
        ]
        
        for pattern in diagram_patterns:
            content_analysis["diagram_references"] += len(re.findall(pattern, text, re.IGNORECASE))
        
        # Citation count (simple pattern)
        citation_patterns = [
            r'\[\d+\]',  # [1], [2], etc.
            r'\([^)]*\d{4}[^)]*\)',  # (Smith, 2020)
            r'\w+\s+et\s+al\.\s*\(\d{4}\)',  # Smith et al. (2020)
        ]
        
        for pattern in citation_patterns:
            content_analysis["citation_count"] += len(re.findall(pattern, text))
        
        # Simple readability score (based on sentence length and word complexity)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            content_analysis["readability_score"] = max(0, 100 - avg_sentence_length * 2)
        
        # Technical depth (based on technical terms and code references)
        tech_term_score = len(content_analysis["technical_terms"]) * 5
        code_ref_score = content_analysis["code_references"] * 3
        methodology_score = len(content_analysis["methodology_mentions"]) * 10
        
        content_analysis["technical_depth"] = min(tech_term_score + code_ref_score + methodology_score, 100)
        
        return content_analysis
    
    async def _calculate_quality_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate overall quality metrics for the report"""
        metrics = {
            "structure_score": 0,
            "content_quality_score": 0,
            "completeness_score": 0,
            "overall_score": 0,
            "recommendations": []
        }
        
        # Structure score (based on document structure)
        structure = await self._analyze_structure(text)
        structure_elements = 0
        
        if structure["has_title"]:
            structure_elements += 1
        if structure["has_abstract"]:
            structure_elements += 1
        if structure["has_introduction"]:
            structure_elements += 1
        if structure["has_conclusion"]:
            structure_elements += 1
        if structure["has_references"]:
            structure_elements += 1
        
        metrics["structure_score"] = (structure_elements / 5) * 100
        
        # Content quality score
        content = await self._analyze_content(text)
        
        # Factors for content quality
        word_count_factor = min(len(text.split()) / 1000, 1) * 20  # Max 20 points for word count
        technical_depth_factor = content["technical_depth"] * 0.3  # Max 30 points
        readability_factor = content["readability_score"] * 0.2  # Max 20 points
        citation_factor = min(content["citation_count"] * 2, 30)  # Max 30 points
        
        metrics["content_quality_score"] = word_count_factor + technical_depth_factor + readability_factor + citation_factor
        
        # Completeness score
        completeness_factors = []
        
        if len(text.split()) >= 500:
            completeness_factors.append(20)  # Minimum length
        else:
            metrics["recommendations"].append("Report should be at least 500 words")
        
        if content["technical_depth"] >= 30:
            completeness_factors.append(20)  # Technical depth
        else:
            metrics["recommendations"].append("Include more technical details and terminology")
        
        if content["code_references"] >= 3:
            completeness_factors.append(20)  # Code examples
        else:
            metrics["recommendations"].append("Include code examples or snippets")
        
        if content["diagram_references"] >= 2:
            completeness_factors.append(20)  # Visual elements
        else:
            metrics["recommendations"].append("Include diagrams or charts to illustrate concepts")
        
        if content["citation_count"] >= 3:
            completeness_factors.append(20)  # References
        else:
            metrics["recommendations"].append("Include proper citations and references")
        
        metrics["completeness_score"] = sum(completeness_factors)
        
        # Overall score
        metrics["overall_score"] = (
            metrics["structure_score"] * 0.3 +
            metrics["content_quality_score"] * 0.4 +
            metrics["completeness_score"] * 0.3
        )
        
        return metrics
