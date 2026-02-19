from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class FeedbackGenerator:
    def __init__(self):
        self.feedback_templates = {
            "strengths": {
                "code_quality": [
                    "Excellent code organization and structure",
                    "Good use of comments and documentation",
                    "Clean and readable code style",
                    "Appropriate variable and function naming",
                    "Well-structured project architecture"
                ],
                "functionality": [
                    "Comprehensive implementation of required features",
                    "Good error handling and edge cases",
                    "Efficient algorithms and data structures",
                    "Modular design with good separation of concerns",
                    "Robust functionality with good test coverage"
                ],
                "documentation": [
                    "Clear and comprehensive documentation",
                    "Well-written README with setup instructions",
                    "Good inline comments explaining complex logic",
                    "Proper API documentation",
                    "Useful examples and usage guidelines"
                ],
                "innovation": [
                    "Creative approach to problem-solving",
                    "Innovative use of technologies or patterns",
                    "Original implementation ideas",
                    "Advanced features beyond requirements",
                    "Novel solutions to technical challenges"
                ]
            },
            "weaknesses": {
                "code_quality": [
                    "Code could benefit from better organization",
                    "Consider adding more comments for clarity",
                    "Some functions are too long and could be refactored",
                    "Inconsistent coding style",
                    "Complex code that could be simplified"
                ],
                "functionality": [
                    "Some features appear incomplete",
                    "Limited error handling",
                    "Missing edge case considerations",
                    "Performance could be optimized",
                    "Functionality doesn't fully meet requirements"
                ],
                "documentation": [
                    "Limited or missing documentation",
                    "README needs more detail",
                    "Lack of inline comments",
                    "No API documentation",
                    "Missing setup or usage instructions"
                ],
                "innovation": [
                    "Implementation follows standard patterns without innovation",
                    "Limited creative problem-solving",
                    "Basic implementation without advanced features",
                    "Could explore more modern approaches",
                    "Opportunity for more unique solutions"
                ]
            },
            "recommendations": {
                "code_quality": [
                    "Add more comprehensive comments to explain complex logic",
                    "Consider breaking down large functions into smaller, focused ones",
                    "Implement consistent coding style throughout the project",
                    "Add type hints where applicable",
                    "Consider using linters and formatters for code quality"
                ],
                "functionality": [
                    "Add comprehensive error handling",
                    "Implement additional test cases",
                    "Consider performance optimizations",
                    "Add validation for user inputs",
                    "Implement logging for debugging and monitoring"
                ],
                "documentation": [
                    "Create a comprehensive README with setup instructions",
                    "Add inline comments for complex algorithms",
                    "Document API endpoints and data structures",
                    "Include examples of how to use the project",
                    "Add troubleshooting guide for common issues"
                ],
                "innovation": [
                    "Explore advanced features or technologies",
                    "Consider implementing additional functionality beyond requirements",
                    "Research and apply modern design patterns",
                    "Experiment with different approaches to problems",
                    "Add unique features that differentiate the project"
                ]
            }
        }
    
    async def generate_feedback(
        self,
        scoring_result: Dict[str, Any],
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive feedback based on analysis results"""
        
        feedback = {
            "overall_feedback": "",
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "detailed_feedback": {},
            "actionable_items": [],
            "learning_resources": []
        }
        
        # Generate overall feedback
        feedback["overall_feedback"] = await self._generate_overall_feedback(scoring_result)
        
        # Generate code-specific feedback
        if code_analysis:
            code_feedback = await self._generate_code_feedback(code_analysis, scoring_result.get("code_breakdown", {}))
            feedback["detailed_feedback"]["code"] = code_feedback
            feedback["strengths"].extend(code_feedback.get("strengths", []))
            feedback["weaknesses"].extend(code_feedback.get("weaknesses", []))
            feedback["recommendations"].extend(code_feedback.get("recommendations", []))
        
        # Generate report-specific feedback
        if report_analysis:
            report_feedback = await self._generate_report_feedback(report_analysis, scoring_result.get("report_breakdown", {}))
            feedback["detailed_feedback"]["report"] = report_feedback
            feedback["strengths"].extend(report_feedback.get("strengths", []))
            feedback["weaknesses"].extend(report_feedback.get("weaknesses", []))
            feedback["recommendations"].extend(report_feedback.get("recommendations", []))
        
        # Generate actionable items
        feedback["actionable_items"] = await self._generate_actionable_items(feedback)
        
        # Generate learning resources
        feedback["learning_resources"] = await self._generate_learning_resources(feedback)
        
        return feedback
    
    async def _generate_overall_feedback(self, scoring_result: Dict[str, Any]) -> str:
        """Generate overall project feedback"""
        
        score_percentage = (scoring_result["overall_score"] / scoring_result["max_score"]) * 100
        grade = scoring_result["grade"]
        
        feedback_templates = {
            "A": [
                f"Excellent work! Your project scored {scoring_result['overall_score']}/{scoring_result['max_score']} ({score_percentage:.1f}%). "
                "This demonstrates a strong understanding of the concepts and high-quality implementation.",
                f"Outstanding performance with a score of {scoring_result['overall_score']}/{scoring_result['max_score']}. "
                "Your project shows exceptional quality and attention to detail."
            ],
            "B": [
                f"Good work! Your project scored {scoring_result['overall_score']}/{scoring_result['max_score']} ({score_percentage:.1f}%). "
                "This is a solid implementation with room for minor improvements.",
                f"Well done with a score of {scoring_result['overall_score']}/{scoring_result['max_score']}. "
                "Your project demonstrates good understanding and execution."
            ],
            "C": [
                f"Acceptable work. Your project scored {scoring_result['overall_score']}/{scoring_result['max_score']} ({score_percentage:.1f}%). "
                "The project meets basic requirements but needs improvement in several areas.",
                f"Your project scored {scoring_result['overall_score']}/{scoring_result['max_score']}. "
                "Consider the feedback below to enhance your implementation."
            ],
            "D": [
                f"Your project scored {scoring_result['overall_score']}/{scoring_result['max_score']} ({score_percentage:.1f}%). "
                "Significant improvements are needed to meet expectations.",
                f"The project needs substantial improvement with a score of {scoring_result['overall_score']}/{scoring_result['max_score']}. "
                "Please review the feedback and address the identified issues."
            ],
            "F": [
                f"Your project scored {scoring_result['overall_score']}/{scoring_result['max_score']} ({score_percentage:.1f}%). "
                "The project requires major revisions to meet basic requirements.",
                f"Significant work is needed with a score of {scoring_result['overall_score']}/{scoring_result['max_score']}. "
                "Please consider revisiting the project requirements and implementation approach."
            ]
        }
        
        import random
        return random.choice(feedback_templates.get(grade, feedback_templates["C"]))
    
    async def _generate_code_feedback(self, code_analysis: Dict[str, Any], code_breakdown: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate code-specific feedback"""
        
        feedback = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Analyze code quality
        if "code_quality_score" in code_analysis:
            quality_score = code_analysis["code_quality_score"]
            
            if quality_score >= 80:
                feedback["strengths"].append("Excellent code quality with good structure and readability")
            elif quality_score >= 60:
                feedback["strengths"].append("Good code quality with room for improvement")
            else:
                feedback["weaknesses"].append("Code quality needs improvement")
                feedback["recommendations"].append("Focus on improving code organization and readability")
        
        # Analyze comment ratio
        if "average_comment_ratio" in code_analysis:
            comment_ratio = code_analysis["average_comment_ratio"]
            
            if comment_ratio >= 0.15:
                feedback["strengths"].append("Good documentation with appropriate comments")
            elif comment_ratio >= 0.08:
                feedback["recommendations"].append("Consider adding more comments to explain complex logic")
            else:
                feedback["weaknesses"].append("Insufficient comments and documentation")
                feedback["recommendations"].append("Add comprehensive comments to improve code maintainability")
        
        # Analyze complexity
        if "average_complexity" in code_analysis:
            complexity = code_analysis["average_complexity"]
            
            if complexity <= 5:
                feedback["strengths"].append("Code maintains good complexity levels")
            elif complexity <= 10:
                feedback["recommendations"].append("Consider simplifying complex functions")
            else:
                feedback["weaknesses"].append("High code complexity may impact maintainability")
                feedback["recommendations"].append("Refactor complex functions into smaller, simpler ones")
        
        # Analyze functionality
        if "total_functions" in code_analysis:
            func_count = code_analysis["total_functions"]
            
            if func_count >= 10:
                feedback["strengths"].append("Good functional coverage with multiple functions")
            elif func_count >= 5:
                feedback["strengths"].append("Adequate functional implementation")
            else:
                feedback["recommendations"].append("Consider expanding functionality with additional features")
        
        # Analyze file organization
        if "file_count" in code_analysis:
            file_count = code_analysis["file_count"]
            
            if file_count >= 5:
                feedback["strengths"].append("Well-organized project with multiple files")
            elif file_count >= 2:
                feedback["strengths"].append("Basic file organization")
            else:
                feedback["recommendations"].append("Consider organizing code into multiple files for better structure")
        
        return feedback
    
    async def _generate_report_feedback(self, report_analysis: Dict[str, Any], report_breakdown: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate report-specific feedback"""
        
        feedback = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Analyze structure
        if "structure_analysis" in report_analysis:
            structure = report_analysis["structure_analysis"]
            
            structure_elements = []
            if structure.get("has_title"):
                structure_elements.append("title")
            if structure.get("has_abstract"):
                structure_elements.append("abstract")
            if structure.get("has_introduction"):
                structure_elements.append("introduction")
            if structure.get("has_conclusion"):
                structure_elements.append("conclusion")
            if structure.get("has_references"):
                structure_elements.append("references")
            
            if len(structure_elements) >= 4:
                feedback["strengths"].append("Well-structured report with all essential sections")
            elif len(structure_elements) >= 3:
                feedback["strengths"].append("Good report structure")
            else:
                feedback["weaknesses"].append("Report structure needs improvement")
                feedback["recommendations"].append("Include essential sections: introduction, methodology, results, and conclusion")
        
        # Analyze content quality
        if "content_analysis" in report_analysis:
            content = report_analysis["content_analysis"]
            
            # Technical terms
            tech_terms = len(content.get("technical_terms", []))
            if tech_terms >= 10:
                feedback["strengths"].append("Rich technical content with appropriate terminology")
            elif tech_terms >= 5:
                feedback["strengths"].append("Good technical content")
            else:
                feedback["recommendations"].append("Include more technical details and terminology")
            
            # Code references
            code_refs = content.get("code_references", 0)
            if code_refs >= 5:
                feedback["strengths"].append("Excellent integration of code examples")
            elif code_refs >= 2:
                feedback["strengths"].append("Good use of code examples")
            else:
                feedback["recommendations"].append("Include more code examples to illustrate implementation")
            
            # Diagram references
            diagram_refs = content.get("diagram_references", 0)
            if diagram_refs >= 3:
                feedback["strengths"].append("Good use of diagrams and visual elements")
            elif diagram_refs >= 1:
                feedback["strengths"].append("Includes visual elements")
            else:
                feedback["recommendations"].append("Consider adding diagrams to illustrate concepts")
        
        # Analyze quality metrics
        if "quality_metrics" in report_analysis:
            metrics = report_analysis["quality_metrics"]
            overall_score = metrics.get("overall_score", 0)
            
            if overall_score >= 80:
                feedback["strengths"].append("High-quality report with comprehensive coverage")
            elif overall_score >= 60:
                feedback["strengths"].append("Good report quality")
            else:
                feedback["weaknesses"].append("Report quality needs improvement")
        
        return feedback
    
    async def _generate_actionable_items(self, feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable improvement items"""
        
        actionable_items = []
        
        # Code-related actionable items
        if "code" in feedback.get("detailed_feedback", {}):
            code_feedback = feedback["detailed_feedback"]["code"]
            
            if any("comment" in item.lower() for item in code_feedback.get("recommendations", [])):
                actionable_items.append({
                    "category": "Documentation",
                    "priority": "Medium",
                    "action": "Add comprehensive comments to explain complex logic and algorithms",
                    "estimated_time": "2-4 hours",
                    "impact": "High"
                })
            
            if any("complex" in item.lower() for item in code_feedback.get("recommendations", [])):
                actionable_items.append({
                    "category": "Code Quality",
                    "priority": "High",
                    "action": "Refactor complex functions into smaller, more focused units",
                    "estimated_time": "4-8 hours",
                    "impact": "High"
                })
        
        # Report-related actionable items
        if "report" in feedback.get("detailed_feedback", {}):
            report_feedback = feedback["detailed_feedback"]["report"]
            
            if any("structure" in item.lower() for item in report_feedback.get("recommendations", [])):
                actionable_items.append({
                    "category": "Report Structure",
                    "priority": "Medium",
                    "action": "Reorganize report to include introduction, methodology, results, and conclusion",
                    "estimated_time": "1-2 hours",
                    "impact": "Medium"
                })
            
            if any("code example" in item.lower() for item in report_feedback.get("recommendations", [])):
                actionable_items.append({
                    "category": "Report Content",
                    "priority": "Medium",
                    "action": "Add code snippets and examples to illustrate implementation",
                    "estimated_time": "2-3 hours",
                    "impact": "Medium"
                })
        
        return actionable_items
    
    async def _generate_learning_resources(self, feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate relevant learning resources based on feedback"""
        
        resources = []
        
        # Code quality resources
        if any("quality" in item.lower() for item in feedback.get("recommendations", [])):
            resources.extend([
                {
                    "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                    "type": "Book",
                    "description": "Essential guide to writing clean, maintainable code",
                    "url": "https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350884"
                },
                {
                    "title": "Refactoring: Improving the Design of Existing Code",
                    "type": "Book",
                    "description": "Learn techniques for improving code structure and design",
                    "url": "https://www.amazon.com/Refactoring-Improving-Design-Existing-Code/dp/0201485672"
                }
            ])
        
        # Documentation resources
        if any("document" in item.lower() for item in feedback.get("recommendations", [])):
            resources.extend([
                {
                    "title": "Read the Docs",
                    "type": "Website",
                    "description": "Comprehensive guide to technical documentation",
                    "url": "https://www.writethedocs.org/"
                },
                {
                    "title": "Google Technical Writing Courses",
                    "type": "Online Course",
                    "description": "Free courses on technical writing and documentation",
                    "url": "https://developers.google.com/tech-writing"
                }
            ])
        
        # General programming resources
        resources.extend([
            {
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "type": "Book",
                "description": "Classic guide to software design patterns",
                "url": "https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612"
            },
            {
                "title": "The Pragmatic Programmer",
                "type": "Book",
                "description": "Practical advice for improving programming skills",
                "url": "https://www.amazon.com/Pragmatic-Programmer-journey-mastery-Anniversary/dp/0135957052"
            }
        ])
        
        return resources
    
    async def format_feedback_for_display(self, feedback: Dict[str, Any]) -> str:
        """Format feedback for user-friendly display"""
        
        formatted = f"# Project Evaluation Feedback\n\n"
        
        # Overall feedback
        formatted += f"## Overall Assessment\n{feedback['overall_feedback']}\n\n"
        
        # Strengths
        if feedback["strengths"]:
            formatted += "## Strengths\n\n"
            for strength in feedback["strengths"]:
                formatted += f"✅ {strength}\n"
            formatted += "\n"
        
        # Areas for improvement
        if feedback["weaknesses"]:
            formatted += "## Areas for Improvement\n\n"
            for weakness in feedback["weaknesses"]:
                formatted += f"⚠️ {weakness}\n"
            formatted += "\n"
        
        # Recommendations
        if feedback["recommendations"]:
            formatted += "## Recommendations\n\n"
            for recommendation in feedback["recommendations"]:
                formatted += f"💡 {recommendation}\n"
            formatted += "\n"
        
        # Actionable items
        if feedback["actionable_items"]:
            formatted += "## Actionable Items\n\n"
            for item in feedback["actionable_items"]:
                formatted += f"### {item['category']} (Priority: {item['priority']})\n"
                formatted += f"- **Action**: {item['action']}\n"
                formatted += f"- **Estimated Time**: {item['estimated_time']}\n"
                formatted += f"- **Impact**: {item['impact']}\n\n"
        
        # Learning resources
        if feedback["learning_resources"]:
            formatted += "## Learning Resources\n\n"
            for resource in feedback["learning_resources"]:
                formatted += f"### {resource['title']} ({resource['type']})\n"
                formatted += f"{resource['description']}\n"
                formatted += f"[Learn more]({resource['url']})\n\n"
        
        return formatted
