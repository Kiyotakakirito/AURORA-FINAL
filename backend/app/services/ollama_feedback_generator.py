from typing import Dict, Any, Optional
import json
import logging
from .ollama_service import ollama_service

logger = logging.getLogger(__name__)

class OllamaFeedbackGenerator:
    """Generate AI-powered feedback using Ollama models"""
    
    def __init__(self):
        self.ollama = ollama_service
    
    async def generate_feedback(
        self, 
        scoring_result: Dict[str, Any],
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive feedback for a project evaluation"""
        
        # Prepare the evaluation context
        context = self._prepare_evaluation_context(
            scoring_result, code_analysis, report_analysis
        )
        
        # Generate different types of feedback
        overall_feedback = await self._generate_overall_feedback(context)
        strengths = await self._generate_strengths(context)
        weaknesses = await self._generate_weaknesses(context)
        recommendations = await self._generate_recommendations(context)
        technical_feedback = await self._generate_technical_feedback(context)
        
        return {
            "overall_feedback": overall_feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "technical_feedback": technical_feedback
        }
    
    def _prepare_evaluation_context(
        self, 
        scoring_result: Dict[str, Any],
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None
    ) -> str:
        """Prepare evaluation context for the AI model"""
        
        context_parts = []
        
        # Add scoring information
        if scoring_result:
            context_parts.append(f"Overall Score: {scoring_result.get('overall_score', 'N/A')}/100")
            
            if 'detailed_scores' in scoring_result:
                scores = scoring_result['detailed_scores']
                context_parts.append(f"Code Quality: {scores.get('code_quality', 'N/A')}/100")
                context_parts.append(f"Functionality: {scores.get('functionality', 'N.A')}/100")
                context_parts.append(f"Documentation: {scores.get('documentation', 'N/A')}/100")
                context_parts.append(f"Innovation: {scores.get('innovation', 'N/A')}/100")
        
        # Add code analysis
        if code_analysis:
            context_parts.append("\n=== Code Analysis ===")
            if 'language' in code_analysis:
                context_parts.append(f"Programming Language: {code_analysis['language']}")
            if 'complexity' in code_analysis:
                context_parts.append(f"Cyclomatic Complexity: {code_analysis['complexity']}")
            if 'quality_score' in code_analysis:
                context_parts.append(f"Code Quality Score: {code_analysis['quality_score']}/100")
            if 'functions' in code_analysis:
                context_parts.append(f"Number of Functions: {len(code_analysis['functions'])}")
        
        # Add report analysis
        if report_analysis:
            context_parts.append("\n=== Report Analysis ===")
            if 'page_count' in report_analysis:
                context_parts.append(f"Report Length: {report_analysis['page_count']} pages")
            if 'structure_analysis' in report_analysis:
                structure = report_analysis['structure_analysis']
                context_parts.append(f"Report Structure: {structure.get('has_abstract', 'Unknown abstract')}, {structure.get('has_introduction', 'Unknown intro')}, {structure.get('has_conclusion', 'Unknown conclusion')}")
            if 'quality_metrics' in report_analysis:
                quality = report_analysis['quality_metrics']
                context_parts.append(f"Writing Quality Score: {quality.get('overall_quality', 'N/A')}/100")
        
        return "\n".join(context_parts)
    
    async def _generate_overall_feedback(self, context: str) -> str:
        """Generate overall project feedback"""
        prompt = f"""
Based on the following project evaluation data, provide comprehensive overall feedback:

{context}

Please provide:
1. A summary of the project's performance
2. Key achievements and areas of excellence
3. Main areas for improvement
4. Overall assessment and recommendation

Be constructive, specific, and encouraging in your feedback.
"""
        
        response = await self.ollama.generate_response(
            prompt=prompt,
            system_prompt="You are an expert software engineering evaluator providing constructive feedback on student projects.",
            temperature=0.7,
            max_tokens=800
        )
        
        return response or "Unable to generate overall feedback at this time."
    
    async def _generate_strengths(self, context: str) -> list:
        """Generate list of project strengths"""
        prompt = f"""
Based on this project evaluation, identify the key strengths:

{context}

List 3-5 specific strengths of this project. For each strength:
- Be specific about what was done well
- Explain why it's valuable
- Keep it concise and positive

Format as a JSON array of strings, like:
["Strength 1 description", "Strength 2 description", "Strength 3 description"]
"""
        
        response = await self.ollama.generate_json_response(prompt)
        
        if response and isinstance(response, list):
            return response[:5]  # Limit to 5 strengths
        
        return ["Well-structured project", "Good implementation approach", "Clear documentation"]
    
    async def _generate_weaknesses(self, context: str) -> list:
        """Generate list of project weaknesses"""
        prompt = f"""
Based on this project evaluation, identify areas for improvement:

{context}

List 3-5 specific areas that need improvement. For each weakness:
- Be specific about what needs work
- Explain why it's important
- Be constructive, not critical

Format as a JSON array of strings, like:
["Area 1 needs improvement", "Area 2 needs improvement", "Area 3 needs improvement"]
"""
        
        response = await self.ollama.generate_json_response(prompt)
        
        if response and isinstance(response, list):
            return response[:5]  # Limit to 5 weaknesses
        
        return ["Could improve error handling", "Add more comprehensive tests", "Enhance documentation"]
    
    async def _generate_recommendations(self, context: str) -> list:
        """Generate actionable recommendations"""
        prompt = f"""
Based on this project evaluation, provide specific actionable recommendations:

{context}

List 3-5 concrete recommendations for improving this project. Each recommendation should:
- Be specific and actionable
- Address identified weaknesses
- Help the student learn and grow

Format as a JSON array of strings, like:
["Recommendation 1", "Recommendation 2", "Recommendation 3"]
"""
        
        response = await self.ollama.generate_json_response(prompt)
        
        if response and isinstance(response, list):
            return response[:5]  # Limit to 5 recommendations
        
        return ["Add comprehensive error handling", "Implement unit tests", "Improve code documentation"]
    
    async def _generate_technical_feedback(self, context: str) -> Dict[str, Any]:
        """Generate detailed technical feedback"""
        prompt = f"""
Based on this project evaluation, provide detailed technical feedback:

{context}

Provide feedback on:
1. Code quality and structure
2. Algorithm design and efficiency
3. Best practices adherence
4. Technical implementation
5. Security considerations

Format your response as JSON with these keys:
{{
  "code_quality": "Feedback on code quality",
  "algorithm_design": "Feedback on algorithm design", 
  "best_practices": "Feedback on best practices",
  "technical_implementation": "Feedback on technical implementation",
  "security": "Feedback on security considerations"
}}
"""
        
        response = await self.ollama.generate_json_response(prompt)
        
        if response and isinstance(response, dict):
            return response
        
        return {
            "code_quality": "Code structure is generally good with room for improvement",
            "algorithm_design": "Algorithms are appropriate for the problem domain",
            "best_practices": "Most best practices are followed",
            "technical_implementation": "Implementation is solid and functional",
            "security": "Basic security considerations are addressed"
        }

# Global instance
ollama_feedback_generator = OllamaFeedbackGenerator()
