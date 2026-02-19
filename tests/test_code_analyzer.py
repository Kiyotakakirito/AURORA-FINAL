import pytest
import asyncio
import tempfile
import os
from evaluation_engine.code_analyzer import CodeAnalyzer

class TestCodeAnalyzer:
    def setup_method(self):
        self.analyzer = CodeAnalyzer()
    
    @pytest.mark.asyncio
    async def test_analyze_python_code(self):
        """Test analysis of Python code"""
        # Create a temporary Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def hello_world():
    """A simple hello world function"""
    print("Hello, World!")
    return "Hello, World!"

class Calculator:
    """A simple calculator class"""
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
''')
            temp_file = f.name
        
        try:
            # Analyze the file
            result = await self.analyzer._analyze_file(temp_file)
            
            # Assertions
            assert result is not None
            assert result['language'] == 'python'
            assert result['function_count'] >= 1
            assert result['line_count'] > 0
            assert 'classes' in result
            assert len(result['classes']) >= 1
            assert result['has_docstring'] == True
            
        finally:
            os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_analyze_javascript_code(self):
        """Test analysis of JavaScript code"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write('''
function greet(name) {
    console.log(`Hello, ${name}!`);
    return `Hello, ${name}!`;
}

class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
    }
    
    getInfo() {
        return `${this.name} (${this.email})`;
    }
}
''')
            temp_file = f.name
        
        try:
            result = await self.analyzer._analyze_file(temp_file)
            
            assert result is not None
            assert result['language'] == 'javascript'
            assert result['function_count'] >= 1
            assert 'classes' in result
            assert len(result['classes']) >= 1
            
        finally:
            os.unlink(temp_file)
    
    def test_detect_language(self):
        """Test language detection from file extensions"""
        assert self.analyzer._detect_language('test.py') == 'python'
        assert self.analyzer._detect_language('test.js') == 'javascript'
        assert self.analyzer._detect_language('test.ts') == 'typescript'
        assert self.analyzer._detect_language('test.java') == 'java'
        assert self.analyzer._detect_language('test.cpp') == 'cpp'
        assert self.analyzer._detect_language('unknown.xyz') == 'unknown'
    
    def test_calculate_comment_ratio(self):
        """Test comment ratio calculation"""
        code_with_comments = '''
# This is a comment
def function():
    # Another comment
    pass
# Final comment
'''
        ratio = self.analyzer._calculate_comment_ratio(code_with_comments)
        assert ratio > 0.5  # Should be high due to many comments
        
        code_without_comments = '''
def function():
    pass
'''
        ratio = self.analyzer._calculate_comment_ratio(code_without_comments)
        assert ratio == 0.0  # No comments
    
    def test_count_functions(self):
        """Test function counting"""
        python_code = '''
def func1():
    pass

def func2():
    pass

class MyClass:
    def method1(self):
        pass
'''
        count = self.analyzer._count_functions(python_code, 'python')
        assert count == 3  # 2 functions + 1 method
        
        js_code = '''
function func1() {}
function func2() {}
const func3 = () => {};
'''
        count = self.analyzer._count_functions(js_code, 'javascript')
        assert count == 3
    
    def test_calculate_complexity(self):
        """Test cyclomatic complexity calculation"""
        simple_code = '''
def simple_function():
    return 42
'''
        complexity = self.analyzer._calculate_complexity(simple_code, 'python')
        assert complexity == 1  # Base complexity
        
        complex_code = '''
def complex_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                try:
                    result = i * 2
                except:
                    result = 0
            else:
                result = i
    else:
        result = 0
    return result
'''
        complexity = self.analyzer._calculate_complexity(complex_code, 'python')
        assert complexity > 5  # Should be higher due to control flow
    
    def test_calculate_quality_score(self):
        """Test quality score calculation"""
        # High quality
        score = self.analyzer._calculate_quality_score(0.2, 3)
        assert score >= 70
        
        # Low quality
        score = self.analyzer._calculate_quality_score(0.05, 15)
        assert score < 50

if __name__ == '__main__':
    pytest.main([__file__])
