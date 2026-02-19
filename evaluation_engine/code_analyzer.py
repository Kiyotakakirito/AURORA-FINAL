import os
import zipfile
import tempfile
import shutil
from typing import Dict, List, Any, Optional
from pathlib import Path
import subprocess
import json
from git import Repo
import ast
import re

class CodeAnalyzer:
    def __init__(self):
        self.supported_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala'
        }
    
    async def analyze_from_zip(self, zip_path: str) -> Dict[str, Any]:
        """Analyze code from a ZIP file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                return await self._analyze_directory(temp_dir)
            except Exception as e:
                return {"error": f"Failed to extract ZIP file: {str(e)}"}
    
    async def analyze_from_github(self, github_url: str) -> Dict[str, Any]:
        """Analyze code from a GitHub repository"""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                Repo.clone_from(github_url, temp_dir, depth=1)
                return await self._analyze_directory(temp_dir)
            except Exception as e:
                return {"error": f"Failed to clone repository: {str(e)}"}
    
    async def _analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze all code files in a directory"""
        code_files = self._find_code_files(directory)
        
        if not code_files:
            return {"error": "No supported code files found"}
        
        analysis_results = {
            "file_count": len(code_files),
            "languages": {},
            "total_lines": 0,
            "complexity_metrics": {},
            "code_quality": {},
            "structure_analysis": {},
            "files_analyzed": []
        }
        
        for file_path in code_files:
            file_analysis = await self._analyze_file(file_path)
            if file_analysis:
                analysis_results["files_analyzed"].append(file_analysis)
                analysis_results["total_lines"] += file_analysis.get("line_count", 0)
                
                # Track languages
                lang = file_analysis.get("language", "unknown")
                analysis_results["languages"][lang] = analysis_results["languages"].get(lang, 0) + 1
        
        # Calculate overall metrics
        analysis_results.update(await self._calculate_overall_metrics(analysis_results["files_analyzed"]))
        
        return analysis_results
    
    def _find_code_files(self, directory: str) -> List[str]:
        """Find all supported code files in directory"""
        code_files = []
        for root, dirs, files in os.walk(directory):
            # Skip common non-code directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv', 'env']]
            
            for file in files:
                if Path(file).suffix.lower() in self.supported_extensions:
                    code_files.append(os.path.join(root, file))
        
        return code_files
    
    async def _analyze_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze a single code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                return None
            
            language = self._detect_language(file_path)
            line_count = len(content.splitlines())
            
            analysis = {
                "file_path": file_path,
                "language": language,
                "line_count": line_count,
                "size_bytes": os.path.getsize(file_path)
            }
            
            # Language-specific analysis
            if language == "python":
                analysis.update(await self._analyze_python(content))
            elif language in ["javascript", "typescript"]:
                analysis.update(await self._analyze_javascript(content))
            elif language == "java":
                analysis.update(await self._analyze_java(content))
            
            # General analysis
            analysis.update({
                "comment_ratio": self._calculate_comment_ratio(content),
                "function_count": self._count_functions(content, language),
                "complexity_score": self._calculate_complexity(content, language)
            })
            
            return analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze {file_path}: {str(e)}"}
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala'
        }
        return language_map.get(ext, 'unknown')
    
    async def _analyze_python(self, content: str) -> Dict[str, Any]:
        """Analyze Python code"""
        try:
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line_count": node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0,
                        "args_count": len(node.args.args)
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(ast.unparse(node))
            
            return {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "has_docstring": ast.get_docstring(tree) is not None
            }
            
        except SyntaxError:
            return {"syntax_error": True}
    
    async def _analyze_javascript(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript code"""
        # Basic regex-based analysis for JS/TS
        functions = re.findall(r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))', content)
        classes = re.findall(r'class\s+(\w+)', content)
        imports = re.findall(r'import\s+.*from\s+[\'"][^\'"]+[\'"]', content)
        
        return {
            "functions": [f[0] or f[1] for f in functions if f[0] or f[1]],
            "classes": classes,
            "imports": imports,
            "has_comments": '//' in content or '/*' in content
        }
    
    async def _analyze_java(self, content: str) -> Dict[str, Any]:
        """Analyze Java code"""
        classes = re.findall(r'(?:public\s+|private\s+|protected\s+)?class\s+(\w+)', content)
        methods = re.findall(r'(?:public\s+|private\s+|protected\s+)?(?:static\s+)?(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*{', content)
        imports = re.findall(r'import\s+[^;]+;', content)
        
        return {
            "classes": classes,
            "methods": methods,
            "imports": imports,
            "has_package": re.search(r'package\s+[^;]+;', content) is not None
        }
    
    def _calculate_comment_ratio(self, content: str) -> float:
        """Calculate ratio of comments to total code"""
        lines = content.splitlines()
        comment_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if (stripped.startswith('//') or 
                stripped.startswith('#') or 
                stripped.startswith('/*') or 
                stripped.startswith('*') or
                stripped.startswith('<!--')):
                comment_lines += 1
        
        return comment_lines / len(lines) if lines else 0
    
    def _count_functions(self, content: str, language: str) -> int:
        """Count number of functions/methods"""
        if language == "python":
            return len(re.findall(r'def\s+\w+\s*\(', content))
        elif language in ["javascript", "typescript"]:
            return len(re.findall(r'function\s+\w+|\w+\s*=\s*(?:function|\([^)]*\)\s*=>)', content))
        elif language == "java":
            return len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*{', content))
        return 0
    
    def _calculate_complexity(self, content: str, language: str) -> int:
        """Calculate cyclomatic complexity"""
        # Count control flow statements
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'catch', 'try']
        complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            if language == "python":
                complexity += len(re.findall(r'\b' + keyword + r'\b', content))
            else:
                complexity += len(re.findall(r'\b' + keyword + r'\b', content, re.IGNORECASE))
        
        return complexity
    
    async def _calculate_overall_metrics(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall project metrics"""
        if not file_analyses:
            return {}
        
        total_functions = sum(f.get("function_count", 0) for f in file_analyses)
        total_classes = sum(len(f.get("classes", [])) for f in file_analyses)
        avg_complexity = sum(f.get("complexity_score", 0) for f in file_analyses) / len(file_analyses)
        avg_comment_ratio = sum(f.get("comment_ratio", 0) for f in file_analyses) / len(file_analyses)
        
        return {
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": avg_complexity,
            "average_comment_ratio": avg_comment_ratio,
            "code_quality_score": self._calculate_quality_score(avg_comment_ratio, avg_complexity)
        }
    
    def _calculate_quality_score(self, comment_ratio: float, complexity: float) -> float:
        """Calculate overall code quality score (0-100)"""
        # Higher comment ratio and lower complexity = better quality
        comment_score = min(comment_ratio * 100, 30)  # Max 30 points for comments
        complexity_score = max(0, 40 - (complexity * 2))  # Max 40 points for low complexity
        structure_score = 30  # Base points for having structure
        
        return min(comment_score + complexity_score + structure_score, 100)
