from typing import Dict, Any, Optional, List
import json
import logging
from .ollama_service import ollama_service

logger = logging.getLogger(__name__)

class ComprehensiveAnalyzer:
    """Provides deep, comprehensive project analysis using AI"""
    
    def __init__(self):
        self.ollama = ollama_service
    
    async def analyze_project_comprehensively(
        self, 
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None,
        project_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Perform comprehensive analysis of the entire project"""
        
        # Extract project understanding
        project_understanding = await self._analyze_project_essence(
            code_analysis, report_analysis, project_files
        )
        
        # Detailed code analysis
        code_review = await self._detailed_code_review(code_analysis)
        
        # Comprehensive PDF analysis
        report_review = await self._detailed_report_analysis(report_analysis)
        
        # Architecture and design analysis
        architecture_analysis = await self._analyze_architecture(code_analysis)
        
        # Implementation quality assessment
        implementation_review = await self._analyze_implementation_quality(code_analysis)
        
        # Specific improvement recommendations
        detailed_improvements = await self._generate_detailed_improvements(
            code_analysis, report_analysis, project_understanding
        )
        
        return {
            "project_understanding": project_understanding,
            "code_review": code_review,
            "report_review": report_review,
            "architecture_analysis": architecture_analysis,
            "implementation_review": implementation_review,
            "detailed_improvements": detailed_improvements
        }
    
    async def _analyze_project_essence(
        self, 
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None,
        project_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Understand what the project is about"""
        
        context_parts = []
        
        # Add code context
        if code_analysis:
            if 'functions' in code_analysis:
                functions = code_analysis['functions'][:5]  # First 5 functions
                context_parts.append("=== CODE FUNCTIONS ===")
                for func in functions:
                    context_parts.append(f"Function: {func.get('name', 'unknown')}()")
                    if 'docstring' in func and func['docstring']:
                        context_parts.append(f"Description: {func['docstring'][:200]}...")
                    if 'parameters' in func:
                        context_parts.append(f"Parameters: {func['parameters']}")
            
            if 'classes' in code_analysis:
                classes = code_analysis['classes'][:3]  # First 3 classes
                context_parts.append("\n=== CLASSES ===")
                for cls in classes:
                    context_parts.append(f"Class: {cls.get('name', 'unknown')}")
                    if 'methods' in cls:
                        context_parts.append(f"Methods: {', '.join(cls['methods'][:5])}")
            
            if 'imports' in code_analysis:
                important_imports = [imp for imp in code_analysis['imports'] if not imp.startswith('.')]
                if important_imports:
                    context_parts.append(f"\n=== IMPORTS ===")
                    context_parts.append(f"Key libraries: {', '.join(important_imports[:10])}")
        
        # Add report context
        if report_analysis:
            if 'content_analysis' in report_analysis:
                content = report_analysis['content_analysis']
                if 'introduction' in content:
                    context_parts.append(f"\n=== REPORT INTRODUCTION ===")
                    context_parts.append(content['introduction'][:500])
                if 'abstract' in content:
                    context_parts.append(f"\n=== REPORT ABSTRACT ===")
                    context_parts.append(content['abstract'][:300])
        
        # Add file structure context
        if project_files:
            context_parts.append(f"\n=== PROJECT STRUCTURE ===")
            context_parts.append(f"Files: {', '.join(project_files[:10])}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""
Based on the following project information, provide a comprehensive understanding of what this project is about:

{context}

Please analyze and provide:
1. Project Purpose: What problem does this project solve?
2. Main Functionality: What are the key features and capabilities?
3. Technology Stack: What technologies and libraries are being used?
4. Project Scope: How complex and comprehensive is this project?
5. Target Users: Who would use this project?

Format your response as JSON:
{{
    "project_purpose": "Detailed description of what the project does",
    "main_functionality": ["feature1", "feature2", "feature3"],
    "technology_stack": ["tech1", "tech2", "tech3"],
    "project_complexity": "simple/moderate/complex",
    "target_users": "Description of target audience",
    "project_summary": "2-3 sentence summary of the entire project"
}}
"""
        
        response = await self.ollama.generate_json_response(
            prompt=prompt,
            system_prompt="You are an expert software analyst who can deeply understand project purposes and functionality from code and documentation."
        )
        
        return response or {
            "project_purpose": "Unable to determine project purpose",
            "main_functionality": [],
            "technology_stack": [],
            "project_complexity": "unknown",
            "target_users": "unknown",
            "project_summary": "Unable to analyze project"
        }
    
    async def _detailed_code_review(self, code_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform detailed code review"""
        
        if not code_analysis:
            return {"error": "No code analysis available"}
        
        context_parts = []
        
        # Code structure
        if 'functions' in code_analysis:
            context_parts.append(f"Total Functions: {len(code_analysis['functions'])}")
            
            # Analyze function complexity
            complex_functions = [f for f in code_analysis['functions'] if f.get('complexity', 0) > 10]
            if complex_functions:
                context_parts.append(f"Complex Functions: {len(complex_functions)}")
                for func in complex_functions[:3]:
                    context_parts.append(f"- {func.get('name', 'unknown')} (complexity: {func.get('complexity', 0)})")
        
        if 'classes' in code_analysis:
            context_parts.append(f"Total Classes: {len(code_analysis['classes'])}")
        
        if 'imports' in code_analysis:
            context_parts.append(f"External Dependencies: {len(code_analysis['imports'])}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""
Perform a detailed code review based on this analysis:

{context}

Please provide:
1. Code Organization Assessment
2. Design Patterns Used
3. Code Quality Issues
4. Best Practices Adherence
5. Security Considerations
6. Performance Implications
7. Maintainability Assessment

Format as JSON:
{{
    "code_organization": {{
        "structure_rating": "excellent/good/fair/poor",
        "modularity": "assessment of code modularity",
        "separation_of_concerns": "how well concerns are separated"
    }},
    "design_patterns": ["pattern1", "pattern2"],
    "quality_issues": [
        {{
            "type": "issue_type",
            "severity": "high/medium/low",
            "description": "detailed description",
            "location": "where in code this occurs"
        }}
    ],
    "best_practices": {{
        "followed": ["practice1", "practice2"],
        "violated": ["practice1", "practice2"]
    }},
    "security_assessment": {{
        "overall_security": "secure/moderately_secure/vulnerable",
        "issues": ["security_issue1", "security_issue2"]
    }},
    "performance_considerations": ["perf_note1", "perf_note2"],
    "maintainability": {{
        "score": "high/medium/low",
        "factors": ["factor1", "factor2"]
    }}
}}
"""
        
        response = await self.ollama.generate_json_response(
            prompt=prompt,
            system_prompt="You are a senior software engineer conducting a thorough code review."
        )
        
        return response or {"error": "Failed to generate code review"}
    
    async def _detailed_report_analysis(self, report_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform detailed analysis of the PDF report"""
        
        if not report_analysis:
            return {"error": "No report analysis available"}
        
        context_parts = []
        
        if 'content_analysis' in report_analysis:
            content = report_analysis['content_analysis']
            for section in ['introduction', 'methodology', 'results', 'conclusion']:
                if section in content:
                    context_parts.append(f"=== {section.upper()} ===")
                    context_parts.append(content[section][:500])
        
        if 'structure_analysis' in report_analysis:
            structure = report_analysis['structure_analysis']
            context_parts.append(f"\n=== REPORT STRUCTURE ===")
            context_parts.append(f"Has Abstract: {structure.get('has_abstract', False)}")
            context_parts.append(f"Has Introduction: {structure.get('has_introduction', False)}")
            context_parts.append(f"Has Methodology: {structure.get('has_methodology', False)}")
            context_parts.append(f"Has Results: {structure.get('has_results', False)}")
            context_parts.append(f"Has Conclusion: {structure.get('has_conclusion', False)}")
            context_parts.append(f"Has References: {structure.get('has_references', False)}")
        
        if 'quality_metrics' in report_analysis:
            quality = report_analysis['quality_metrics']
            context_parts.append(f"\n=== WRITING QUALITY ===")
            context_parts.append(f"Overall Quality: {quality.get('overall_quality', 'N/A')}/100")
            context_parts.append(f"Clarity: {quality.get('clarity', 'N/A')}/100")
            context_parts.append(f"Completeness: {quality.get('completeness', 'N/A')}/100")
        
        context = "\n".join(context_parts)
        
        prompt = f"""
Perform a comprehensive analysis of this project report:

{context}

Please analyze:
1. Report Structure Completeness
2. Content Quality and Depth
3. Technical Accuracy
4. Writing Clarity and Professionalism
5. Documentation Standards
6. Missing Components
7. Overall Effectiveness

Format as JSON:
{{
    "structure_analysis": {{
        "completeness_score": "excellent/good/fair/poor",
        "missing_sections": ["section1", "section2"],
        "organization_quality": "assessment of report organization"
    }},
    "content_quality": {{
        "technical_depth": "deep/moderate/shallow",
        "analysis_quality": "excellent/good/fair/poor",
        "evidence_support": "well_supported/moderately_supported/poorly_supported"
    }},
    "writing_assessment": {{
        "clarity": "excellent/good/fair/poor",
        "professionalism": "high/medium/low",
        "grammar_quality": "excellent/good/fair/poor"
    }},
    "technical_accuracy": {{
        "accuracy_level": "high/medium/low",
        "concepts_understanding": "excellent/good/fair/poor",
        "methodology_soundness": "sound/questionable/flawed"
    }},
    "documentation_standards": {{
        "follows_standards": true/false,
        "citation_quality": "excellent/good/fair/poor",
        "reference_completeness": "complete/incomplete/missing"
    }},
    "recommendations": [
        "improvement_suggestion1",
        "improvement_suggestion2"
    ],
    "overall_assessment": "summary of report quality"
}}
"""
        
        response = await self.ollama.generate_json_response(
            prompt=prompt,
            system_prompt="You are an expert technical writer and academic evaluator analyzing project documentation."
        )
        
        return response or {"error": "Failed to analyze report"}
    
    async def _analyze_architecture(self, code_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze software architecture and design"""
        
        if not code_analysis:
            return {"error": "No code available for architecture analysis"}
        
        context_parts = []
        
        if 'classes' in code_analysis:
            context_parts.append("=== CLASS ARCHITECTURE ===")
            for cls in code_analysis['classes']:
                context_parts.append(f"Class: {cls.get('name', 'unknown')}")
                if 'methods' in cls:
                    context_parts.append(f"  Methods: {', '.join(cls['methods'])}")
                if 'inheritance' in cls:
                    context_parts.append(f"  Inherits: {cls['inheritance']}")
        
        if 'functions' in code_analysis:
            context_parts.append(f"\n=== FUNCTION DISTRIBUTION ===")
            context_parts.append(f"Total functions: {len(code_analysis['functions'])}")
        
        if 'imports' in code_analysis:
            context_parts.append(f"\n=== DEPENDENCIES ===")
            context_parts.append(f"External libraries: {code_analysis['imports']}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""
Analyze the software architecture and design patterns:

{context}

Please provide:
1. Architecture Style (MVC, Layered, etc.)
2. Design Patterns Identification
3. Coupling and Cohesion Assessment
4. Scalability Considerations
5. Architecture Strengths and Weaknesses

Format as JSON:
{{
    "architecture_style": "identified_architecture_style",
    "design_patterns": {{
        "identified": ["pattern1", "pattern2"],
        "missing_opportunities": ["pattern1", "pattern2"]
    }},
    "coupling_cohesion": {{
        "coupling_level": "tight/loose/moderate",
        "cohesion_level": "high/medium/low",
        "assessment": "detailed assessment"
    }},
    "scalability": {{
        "current_scalability": "high/medium/low",
        "bottlenecks": ["bottleneck1", "bottleneck2"],
        "improvements": ["improvement1", "improvement2"]
    }},
    "architecture_strengths": ["strength1", "strength2"],
    "architecture_weaknesses": ["weakness1", "weakness2"],
    "overall_architecture_score": "excellent/good/fair/poor"
}}
"""
        
        response = await self.ollama.generate_json_response(
            prompt=prompt,
            system_prompt="You are a software architect evaluating system design and architecture."
        )
        
        return response or {"error": "Failed to analyze architecture"}
    
    async def _analyze_implementation_quality(self, code_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze implementation quality and specific code issues"""
        
        if not code_analysis:
            return {"error": "No code available for implementation analysis"}
        
        context_parts = []
        
        # Extract specific code details
        if 'functions' in code_analysis:
            context_parts.append("=== FUNCTION ANALYSIS ===")
            for func in code_analysis['functions'][:10]:  # First 10 functions
                context_parts.append(f"Function: {func.get('name', 'unknown')}")
                context_parts.append(f"  Lines: {func.get('lines', 'unknown')}")
                context_parts.append(f"  Complexity: {func.get('complexity', 'unknown')}")
                if 'parameters' in func:
                    context_parts.append(f"  Parameters: {len(func['parameters'])}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""
Analyze the implementation quality and identify specific code improvements:

{context}

Please provide:
1. Code Quality Assessment
2. Specific Code Issues with Locations
3. Performance Bottlenecks
4. Error Handling Assessment
5. Code Duplication Issues
6. Naming Conventions
7. Code Readability

Format as JSON:
{{
    "code_quality": {{
        "overall_rating": "excellent/good/fair/poor",
        "readability": "excellent/good/fair/poor",
        "efficiency": "excellent/good/fair/poor"
    }},
    "specific_issues": [
        {{
            "issue": "detailed description of issue",
            "severity": "high/medium/low",
            "location": "function_name or area",
            "suggestion": "how to fix it"
        }}
    ],
    "performance_issues": [
        {{
            "issue": "performance problem",
            "impact": "high/medium/low",
            "optimization": "how to optimize"
        }}
    ],
    "error_handling": {{
        "adequacy": "excellent/good/fair/poor",
        "missing_handling": ["area1", "area2"]
    }},
    "code_duplication": {{
        "present": true/false,
        "areas": ["area1", "area2"],
        "refactoring_suggestions": ["suggestion1", "suggestion2"]
    }},
    "naming_conventions": {{
        "consistency": "excellent/good/fair/poor",
        "clarity": "excellent/good/fair/poor",
        "issues": ["issue1", "issue2"]
    }},
    "improvement_priorities": [
        "priority1_improvement",
        "priority2_improvement"
    ]
}}
"""
        
        response = await self.ollama.generate_json_response(
            prompt=prompt,
            system_prompt="You are a senior code reviewer analyzing implementation quality for improvement opportunities."
        )
        
        return response or {"error": "Failed to analyze implementation"}
    
    async def _generate_detailed_improvements(
        self, 
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None,
        project_understanding: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate specific, actionable improvement recommendations"""
        
        context_parts = []
        
        if project_understanding:
            context_parts.append("=== PROJECT CONTEXT ===")
            context_parts.append(f"Project Type: {project_understanding.get('project_purpose', 'Unknown')}")
            context_parts.append(f"Complexity: {project_understanding.get('project_complexity', 'Unknown')}")
        
        context_parts.append("\n=== IMPROVEMENT FOCUS AREAS ===")
        context_parts.append("Code Quality & Structure")
        context_parts.append("Performance & Optimization")
        context_parts.append("Security & Best Practices")
        context_parts.append("Documentation & Reporting")
        context_parts.append("Testing & Validation")
        
        context = "\n".join(context_parts)
        
        prompt = f"""
Generate detailed, specific improvement recommendations for this project:

{context}

Provide actionable recommendations in these categories:

1. Code Structure Improvements
2. Performance Optimizations
3. Security Enhancements
4. Documentation Improvements
5. Testing Recommendations
6. User Experience Improvements
7. Future Enhancement Suggestions

Format as JSON:
{{
    "code_structure": [
        {{
            "improvement": "specific improvement",
            "priority": "high/medium/low",
            "effort": "high/medium/low",
            "impact": "description of expected impact",
            "implementation_steps": ["step1", "step2", "step3"]
        }}
    ],
    "performance_optimizations": [
        {{
            "optimization": "specific optimization",
            "priority": "high/medium/low",
            "expected_gain": "description of performance improvement",
            "implementation": "how to implement"
        }}
    ],
    "security_enhancements": [
        {{
            "enhancement": "security improvement",
            "risk_level": "high/medium/low",
            "implementation": "implementation details"
        }}
    ],
    "documentation_improvements": [
        {{
            "improvement": "documentation enhancement",
            "area": "code/report/both",
            "details": "specific details"
        }}
    ],
    "testing_recommendations": [
        {{
            "test_type": "unit/integration/e2o/performance",
            "coverage_area": "what to test",
            "priority": "high/medium/low"
        }}
    ],
    "user_experience": [
        {{
            "improvement": "UX enhancement",
            "benefit": "user benefit",
            "implementation": "how to implement"
        }}
    ],
    "future_enhancements": [
        {{
            "enhancement": "future feature",
            "complexity": "high/medium/low",
            "business_value": "value description"
        }}
    ]
}}
"""
        
        response = await self.ollama.generate_json_response(
            prompt=prompt,
            system_prompt="You are a senior technical consultant providing detailed improvement recommendations for software projects."
        )
        
        return response or {"error": "Failed to generate improvements"}

# Global instance
comprehensive_analyzer = ComprehensiveAnalyzer()
