import pytest
import asyncio
import tempfile
import os
from evaluation_engine.pdf_processor import PDFProcessor

class TestPDFProcessor:
    def setup_method(self):
        self.processor = PDFProcessor()
    
    @pytest.mark.asyncio
    async def test_extract_text_from_pdf(self):
        """Test text extraction from PDF"""
        # This test would require a sample PDF file
        # For now, we'll test with a mock scenario
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_file = f.name
        
        try:
            # Since we can't create a real PDF easily, we'll test the error handling
            result = await self.processor._extract_text(temp_file)
            # Should return empty string or raise exception for invalid PDF
            assert isinstance(result, str)
            
        finally:
            os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_analyze_structure(self):
        """Test structure analysis"""
        text_content = '''
# My Project Report

## Abstract
This is the abstract of my project.

## Introduction
This is the introduction section.

## Methodology
This is the methodology section.

## Results
These are the results.

## Conclusion
This is the conclusion.

## References
1. Reference one
2. Reference two
'''
        
        structure = await self.processor._analyze_structure(text_content)
        
        assert structure['has_title'] == True
        assert structure['has_abstract'] == True
        assert structure['has_introduction'] == True
        assert structure['has_conclusion'] == True
        assert structure['has_references'] == True
        assert len(structure['headings']) > 0
        assert len(structure['sections']) > 0
    
    @pytest.mark.asyncio
    async def test_analyze_content(self):
        """Test content analysis"""
        text_content = '''
# Technical Project Report

This project uses advanced algorithms and data structures.
We implemented a machine learning model using TensorFlow.
The code follows object-oriented programming principles.

We included several code examples:
```python
def example():
    return "example"
```

The project includes multiple diagrams as shown in Figure 1 and Figure 2.
We referenced several papers (Smith, 2020; Johnson, 2021).
'''
        
        content = await self.processor._analyze_content(text_content)
        
        assert len(content['technical_terms']) > 0
        assert content['code_references'] > 0
        assert content['diagram_references'] > 0
        assert content['citation_count'] > 0
        assert content['readability_score'] >= 0
        assert content['technical_depth'] >= 0
    
    @pytest.mark.asyncio
    async def test_calculate_quality_metrics(self):
        """Test quality metrics calculation"""
        text_content = '''
# Comprehensive Project Report

## Abstract
This report describes a comprehensive software project.

## Introduction
The project addresses an important problem in software engineering.

## Methodology
We used agile development methodology with modern tools.

## Implementation
The implementation includes well-structured code with proper documentation.

## Results
The results demonstrate successful completion of project objectives.

## Conclusion
The project achieves its goals and provides valuable insights.

## References
1. Martin, R. (2017). Clean Code
2. Fowler, M. (2018). Refactoring
3. Beck, K. (2003). Test-Driven Development
'''
        
        metrics = await self.processor._calculate_quality_metrics(text_content)
        
        assert metrics['structure_score'] > 0
        assert metrics['content_quality_score'] > 0
        assert metrics['completeness_score'] > 0
        assert metrics['overall_score'] > 0
        assert 0 <= metrics['overall_score'] <= 100
    
    def test_get_page_count(self):
        """Test page count extraction"""
        # Test with non-existent file
        count = self.processor._get_page_count('non_existent.pdf')
        assert count == 0
    
    @pytest.mark.asyncio
    async def test_process_pdf_invalid_file(self):
        """Test processing of invalid PDF file"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            # Write invalid content
            f.write(b'This is not a PDF file')
            temp_file = f.name
        
        try:
            result = await self.processor.process_pdf(temp_file)
            # Should handle error gracefully
            assert 'error' in result
            
        finally:
            os.unlink(temp_file)

if __name__ == '__main__':
    pytest.main([__file__])
