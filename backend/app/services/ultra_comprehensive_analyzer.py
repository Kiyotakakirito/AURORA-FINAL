"""
Ultra-Comprehensive Project Analyzer
Provides extremely detailed, line-by-line analysis using Ollama models
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
import ast
import re
from datetime import datetime

from .ollama_service import ollama_service
from ..core.config import settings


class UltraComprehensiveAnalyzer:
    """Ultra-detailed project analyzer using Ollama for comprehensive analysis"""
    
    def __init__(self):
        self.ollama_service = ollama_service
        self.model = settings.ollama_model
        
    async def analyze_project_ultra_comprehensively(
        self,
        code_analysis: Optional[Dict[str, Any]] = None,
        report_analysis: Optional[Dict[str, Any]] = None,
        project_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform ultra-comprehensive analysis of the project using real data
        """
        try:
            # Initialize analysis result
            analysis_result = {
                "analysis_timestamp": datetime.now().isoformat(),
                "analysis_model": self.model,
                "ultra_detailed_analysis": {}
            }
            
            # 1. Deep Project Essence Analysis - Using real data
            project_essence = await self._analyze_project_essence_real(
                code_analysis, report_analysis, project_files
            )
            analysis_result["ultra_detailed_analysis"]["project_essence"] = project_essence
            
            # 2. Line-by-Line Code Analysis - Using actual code files
            line_by_line_analysis = await self._analyze_code_real_files(
                code_analysis, project_files
            )
            analysis_result["ultra_detailed_analysis"]["line_by_line_analysis"] = line_by_line_analysis
            
            # 3. Complete Tech Stack Identification - From actual dependencies
            tech_stack_analysis = await self._identify_tech_stack_real(
                code_analysis, project_files
            )
            analysis_result["ultra_detailed_analysis"]["tech_stack_analysis"] = tech_stack_analysis
            
            # 4. PDF-Project Matching Analysis - Compare actual content
            pdf_project_matching = await self._analyze_pdf_project_matching_real(
                code_analysis, report_analysis
            )
            analysis_result["ultra_detailed_analysis"]["pdf_project_matching"] = pdf_project_matching
            
            # 5. Strict Scoring Analysis - Based on actual code quality
            strict_scoring = await self._perform_strict_scoring_real(
                code_analysis, report_analysis, project_files
            )
            analysis_result["ultra_detailed_analysis"]["strict_scoring"] = strict_scoring
            
            # 6. Ultra-Detailed Implementation Review - Real code review
            implementation_review = await self._implementation_review_real(
                code_analysis, project_files
            )
            analysis_result["ultra_detailed_analysis"]["implementation_review"] = implementation_review
            
            # 7. Comprehensive Quality Metrics - Real metrics calculation
            quality_metrics = await self._calculate_quality_metrics_real(
                code_analysis, report_analysis, project_files
            )
            analysis_result["ultra_detailed_analysis"]["quality_metrics"] = quality_metrics
            
            return analysis_result
            
        except Exception as e:
            return {
                "error": f"Ultra-comprehensive analysis failed: {str(e)}",
                "analysis_timestamp": datetime.now().isoformat(),
                "ultra_detailed_analysis": {}
            }
    
    async def _analyze_project_essence_real(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        report_analysis: Optional[Dict[str, Any]],
        project_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Analyze project essence using real project data"""
        
        # Extract real project information
        real_project_info = self._extract_real_project_info(code_analysis, project_files)
        
        prompt = f"""
        Analyze this REAL project with extreme detail based on actual code and files:

        ACTUAL PROJECT DATA:
        {json.dumps(real_project_info, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Report Analysis Results:
        {json.dumps(report_analysis, indent=2) if report_analysis else "No report analysis available"}

        Project Files Found:
        {json.dumps(project_files, indent=2) if project_files else "No file list available"}

        CRITICAL: Provide UNIQUE, project-specific analysis. Do NOT use generic templates.
        Analyze what THIS SPECIFIC project actually does based on the real data above.

        Provide ultra-detailed analysis covering:
        1. **ACTUAL Project Purpose**: What does this specific codebase actually do?
        2. **Real Functionality**: What features are actually implemented in the code?
        3. **Actual Architecture**: How is this project really structured?
        4. **Real Technologies**: What technologies are actually used based on dependencies and code?
        5. **True Complexity**: How complex is this project really?
        6. **Actual Target Users**: Who would actually use this based on features?
        7. **Real Business Value**: What value does this specific implementation provide?
        8. **Actual Innovation**: What's innovative about THIS specific project?
        9. **Real Scalability**: How scalable is the current implementation?
        10. **True Market Fit**: How well does this fit market needs based on actual features?

        Be extremely specific and reference actual code, files, and implementation details.
        Do not provide generic analysis - analyze what's actually in this project.
        Respond with detailed JSON containing project-specific insights.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "analysis": response,
                "real_project_data": real_project_info,
                "project_specific_insights": self._parse_project_specific_insights(response),
                "confidence_score": self._calculate_confidence_score(response)
            }
        except Exception as e:
            return {"error": f"Real project essence analysis failed: {str(e)}"}
    
    def _extract_real_project_info(self, code_analysis: Optional[Dict[str, Any]], project_files: Optional[List[str]]) -> Dict[str, Any]:
        """Extract real project information from code analysis and files"""
        real_info = {
            "file_structure": {},
            "dependencies": [],
            "actual_features": [],
            "code_patterns": [],
            "technologies_detected": []
        }
        
        if project_files:
            # Analyze file structure
            for file_path in project_files:
                file_info = {
                    "path": file_path,
                    "type": self._get_file_type(file_path),
                    "purpose": self._infer_file_purpose(file_path)
                }
                real_info["file_structure"][file_path] = file_info
        
        if code_analysis:
            # Extract actual features from code analysis
            if "files_analyzed" in code_analysis:
                for file_data in code_analysis["files_analyzed"]:
                    if "functions" in file_data:
                        real_info["actual_features"].extend(file_data["functions"])
                    if "classes" in file_data:
                        real_info["actual_features"].extend(file_data["classes"])
            
            # Extract dependencies
            if "dependencies" in code_analysis:
                real_info["dependencies"] = code_analysis["dependencies"]
            
            # Extract technologies
            if "technologies" in code_analysis:
                real_info["technologies_detected"] = code_analysis["technologies"]
        
        return real_info
    
    def _get_file_type(self, file_path: str) -> str:
        """Determine file type from path"""
        if file_path.endswith('.js') or file_path.endswith('.jsx'):
            return "javascript"
        elif file_path.endswith('.ts') or file_path.endswith('.tsx'):
            return "typescript"
        elif file_path.endswith('.py'):
            return "python"
        elif file_path.endswith('.java'):
            return "java"
        elif file_path.endswith('.css'):
            return "stylesheet"
        elif file_path.endswith('.html'):
            return "markup"
        elif file_path.endswith('.json'):
            return "config"
        elif file_path.endswith('.md'):
            return "documentation"
        else:
            return "unknown"
    
    def _infer_file_purpose(self, file_path: str) -> str:
        """Infer the purpose of a file from its name and path"""
        path_lower = file_path.lower()
        
        if 'app' in path_lower or 'main' in path_lower:
            return "main_application"
        elif 'controller' in path_lower:
            return "request_handling"
        elif 'model' in path_lower:
            return "data_model"
        elif 'service' in path_lower:
            return "business_logic"
        elif 'util' in path_lower or 'helper' in path_lower:
            return "utility_functions"
        elif 'config' in path_lower:
            return "configuration"
        elif 'test' in path_lower:
            return "testing"
        elif 'component' in path_lower:
            return "ui_component"
        elif 'api' in path_lower:
            return "api_endpoint"
        elif 'database' in path_lower or 'db' in path_lower:
            return "database_related"
        elif 'auth' in path_lower:
            return "authentication"
        elif 'route' in path_lower:
            return "routing"
        else:
            return "general"
    
    def _parse_project_specific_insights(self, response: str) -> Dict[str, Any]:
        """Parse project-specific insights from Ollama response"""
        insights = {
            "unique_features": [],
            "specific_technologies": [],
            "actual_complexity": "",
            "real_purpose": "",
            "specific_issues": []
        }
        
        # Extract specific features mentioned
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['feature:', 'functionality:', 'implements:']):
                insights["unique_features"].append(line.strip())
            elif any(keyword in line.lower() for keyword in ['technology:', 'framework:', 'library:']):
                insights["specific_technologies"].append(line.strip())
            elif any(keyword in line.lower() for keyword in ['complexity:', 'difficult:', 'simple:']):
                insights["actual_complexity"] = line.strip()
            elif any(keyword in line.lower() for keyword in ['purpose:', 'goal:', 'objective:']):
                insights["real_purpose"] = line.strip()
            elif any(keyword in line.lower() for keyword in ['issue:', 'problem:', 'concern:']):
                insights["specific_issues"].append(line.strip())
        
        return insights
    
    async def _analyze_code_real_files(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        project_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Perform real line-by-line code analysis using actual code files"""
        
        # Extract actual code content and structure
        real_code_data = self._extract_real_code_data(code_analysis, project_files)
        
        prompt = f"""
        Perform extremely detailed line-by-line analysis of this ACTUAL code:

        REAL CODE DATA:
        {json.dumps(real_code_data, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Project Files:
        {json.dumps(project_files, indent=2) if project_files else "No file list available"}

        CRITICAL: Analyze the ACTUAL code provided above. Do not provide generic analysis.
        Focus on what's really in these files.

        For each specific file in the project, provide:
        1. **File Overview**: What this specific file actually does
        2. **Line-by-Line Analysis**: Critical lines and their real purpose
        3. **Actual Code Quality**: Real issues in this specific code
        4. **Real Complexity**: Actual complexity of this file
        5. **Security Issues**: Real vulnerabilities in the code
        6. **Performance Issues**: Actual performance problems
        7. **Maintainability**: How maintainable this specific code is
        8. **Code Smells**: Real anti-patterns found
        9. **Best Practices**: Actual adherence to best practices
        10. **Specific Improvements**: Concrete suggestions for this code

        Reference actual function names, variable names, and code patterns.
        Be extremely specific about what's in the code.
        Do not provide generic feedback - analyze what's actually written.
        Respond with detailed JSON structure containing file-specific analysis.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "line_by_line_details": response,
                "real_code_analysis": real_code_data,
                "file_specific_issues": self._extract_file_specific_issues(response),
                "actual_code_quality": self._extract_actual_code_quality(response)
            }
        except Exception as e:
            return {"error": f"Real code analysis failed: {str(e)}"}
    
    def _extract_real_code_data(self, code_analysis: Optional[Dict[str, Any]], project_files: Optional[List[str]]) -> Dict[str, Any]:
        """Extract real code data from analysis"""
        real_code = {
            "files": {},
            "functions": [],
            "classes": [],
            "imports": [],
            "patterns": []
        }
        
        if code_analysis and "files_analyzed" in code_analysis:
            for file_data in code_analysis["files_analyzed"]:
                file_name = file_data.get("file_name", "unknown")
                real_code["files"][file_name] = {
                    "functions": file_data.get("functions", []),
                    "classes": file_data.get("classes", []),
                    "imports": file_data.get("imports", []),
                    "lines_of_code": file_data.get("lines_of_code", 0),
                    "complexity": file_data.get("complexity", 0)
                }
                
                # Collect all functions and classes
                real_code["functions"].extend(file_data.get("functions", []))
                real_code["classes"].extend(file_data.get("classes", []))
                real_code["imports"].extend(file_data.get("imports", []))
        
        return real_code
    
    def _extract_file_specific_issues(self, response: str) -> List[Dict[str, Any]]:
        """Extract file-specific issues from response"""
        issues = []
        lines = response.split('\n')
        current_file = None
        
        for line in lines:
            if '.js' in line or '.py' in line or '.ts' in line or '.java' in line:
                current_file = line.strip()
            elif current_file and any(keyword in line.lower() for keyword in ['issue:', 'problem:', 'error:', 'bug:']):
                issues.append({
                    "file": current_file,
                    "issue": line.strip(),
                    "severity": self._determine_severity(line)
                })
        
        return issues
    
    def _extract_actual_code_quality(self, response: str) -> Dict[str, Any]:
        """Extract actual code quality metrics from response"""
        quality = {
            "overall_rating": "",
            "specific_issues": [],
            "good_practices": [],
            "complexity_assessment": ""
        }
        
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['quality:', 'rating:', 'score:']):
                quality["overall_rating"] = line.strip()
            elif any(keyword in line.lower() for keyword in ['good:', 'well:', 'excellent:']):
                quality["good_practices"].append(line.strip())
            elif any(keyword in line.lower() for keyword in ['complex:', 'simple:', 'difficult:']):
                quality["complexity_assessment"] = line.strip()
        
        return quality
    
    async def _identify_tech_stack_real(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        project_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Identify real technology stack from actual dependencies and code"""
        
        # Extract real technology information
        real_tech_data = self._extract_real_tech_data(code_analysis, project_files)
        
        prompt = f"""
        Identify the ACTUAL technology stack from this real project data:

        REAL TECHNOLOGY DATA:
        {json.dumps(real_tech_data, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Project Files:
        {json.dumps(project_files, indent=2) if project_files else "No file list available"}

        CRITICAL: Identify ONLY the technologies that are actually used in this project.
        Do not suggest or assume technologies - analyze what's really there.

        Provide comprehensive tech stack analysis covering:
        1. **Actual Frontend Technologies**: What frontend frameworks/libraries are really used
        2. **Real Backend Technologies**: What backend technologies are actually implemented
        3. **Actual Development Tools**: What build tools and package managers are used
        4. **Real Infrastructure**: What deployment/infrastructure tools are present
        5. **Actual Third-party Services**: What external APIs/services are integrated
        6. **Real Data Technologies**: What databases/storage are actually used
        7. **Actual Security Technologies**: What security measures are implemented
        8. **Real Testing Stack**: What testing frameworks are actually used
        9. **Actual Documentation Tools**: What documentation tools are present
        10. **Real Version Control**: What version control/collaboration tools are used

        For each technology, identify:
        - Exact version if detectable from dependencies
        - How it's actually used in the code
        - Integration points with other technologies
        - Configuration files that prove its usage
        - Import statements that confirm its presence

        Be extremely specific and reference actual package.json, requirements.txt, imports, etc.
        Do not list technologies that are not actually used.
        Respond with detailed JSON structure.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "complete_tech_stack": response,
                "real_tech_data": real_tech_data,
                "detected_technologies": self._parse_detected_technologies(response),
                "integration_analysis": self._analyze_real_integrations(response)
            }
        except Exception as e:
            return {"error": f"Real tech stack analysis failed: {str(e)}"}
    
    def _extract_real_tech_data(self, code_analysis: Optional[Dict[str, Any]], project_files: Optional[List[str]]) -> Dict[str, Any]:
        """Extract real technology data from project"""
        tech_data = {
            "package_files": {},
            "imports_found": [],
            "config_files": [],
            "dependencies": []
        }
        
        if project_files:
            # Look for package files
            for file_path in project_files:
                if any(pkg_file in file_path.lower() for pkg_file in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle']):
                    tech_data["package_files"][file_path] = "dependency_file"
                elif any(config in file_path.lower() for config in ['webpack', 'vite', 'babel', 'eslint', 'tsconfig']):
                    tech_data["config_files"].append(file_path)
        
        if code_analysis:
            # Extract imports and dependencies
            if "files_analyzed" in code_analysis:
                for file_data in code_analysis["files_analyzed"]:
                    if "imports" in file_data:
                        tech_data["imports_found"].extend(file_data["imports"])
            
            if "dependencies" in code_analysis:
                tech_data["dependencies"] = code_analysis["dependencies"]
        
        return tech_data
    
    def _parse_detected_technologies(self, response: str) -> Dict[str, List[str]]:
        """Parse detected technologies from response"""
        technologies = {
            "frontend": [],
            "backend": [],
            "database": [],
            "tools": [],
            "other": []
        }
        
        lines = response.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(tech in line_lower for tech in ['react', 'vue', 'angular', 'html', 'css', 'javascript', 'typescript']):
                technologies["frontend"].append(line.strip())
            elif any(tech in line_lower for tech in ['node', 'python', 'java', 'php', 'ruby', 'go', 'rust', 'express', 'django', 'flask']):
                technologies["backend"].append(line.strip())
            elif any(tech in line_lower for tech in ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite']):
                technologies["database"].append(line.strip())
            elif any(tech in line_lower for tech in ['npm', 'webpack', 'vite', 'babel', 'eslint']):
                technologies["tools"].append(line.strip())
        
        return technologies
    
    def _analyze_real_integrations(self, response: str) -> List[str]:
        """Analyze real technology integrations from response"""
        integrations = []
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['integrates', 'connects', 'uses', 'implements']):
                integrations.append(line.strip())
        
        return integrations[:10]  # Top 10 integrations
    
    async def _analyze_pdf_project_matching_real(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        report_analysis: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze real PDF-project matching using actual content"""
        
        # Extract real content for comparison
        real_code_content = self._extract_code_content_for_matching(code_analysis)
        real_pdf_content = self._extract_pdf_content_for_matching(report_analysis)
        
        prompt = f"""
        Analyze the match between ACTUAL PDF documentation and REAL project implementation:

        REAL CODE CONTENT:
        {json.dumps(real_code_content, indent=2)}
        
        REAL PDF CONTENT:
        {json.dumps(real_pdf_content, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Report Analysis Results:
        {json.dumps(report_analysis, indent=2) if report_analysis else "No report analysis available"}

        CRITICAL: Compare what's ACTUALLY in the code with what's ACTUALLY in the PDF.
        Do not provide generic analysis - compare the real content.

        Provide detailed matching analysis covering:
        1. **Real Feature Alignment**: Which features described in PDF are actually implemented in code?
        2. **Actual Architecture Consistency**: Does the real implementation match the described architecture?
        3. **Real Technology Stack Verification**: Are the technologies in the PDF actually used in code?
        4. **Actual Functionality Completeness**: What percentage of described functionality is really implemented?
        5. **Real Documentation Accuracy**: How accurate is the documentation compared to actual code?
        6. **Missing Features**: What's described in PDF but not found in code?
        7. **Extra Features**: What's implemented in code but not mentioned in PDF?
        8. **Real Implementation Quality**: How well does the actual implementation match specifications?
        9. **Actual User Experience Alignment**: Does the real UX match the described UX?
        10. **Real Business Logic Consistency**: Does the actual business logic match the description?

        For each discrepancy, provide:
        - Specific details of the mismatch
        - Impact assessment (critical, major, minor)
        - Evidence from actual code or documentation
        - Concrete recommendations for alignment

        Calculate an actual alignment score (0-100) based on real comparison.
        Be extremely specific about what matches and what doesn't.
        Respond with detailed JSON structure.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "matching_analysis": response,
                "real_comparison_data": {
                    "code_content": real_code_content,
                    "pdf_content": real_pdf_content
                },
                "actual_alignment_score": self._extract_real_alignment_score(response),
                "specific_discrepancies": self._extract_specific_discrepancies(response),
                "concrete_recommendations": self._extract_concrete_recommendations(response)
            }
        except Exception as e:
            return {"error": f"Real PDF-project matching analysis failed: {str(e)}"}
    
    def _extract_code_content_for_matching(self, code_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract code content for PDF matching"""
        content = {
            "features_found": [],
            "technologies_used": [],
            "architecture_patterns": [],
            "functions_implemented": []
        }
        
        if code_analysis:
            if "files_analyzed" in code_analysis:
                for file_data in code_analysis["files_analyzed"]:
                    if "functions" in file_data:
                        content["functions_implemented"].extend(file_data["functions"])
                    if "classes" in file_data:
                        content["functions_implemented"].extend(file_data["classes"])
            
            if "technologies" in code_analysis:
                content["technologies_used"] = code_analysis["technologies"]
            
            if "patterns" in code_analysis:
                content["architecture_patterns"] = code_analysis["patterns"]
        
        return content
    
    def _extract_pdf_content_for_matching(self, report_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract PDF content for code matching"""
        content = {
            "features_described": [],
            "technologies_mentioned": [],
            "architecture_described": "",
            "requirements_listed": []
        }
        
        if report_analysis:
            if "features" in report_analysis:
                content["features_described"] = report_analysis["features"]
            
            if "technologies" in report_analysis:
                content["technologies_mentioned"] = report_analysis["technologies"]
            
            if "architecture" in report_analysis:
                content["architecture_described"] = report_analysis["architecture"]
            
            if "requirements" in report_analysis:
                content["requirements_listed"] = report_analysis["requirements"]
        
        return content
    
    def _extract_real_alignment_score(self, response: str) -> float:
        """Extract real alignment score from response"""
        import re
        score_patterns = [
            r'(\d+)%.*alignment',
            r'alignment.*?(\d+)%',
            r'score.*?(\d+)',
            r'(\d+)/100'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, response.lower())
            if match:
                try:
                    return float(match.group(1))
                except:
                    continue
        
        return 75.0  # Default if no score found
    
    def _extract_specific_discrepancies(self, response: str) -> List[Dict[str, Any]]:
        """Extract specific discrepancies from response"""
        discrepancies = []
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['missing', 'different', 'mismatch', 'not found', 'discrepancy']):
                discrepancies.append({
                    "description": line.strip(),
                    "severity": self._determine_severity(line),
                    "category": self._determine_category(line)
                })
        
        return discrepancies[:10]  # Top 10 discrepancies
    
    def _extract_concrete_recommendations(self, response: str) -> List[str]:
        """Extract concrete recommendations from response"""
        recommendations = []
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'could', 'add', 'implement']):
                recommendations.append(line.strip())
        
        return recommendations[:5]  # Top 5 recommendations
    
    async def _perform_strict_scoring_real(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        report_analysis: Optional[Dict[str, Any]],
        project_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Perform strict scoring based on actual code quality"""
        
        # Calculate real metrics for scoring
        real_metrics = self._calculate_real_scoring_metrics(code_analysis, project_files)
        
        prompt = f"""
        Perform STRICT, detailed scoring of this ACTUAL project:

        REAL PROJECT METRICS:
        {json.dumps(real_metrics, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Report Analysis Results:
        {json.dumps(report_analysis, indent=2) if report_analysis else "No report analysis available"}

        Project Files:
        {json.dumps(project_files, indent=2) if project_files else "No file list available"}

        CRITICAL: Provide STRICT, HONEST scoring based on the ACTUAL code quality.
        Do not give generous scores - evaluate what's really implemented.

        Provide strict scoring (0-100) for each category with detailed justification:

        1. **Code Quality Score** (0-100):
           - Actual code organization and structure
           - Real naming conventions and readability
           - Actual error handling and edge cases
           - Real performance optimization
           - Actual security best practices
           - Real testing coverage and quality

        2. **Functionality Score** (0-100):
           - Actual feature completeness
           - Real user experience quality
           - Actual business logic implementation
           - Real data handling and validation
           - Actual integration quality
           - Real reliability and stability

        3. **Documentation Score** (0-100):
           - Actual code documentation quality
           - Real API documentation completeness
           - Actual README and setup instructions
           - Real architecture documentation
           - Actual user guides and examples
           - Real comments and inline documentation

        4. **Innovation Score** (0-100):
           - Actual originality and creativity
           - Real technical innovation
           - Actual problem-solving approach
           - Real use of new technologies
           - Actual unique features or approaches
           - Real market differentiation

        5. **Architecture Score** (0-100):
           - Actual system design quality
           - Real scalability considerations
           - Actual modularity and separation of concerns
           - Real design patterns usage
           - Actual technology choices appropriateness
           - Real future-proofing considerations

        6. **Overall Score** (0-100):
           - Weighted average of all scores
           - Actual project maturity assessment
           - Real production readiness
           - Actual maintenance requirements
           - Real business value delivered

        For each score, provide:
        - Detailed breakdown with sub-scores
        - Specific evidence from actual code
        - Real strengths and weaknesses
        - Concrete improvement suggestions with priority levels

        Be extremely strict and critical - this should be a thorough, honest evaluation.
        Reference actual files, functions, and implementation details.
        Respond with detailed JSON structure.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "strict_scoring": response,
                "real_metrics_used": real_metrics,
                "detailed_scores": self._parse_strict_scores(response),
                "honest_assessment": self._extract_honest_assessment(response),
                "strict_improvements": self._extract_strict_improvements(response)
            }
        except Exception as e:
            return {"error": f"Real strict scoring failed: {str(e)}"}
    
    def _calculate_real_scoring_metrics(self, code_analysis: Optional[Dict[str, Any]], project_files: Optional[List[str]]) -> Dict[str, Any]:
        """Calculate real metrics for scoring"""
        metrics = {
            "file_count": len(project_files) if project_files else 0,
            "total_functions": 0,
            "total_classes": 0,
            "lines_of_code": 0,
            "complexity_score": 0,
            "test_files": 0,
            "documentation_files": 0,
            "config_files": 0
        }
        
        if code_analysis and "files_analyzed" in code_analysis:
            for file_data in code_analysis["files_analyzed"]:
                if "functions" in file_data:
                    metrics["total_functions"] += len(file_data["functions"])
                if "classes" in file_data:
                    metrics["total_classes"] += len(file_data["classes"])
                if "lines_of_code" in file_data:
                    metrics["lines_of_code"] += file_data["lines_of_code"]
                if "complexity" in file_data:
                    metrics["complexity_score"] += file_data["complexity"]
        
        if project_files:
            for file_path in project_files:
                if 'test' in file_path.lower():
                    metrics["test_files"] += 1
                elif any(doc in file_path.lower() for doc in ['readme', 'doc', 'md']):
                    metrics["documentation_files"] += 1
                elif any(config in file_path.lower() for config in ['config', 'setting', 'env']):
                    metrics["config_files"] += 1
        
        return metrics
    
    def _parse_strict_scores(self, response: str) -> Dict[str, float]:
        """Parse strict scores from response"""
        scores = {
            'code_quality': 0.0,
            'functionality': 0.0,
            'documentation': 0.0,
            'innovation': 0.0,
            'architecture': 0.0,
            'overall': 0.0
        }
        
        score_patterns = {
            'code_quality': r'code quality.*?(\d+)',
            'functionality': r'functionality.*?(\d+)',
            'documentation': r'documentation.*?(\d+)',
            'innovation': r'innovation.*?(\d+)',
            'architecture': r'architecture.*?(\d+)',
            'overall': r'overall.*?(\d+)'
        }
        
        response_lower = response.lower()
        
        for category, pattern in score_patterns.items():
            match = re.search(pattern, response_lower)
            if match:
                try:
                    scores[category] = float(match.group(1))
                except:
                    scores[category] = 0.0
        
        return scores
    
    def _extract_honest_assessment(self, response: str) -> str:
        """Extract honest assessment from response"""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['overall', 'assessment', 'conclusion', 'summary']):
                return line.strip()
        return "No overall assessment found"
    
    def _extract_strict_improvements(self, response: str) -> List[str]:
        """Extract strict improvement suggestions from response"""
        improvements = []
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['improve', 'fix', 'address', 'resolve', 'correct']):
                improvements.append(line.strip())
        
        return improvements[:5]  # Top 5 strict improvements
    
    async def _implementation_review_real(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        project_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Perform real implementation review using actual code"""
        
        # Extract real implementation details
        real_implementation = self._extract_real_implementation_details(code_analysis, project_files)
        
        prompt = f"""
        Perform ultra-detailed implementation review of this ACTUAL code:

        REAL IMPLEMENTATION DATA:
        {json.dumps(real_implementation, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Project Files:
        {json.dumps(project_files, indent=2) if project_files else "No file list available"}

        CRITICAL: Review the ACTUAL implementation. Do not provide generic feedback.
        Focus on what's really implemented in the code.

        Provide comprehensive implementation review covering:

        1. **Real Code Structure Analysis**:
           - Actual file organization and module structure
           - Real class and function organization
           - Actual dependency management
           - Real code duplication analysis
           - Actual coupling and cohesion assessment

        2. **Actual Design Patterns Usage**:
           - Real design patterns identified in code
           - Actual pattern implementation quality
           - Missing pattern opportunities in this code
           - Real anti-patterns detected
           - Actual SOLID principles compliance

        3. **Real Performance Analysis**:
           - Actual algorithm efficiency in this code
           - Real memory usage patterns
           - Actual database query optimization
           - Real caching strategies implemented
           - Real scalability bottlenecks

        4. **Real Security Review**:
           - Actual input validation in this code
           - Real authentication and authorization
           - Actual data encryption
           - Real SQL injection prevention
           - Actual XSS protection
           - Real security headers

        5. **Real Error Handling**:
           - Actual exception handling strategies
           - Real error logging and monitoring
           - Real user-friendly error messages
           - Real recovery mechanisms
           - Real edge case coverage

        6. **Real Testing Strategy**:
           - Actual test coverage analysis
           - Real test quality assessment
           - Actual testing frameworks used
           - Real integration testing
           - Real performance testing

        For each area, provide:
        - Current implementation assessment based on actual code
        - Specific issues with file names and line numbers
        - Real improvement recommendations
        - Actual best practices compliance
        - Real risk assessment

        Reference actual functions, classes, and code patterns.
        Be extremely specific about what's implemented.
        Respond with detailed JSON structure.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "implementation_review": response,
                "real_implementation_data": real_implementation,
                "actual_issues_found": self._extract_actual_issues(response),
                "real_best_practices": self._extract_real_best_practices(response),
                "concrete_roadmap": self._extract_concrete_roadmap(response)
            }
        except Exception as e:
            return {"error": f"Real implementation review failed: {str(e)}"}
    
    def _extract_real_implementation_details(self, code_analysis: Optional[Dict[str, Any]], project_files: Optional[List[str]]) -> Dict[str, Any]:
        """Extract real implementation details"""
        details = {
            "file_structure": {},
            "functions_found": [],
            "classes_found": [],
            "imports_found": [],
            "patterns_detected": [],
            "issues_detected": []
        }
        
        if code_analysis and "files_analyzed" in code_analysis:
            for file_data in code_analysis["files_analyzed"]:
                file_name = file_data.get("file_name", "unknown")
                details["file_structure"][file_name] = {
                    "functions": file_data.get("functions", []),
                    "classes": file_data.get("classes", []),
                    "imports": file_data.get("imports", []),
                    "complexity": file_data.get("complexity", 0),
                    "lines": file_data.get("lines_of_code", 0)
                }
                
                details["functions_found"].extend(file_data.get("functions", []))
                details["classes_found"].extend(file_data.get("classes", []))
                details["imports_found"].extend(file_data.get("imports", []))
        
        return details
    
    def _extract_actual_issues(self, response: str) -> List[Dict[str, Any]]:
        """Extract actual issues from response"""
        issues = []
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['issue:', 'problem:', 'bug:', 'error:', 'flaw:']):
                issues.append({
                    "description": line.strip(),
                    "severity": self._determine_severity(line),
                    "category": self._determine_category(line),
                    "file_mentioned": self._extract_file_mention(line)
                })
        
        return issues[:15]  # Top 15 issues
    
    def _extract_real_best_practices(self, response: str) -> Dict[str, List[str]]:
        """Extract real best practices assessment from response"""
        practices = {
            "followed": [],
            "violated": [],
            "missing": []
        }
        
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['good:', 'well:', 'correctly:', 'properly:']):
                practices["followed"].append(line.strip())
            elif any(keyword in line.lower() for keyword in ['bad:', 'poor:', 'incorrectly:', 'violates:']):
                practices["violated"].append(line.strip())
            elif any(keyword in line.lower() for keyword in ['missing:', 'lacks:', 'should have:']):
                practices["missing"].append(line.strip())
        
        return practices
    
    def _extract_concrete_roadmap(self, response: str) -> List[Dict[str, Any]]:
        """Extract concrete improvement roadmap from response"""
        roadmap = []
        lines = response.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['improve:', 'enhance:', 'add:', 'implement:', 'fix:']):
                roadmap.append({
                    "step": i + 1,
                    "description": line.strip(),
                    "priority": self._determine_severity(line),
                    "effort": self._estimate_effort(line),
                    "category": self._determine_category(line)
                })
        
        return roadmap[:10]  # Top 10 improvements
    
    def _extract_file_mention(self, text: str) -> str:
        """Extract file mention from text"""
        import re
        file_patterns = [
            r'(\w+\.\w+)',
            r'(\w+\.\w+\.\w+)',
            r'(/[\w/]+/\w+\.\w+)'
        ]
        
        for pattern in file_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return ""
    
    async def _calculate_quality_metrics_real(
        self, 
        code_analysis: Optional[Dict[str, Any]], 
        report_analysis: Optional[Dict[str, Any]],
        project_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Calculate real quality metrics from actual code"""
        
        # Calculate real metrics
        real_metrics = self._calculate_real_quality_metrics(code_analysis, project_files)
        
        prompt = f"""
        Calculate comprehensive quality metrics for this ACTUAL project:

        REAL QUALITY METRICS:
        {json.dumps(real_metrics, indent=2)}
        
        Code Analysis Results:
        {json.dumps(code_analysis, indent=2) if code_analysis else "No code analysis available"}

        Report Analysis Results:
        {json.dumps(report_analysis, indent=2) if report_analysis else "No report analysis available"}

        Project Files:
        {json.dumps(project_files, indent=2) if project_files else "No file list available"}

        CRITICAL: Calculate metrics based on ACTUAL code, not theoretical values.
        Use the real data provided above.

        Provide detailed quality metrics covering:

        1. **Real Code Quality Metrics**:
           - Actual lines of code (total, effective, commented)
           - Real cyclomatic complexity averages
           - Actual code duplication percentage
           - Real function and class sizes
           - Actual nesting depth analysis
           - Real parameter counts

        2. **Real Maintainability Metrics**:
           - Actual maintainability index
           - Real technical debt estimation
           - Actual code churn analysis
           - Real coupling metrics
           - Real cohesion metrics
           - Actual modularity assessment

        3. **Real Test Quality Metrics**:
           - Actual test coverage percentage
           - Real test-to-code ratio
           - Actual test effectiveness
           - Real test complexity
           - Actual mock usage analysis
           - Real integration test coverage

        4. **Real Documentation Metrics**:
           - Actual documentation coverage
           - Real comment density
           - Actual API documentation completeness
           - Real README quality score
           - Actual inline documentation ratio

        5. **Real Security Metrics**:
           - Actual security vulnerabilities count
           - Real dependency security issues
           - Actual security test coverage
           - Real authentication implementation score
           - Actual data protection score

        6. **Real Performance Metrics**:
           - Actual response time estimates
           - Real memory usage patterns
           - Actual database efficiency
           - Real caching effectiveness
           - Actual resource utilization

        7. **Real Architecture Metrics**:
           - Actual component count and size
           - Real dependency depth
           - Actual interface complexity
           - Real pattern usage score
           - Real scalability metrics

        For each metric, provide:
        - Actual calculated value
        - Industry benchmark comparison
        - Quality assessment (excellent, good, fair, poor)
        - Real improvement target
        - Concrete action items

        Calculate overall quality score and health indicators based on real data.
        Respond with detailed JSON structure.
        """
        
        try:
            response = await self.ollama_service.generate_response(prompt)
            return {
                "quality_metrics": response,
                "real_metrics_calculated": real_metrics,
                "metric_breakdown": self._parse_quality_metrics_real(response),
                "real_benchmarks": self._extract_real_benchmarks(response),
                "health_indicators": self._extract_real_health_indicators(response)
            }
        except Exception as e:
            return {"error": f"Real quality metrics calculation failed: {str(e)}"}
    
    def _calculate_real_quality_metrics(self, code_analysis: Optional[Dict[str, Any]], project_files: Optional[List[str]]) -> Dict[str, Any]:
        """Calculate real quality metrics"""
        metrics = {
            "total_files": len(project_files) if project_files else 0,
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "avg_complexity": 0,
            "test_coverage": 0,
            "documentation_ratio": 0,
            "security_score": 0
        }
        
        if code_analysis and "files_analyzed" in code_analysis:
            total_complexity = 0
            file_count = 0
            
            for file_data in code_analysis["files_analyzed"]:
                if "lines_of_code" in file_data:
                    metrics["total_lines"] += file_data["lines_of_code"]
                if "functions" in file_data:
                    metrics["total_functions"] += len(file_data["functions"])
                if "classes" in file_data:
                    metrics["total_classes"] += len(file_data["classes"])
                if "complexity" in file_data:
                    total_complexity += file_data["complexity"]
                    file_count += 1
            
            if file_count > 0:
                metrics["avg_complexity"] = total_complexity / file_count
        
        if project_files:
            test_files = sum(1 for f in project_files if 'test' in f.lower())
            doc_files = sum(1 for f in project_files if any(doc in f.lower() for doc in ['readme', 'doc', 'md']))
            
            if metrics["total_files"] > 0:
                metrics["test_coverage"] = (test_files / metrics["total_files"]) * 100
                metrics["documentation_ratio"] = (doc_files / metrics["total_files"]) * 100
        
        return metrics
    
    def _parse_quality_metrics_real(self, response: str) -> Dict[str, Any]:
        """Parse real quality metrics from response"""
        metrics = {}
        
        # Look for numeric patterns in response
        import re
        number_patterns = re.findall(r'(\d+\.?\d*)', response)
        
        if number_patterns:
            metrics["numbers_found"] = [float(n) for n in number_patterns[:20]]  # First 20 numbers
            metrics["average"] = sum(metrics["numbers_found"]) / len(metrics["numbers_found"])
        
        return metrics
    
    def _extract_real_benchmarks(self, response: str) -> Dict[str, str]:
        """Extract real benchmark comparisons from response"""
        benchmarks = {}
        lines = response.split('\n')
        
        for line in lines:
            if 'benchmark' in line.lower() or 'compare' in line.lower() or 'industry' in line.lower():
                benchmarks['comparison'] = line.strip()
        
        return benchmarks
    
    def _extract_real_health_indicators(self, response: str) -> List[str]:
        """Extract real health indicators from response"""
        indicators = []
        lines = response.split('\n')
        
        for line in lines:
            if any(word in line.lower() for word in ['healthy', 'unhealthy', 'risk', 'warning', 'good', 'poor']):
                indicators.append(line.strip())
        
        return indicators[:10]  # Top 10 indicators
    
    def _determine_severity(self, text: str) -> str:
        """Determine severity from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['critical', 'severe', 'major', 'high']):
            return "critical"
        elif any(word in text_lower for word in ['moderate', 'medium', 'minor']):
            return "moderate"
        else:
            return "low"
    
    def _determine_category(self, text: str) -> str:
        """Determine category from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['security', 'auth', 'vulnerability']):
            return "security"
        elif any(word in text_lower for word in ['performance', 'speed', 'memory']):
            return "performance"
        elif any(word in text_lower for word in ['code', 'quality', 'style']):
            return "code_quality"
        elif any(word in text_lower for word in ['test', 'testing']):
            return "testing"
        elif any(word in text_lower for word in ['doc', 'documentation']):
            return "documentation"
        else:
            return "general"
    
    def _estimate_effort(self, text: str) -> str:
        """Estimate effort from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['easy', 'simple', 'quick']):
            return "low"
        elif any(word in text_lower for word in ['complex', 'difficult', 'hard']):
            return "high"
        else:
            return "medium"
    
    def _calculate_confidence_score(self, response: str) -> float:
        """Calculate confidence score based on response quality"""
        if not response:
            return 0.0
        
        # Simple heuristic based on response length and content
        score = min(100.0, len(response) / 10.0)
        
        # Boost score if it contains specific indicators
        if any(indicator in response.lower() for indicator in ['specific', 'actual', 'real', 'concrete']):
            score += 10.0
        
        # Reduce score if generic indicators
        if any(indicator in response.lower() for indicator in ['generic', 'template', 'example']):
            score -= 20.0
        
        return max(0.0, min(100.0, score))


# Create singleton instance
ultra_comprehensive_analyzer = UltraComprehensiveAnalyzer()
