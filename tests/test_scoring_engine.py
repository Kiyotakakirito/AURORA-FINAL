import pytest
import asyncio
from evaluation_engine.scoring_engine import ScoringEngine

class TestScoringEngine:
    def setup_method(self):
        self.engine = ScoringEngine()
    
    @pytest.mark.asyncio
    async def test_calculate_score_code_only(self):
        """Test scoring with code analysis only"""
        code_analysis = {
            'file_count': 5,
            'total_lines': 500,
            'code_quality_score': 80,
            'average_complexity': 5,
            'average_comment_ratio': 0.15,
            'total_functions': 10,
            'total_classes': 3
        }
        
        result = await self.engine.calculate_score(
            code_analysis=code_analysis,
            report_analysis=None,
            code_weight=1.0,
            report_weight=0.0
        )
        
        assert result['overall_score'] > 0
        assert result['overall_score'] <= 100
        assert result['max_score'] == 100
        assert result['code_score'] > 0
        assert result['report_score'] == 0
        assert 'grade' in result
        assert 'code_breakdown' in result
    
    @pytest.mark.asyncio
    async def test_calculate_score_report_only(self):
        """Test scoring with report analysis only"""
        report_analysis = {
            'page_count': 10,
            'word_count': 2000,
            'structure_analysis': {
                'has_title': True,
                'has_abstract': True,
                'has_introduction': True,
                'has_conclusion': True,
                'has_references': True
            },
            'content_analysis': {
                'technical_terms': [
                    {'term': 'algorithm', 'count': 5},
                    {'term': 'implementation', 'count': 3}
                ],
                'code_references': 8,
                'diagram_references': 4,
                'citation_count': 10,
                'readability_score': 75,
                'technical_depth': 80
            },
            'quality_metrics': {
                'structure_score': 90,
                'content_quality_score': 85,
                'completeness_score': 88,
                'overall_score': 87
            }
        }
        
        result = await self.engine.calculate_score(
            code_analysis=None,
            report_analysis=report_analysis,
            code_weight=0.0,
            report_weight=1.0
        )
        
        assert result['overall_score'] > 0
        assert result['overall_score'] <= 100
        assert result['code_score'] == 0
        assert result['report_score'] > 0
        assert 'grade' in result
        assert 'report_breakdown' in result
    
    @pytest.mark.asyncio
    async def test_calculate_score_mixed(self):
        """Test scoring with both code and report analysis"""
        code_analysis = {
            'file_count': 8,
            'total_lines': 800,
            'code_quality_score': 75,
            'average_complexity': 6,
            'average_comment_ratio': 0.12,
            'total_functions': 15,
            'total_classes': 5
        }
        
        report_analysis = {
            'page_count': 12,
            'word_count': 2500,
            'structure_analysis': {
                'has_title': True,
                'has_abstract': True,
                'has_introduction': True,
                'has_conclusion': True,
                'has_references': True
            },
            'content_analysis': {
                'technical_terms': [
                    {'term': 'algorithm', 'count': 8},
                    {'term': 'implementation', 'count': 6}
                ],
                'code_references': 12,
                'diagram_references': 6,
                'citation_count': 15,
                'readability_score': 70,
                'technical_depth': 75
            },
            'quality_metrics': {
                'structure_score': 85,
                'content_quality_score': 80,
                'completeness_score': 82,
                'overall_score': 82
            }
        }
        
        result = await self.engine.calculate_score(
            code_analysis=code_analysis,
            report_analysis=report_analysis,
            code_weight=0.7,
            report_weight=0.3
        )
        
        assert result['overall_score'] > 0
        assert result['overall_score'] <= 100
        assert result['code_score'] > 0
        assert result['report_score'] > 0
        # Weighted combination should be between individual scores
        assert result['overall_score'] == result['code_score'] * 0.7 + result['report_score'] * 0.3
    
    def test_calculate_grade(self):
        """Test grade calculation"""
        assert self.engine._calculate_grade(95, 100) == 'A'
        assert self.engine._calculate_grade(85, 100) == 'B'
        assert self.engine._calculate_grade(75, 100) == 'C'
        assert self.engine._calculate_grade(65, 100) == 'D'
        assert self.engine._calculate_grade(55, 100) == 'F'
    
    @pytest.mark.asyncio
    async def test_calculate_code_score(self):
        """Test detailed code scoring"""
        code_analysis = {
            'code_quality_score': 80,
            'average_comment_ratio': 0.15,
            'average_complexity': 5,
            'total_functions': 10,
            'total_classes': 3,
            'file_count': 5
        }
        
        score, breakdown = await self.engine._calculate_code_score(code_analysis, self.engine.default_weights)
        
        assert 0 <= score <= 100
        assert 'code_quality' in breakdown
        assert 'functionality' in breakdown
        assert 'documentation' in breakdown
        assert 'innovation' in breakdown
        
        # Check individual category scores
        assert 0 <= breakdown['code_quality']['score'] <= 30
        assert 0 <= breakdown['functionality']['score'] <= 40
        assert 0 <= breakdown['documentation']['score'] <= 20
        assert 0 <= breakdown['innovation']['score'] <= 10
    
    @pytest.mark.asyncio
    async def test_calculate_report_score(self):
        """Test detailed report scoring"""
        report_analysis = {
            'structure_analysis': {
                'has_title': True,
                'has_abstract': True,
                'has_introduction': True,
                'has_conclusion': True,
                'has_references': True
            },
            'content_analysis': {
                'technical_terms': [
                    {'term': 'algorithm', 'count': 5},
                    {'term': 'implementation', 'count': 3}
                ],
                'code_references': 8,
                'diagram_references': 4,
                'citation_count': 10,
                'readability_score': 75,
                'technical_depth': 80
            }
        }
        
        score, breakdown = await self.engine._calculate_report_score(report_analysis)
        
        assert 0 <= score <= 100
        assert 'structure' in breakdown
        assert 'content_quality' in breakdown
        assert 'completeness' in breakdown
        
        # Check individual category scores
        assert 0 <= breakdown['structure']['score'] <= 30
        assert 0 <= breakdown['content_quality']['score'] <= 40
        assert 0 <= breakdown['completeness']['score'] <= 30
    
    @pytest.mark.asyncio
    async def test_custom_criteria(self):
        """Test scoring with custom criteria"""
        custom_criteria = {
            'weights': {
                'code_quality': 0.4,
                'functionality': 0.3,
                'documentation': 0.2,
                'innovation': 0.1
            },
            'max_score': 50
        }
        
        code_analysis = {
            'file_count': 5,
            'total_lines': 500,
            'code_quality_score': 80,
            'average_complexity': 5,
            'average_comment_ratio': 0.15,
            'total_functions': 10,
            'total_classes': 3
        }
        
        result = await self.engine.calculate_score(
            code_analysis=code_analysis,
            report_analysis=None,
            criteria=custom_criteria,
            code_weight=1.0,
            report_weight=0.0
        )
        
        assert result['max_score'] == 50
        assert result['overall_score'] <= 50
    
    @pytest.mark.asyncio
    async def test_benchmark_score(self):
        """Test score benchmarking"""
        # Test excellent score
        result = await self.engine.benchmark_score(92, 100)
        assert result['level'] == 'excellent'
        assert result['percentile'] == 90
        
        # Test good score
        result = await self.engine.benchmark_score(85, 100)
        assert result['level'] == 'good'
        assert result['percentile'] == 70
        
        # Test average score
        result = await self.engine.benchmark_score(75, 100)
        assert result['level'] == 'average'
        assert result['percentile'] == 50
        
        # Test poor score
        result = await self.engine.benchmark_score(45, 100)
        assert result['level'] == 'poor'
        assert result['percentile'] == 10

if __name__ == '__main__':
    pytest.main([__file__])
