from typing import Dict, List, Any, Optional
import json
import math

class ScoringEngine:
    def __init__(self):
        self.default_weights = {
            "code_quality": 0.3,
            "functionality": 0.4,
            "documentation": 0.2,
            "innovation": 0.1
        }
    
    async def calculate_score(
        self,
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None,
        criteria: Optional[Dict[str, Any]] = None,
        code_weight: float = 0.7,
        report_weight: float = 0.3
    ) -> Dict[str, Any]:
        """Calculate overall project score"""
        
        # Use provided criteria or defaults
        weights = criteria.get("weights", self.default_weights) if criteria else self.default_weights
        
        # Calculate code score
        code_score = 0
        code_breakdown = {}
        
        if code_analysis:
            code_score, code_breakdown = await self._calculate_code_score(code_analysis, weights)
        
        # Calculate report score
        report_score = 0
        report_breakdown = {}
        
        if report_analysis:
            report_score, report_breakdown = await self._calculate_report_score(report_analysis)
        
        # Calculate weighted overall score
        overall_score = (code_score * code_weight) + (report_score * report_weight)
        
        # Normalize to max_score
        max_score = criteria.get("max_score", 100) if criteria else 100
        normalized_score = min(overall_score, max_score)
        
        return {
            "overall_score": round(normalized_score, 2),
            "max_score": max_score,
            "code_score": round(code_score, 2),
            "report_score": round(report_score, 2),
            "code_breakdown": code_breakdown,
            "report_breakdown": report_breakdown,
            "weights_used": weights,
            "grade": await self._calculate_grade(normalized_score, max_score)
        }
    
    async def _calculate_code_score(self, code_analysis: Dict[str, Any], weights: Dict[str, float]) -> tuple[float, Dict[str, Any]]:
        """Calculate score for code analysis"""
        
        breakdown = {
            "code_quality": {"score": 0, "max": 30, "factors": {}},
            "functionality": {"score": 0, "max": 40, "factors": {}},
            "documentation": {"score": 0, "max": 20, "factors": {}},
            "innovation": {"score": 0, "max": 10, "factors": {}}
        }
        
        # Code Quality (30 points max)
        quality_score = 0
        quality_factors = {}
        
        if "code_quality_score" in code_analysis:
            quality_score = code_analysis["code_quality_score"] * 0.3
            quality_factors["overall_quality"] = code_analysis["code_quality_score"]
        
        if "average_comment_ratio" in code_analysis:
            comment_score = min(code_analysis["average_comment_ratio"] * 100, 15)
            quality_score += comment_score * 0.5
            quality_factors["comment_ratio"] = comment_score
        
        if "average_complexity" in code_analysis:
            complexity = code_analysis["average_complexity"]
            complexity_score = max(0, 15 - (complexity * 2))
            quality_score += complexity_score * 0.5
            quality_factors["complexity"] = complexity_score
        
        breakdown["code_quality"]["score"] = min(quality_score, 30)
        breakdown["code_quality"]["factors"] = quality_factors
        
        # Functionality (40 points max)
        functionality_score = 0
        functionality_factors = {}
        
        if "total_functions" in code_analysis:
            func_count = code_analysis["total_functions"]
            func_score = min(func_count * 2, 20)
            functionality_score += func_score
            functionality_factors["function_count"] = func_score
        
        if "total_classes" in code_analysis:
            class_count = code_analysis["total_classes"]
            class_score = min(class_count * 5, 15)
            functionality_score += class_score
            functionality_factors["class_count"] = class_score
        
        if "file_count" in code_analysis:
            file_count = code_analysis["file_count"]
            file_score = min(file_count * 2, 5)
            functionality_score += file_score
            functionality_factors["file_organization"] = file_score
        
        breakdown["functionality"]["score"] = min(functionality_score, 40)
        breakdown["functionality"]["factors"] = functionality_factors
        
        # Documentation (20 points max)
        documentation_score = 0
        documentation_factors = {}
        
        if "files_analyzed" in code_analysis:
            doc_files = 0
            for file_analysis in code_analysis["files_analyzed"]:
                if file_analysis.get("has_docstring") or file_analysis.get("has_comments"):
                    doc_files += 1
            
            doc_ratio = doc_files / len(code_analysis["files_analyzed"]) if code_analysis["files_analyzed"] else 0
            documentation_score = doc_ratio * 20
            documentation_factors["documented_files"] = doc_ratio * 20
        
        breakdown["documentation"]["score"] = min(documentation_score, 20)
        breakdown["documentation"]["factors"] = documentation_factors
        
        # Innovation (10 points max)
        innovation_score = 0
        innovation_factors = {}
        
        # Check for diverse language usage
        if "languages" in code_analysis and len(code_analysis["languages"]) > 1:
            innovation_score += 3
            innovation_factors["multiple_languages"] = 3
        
        # Check for advanced patterns
        advanced_patterns = 0
        if "files_analyzed" in code_analysis:
            for file_analysis in code_analysis["files_analyzed"]:
                if file_analysis.get("language") == "python":
                    # Check for advanced Python features
                    if file_analysis.get("imports"):
                        imports = file_analysis.get("imports", [])
                        if any("numpy" in imp or "pandas" in imp or "tensorflow" in imp for imp in imports):
                            advanced_patterns += 1
        
        innovation_score += min(advanced_patterns * 2, 7)
        innovation_factors["advanced_patterns"] = min(advanced_patterns * 2, 7)
        
        breakdown["innovation"]["score"] = min(innovation_score, 10)
        breakdown["innovation"]["factors"] = innovation_factors
        
        # Calculate total code score
        total_code_score = (
            breakdown["code_quality"]["score"] +
            breakdown["functionality"]["score"] +
            breakdown["documentation"]["score"] +
            breakdown["innovation"]["score"]
        )
        
        return total_code_score, breakdown
    
    async def _calculate_report_score(self, report_analysis: Dict[str, Any]) -> tuple[float, Dict[str, Any]]:
        """Calculate score for report analysis"""
        
        breakdown = {
            "structure": {"score": 0, "max": 30, "factors": {}},
            "content_quality": {"score": 0, "max": 40, "factors": {}},
            "completeness": {"score": 0, "max": 30, "factors": {}}
        }
        
        # Structure (30 points max)
        structure_score = 0
        structure_factors = {}
        
        if "structure_analysis" in report_analysis:
            structure = report_analysis["structure_analysis"]
            
            if structure.get("has_title"):
                structure_score += 6
                structure_factors["title"] = 6
            
            if structure.get("has_abstract"):
                structure_score += 6
                structure_factors["abstract"] = 6
            
            if structure.get("has_introduction"):
                structure_score += 6
                structure_factors["introduction"] = 6
            
            if structure.get("has_conclusion"):
                structure_score += 6
                structure_factors["conclusion"] = 6
            
            if structure.get("has_references"):
                structure_score += 6
                structure_factors["references"] = 6
            
            # Bonus for additional sections
            section_count = len(structure.get("sections", []))
            if section_count > 5:
                structure_score += min(section_count - 5, 3)
                structure_factors["additional_sections"] = min(section_count - 5, 3)
        
        breakdown["structure"]["score"] = min(structure_score, 30)
        breakdown["structure"]["factors"] = structure_factors
        
        # Content Quality (40 points max)
        content_score = 0
        content_factors = {}
        
        if "content_analysis" in report_analysis:
            content = report_analysis["content_analysis"]
            
            # Technical terms
            tech_term_score = min(len(content.get("technical_terms", [])) * 2, 15)
            content_score += tech_term_score
            content_factors["technical_terms"] = tech_term_score
            
            # Code references
            code_ref_score = min(content.get("code_references", 0) * 3, 10)
            content_score += code_ref_score
            content_factors["code_references"] = code_ref_score
            
            # Diagram references
            diagram_score = min(content.get("diagram_references", 0) * 4, 10)
            content_score += diagram_score
            content_factors["diagrams"] = diagram_score
            
            # Readability
            readability_score = content.get("readability_score", 0) * 0.05
            content_score += readability_score
            content_factors["readability"] = readability_score
        
        breakdown["content_quality"]["score"] = min(content_score, 40)
        breakdown["content_quality"]["factors"] = content_factors
        
        # Completeness (30 points max)
        completeness_score = 0
        completeness_factors = {}
        
        if "quality_metrics" in report_analysis:
            metrics = report_analysis["quality_metrics"]
            
            completeness_score = metrics.get("completeness_score", 0)
            completeness_factors = {
                "word_count": 20 if metrics.get("overall_score", 0) > 50 else 0,
                "technical_depth": 20 if metrics.get("overall_score", 0) > 60 else 0,
                "citations": 20 if metrics.get("overall_score", 0) > 70 else 0
            }
        
        breakdown["completeness"]["score"] = min(completeness_score, 30)
        breakdown["completeness"]["factors"] = completeness_factors
        
        # Calculate total report score
        total_report_score = (
            breakdown["structure"]["score"] +
            breakdown["content_quality"]["score"] +
            breakdown["completeness"]["score"]
        )
        
        return total_report_score, breakdown
    
    async def _calculate_grade(self, score: float, max_score: float) -> str:
        """Calculate letter grade based on score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
    
    async def generate_score_explanation(self, scoring_result: Dict[str, Any]) -> str:
        """Generate human-readable explanation of the score"""
        
        explanation = f"Overall Score: {scoring_result['overall_score']}/{scoring_result['max_score']} (Grade: {scoring_result['grade']})\n\n"
        
        # Code section
        if scoring_result["code_score"] > 0:
            explanation += f"Code Score: {scoring_result['code_score']}/100\n"
            code_breakdown = scoring_result["code_breakdown"]
            
            for category, details in code_breakdown.items():
                if details["score"] > 0:
                    explanation += f"  - {category.replace('_', ' ').title()}: {details['score']}/{details['max']}\n"
        
        # Report section
        if scoring_result["report_score"] > 0:
            explanation += f"\nReport Score: {scoring_result['report_score']}/100\n"
            report_breakdown = scoring_result["report_breakdown"]
            
            for category, details in report_breakdown.items():
                if details["score"] > 0:
                    explanation += f"  - {category.replace('_', ' ').title()}: {details['score']}/{details['max']}\n"
        
        return explanation
    
    async def benchmark_score(self, score: float, max_score: float) -> Dict[str, Any]:
        """Benchmark score against typical distributions"""
        
        percentage = (score / max_score) * 100
        
        # Typical score distributions (approximate)
        benchmarks = {
            "excellent": {"range": (90, 100), "percentile": 90, "description": "Outstanding work"},
            "good": {"range": (80, 89), "percentile": 70, "description": "Above average"},
            "average": {"range": (70, 79), "percentile": 50, "description": "Meets expectations"},
            "below_average": {"range": (60, 69), "percentile": 30, "description": "Needs improvement"},
            "poor": {"range": (0, 59), "percentile": 10, "description": "Significant improvements needed"}
        }
        
        for level, data in benchmarks.items():
            if data["range"][0] <= percentage <= data["range"][1]:
                return {
                    "level": level,
                    "percentile": data["percentile"],
                    "description": data["description"],
                    "percentage": percentage
                }
        
        return benchmarks["poor"]
