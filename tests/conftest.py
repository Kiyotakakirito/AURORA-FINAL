import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_python_code():
    """Sample Python code for testing"""
    return '''
def fibonacci(n):
    """Calculate Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class MathUtils:
    """Utility class for mathematical operations"""
    
    @staticmethod
    def factorial(n):
        """Calculate factorial"""
        if n <= 1:
            return 1
        return n * MathUtils.factorial(n-1)
    
    def is_prime(self, n):
        """Check if number is prime"""
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
'''

@pytest.fixture
def sample_javascript_code():
    """Sample JavaScript code for testing"""
    return '''
function calculateSum(arr) {
    return arr.reduce((sum, num) => sum + num, 0);
}

class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    greet() {
        return `Hello, my name is ${this.name} and I'm ${this.age} years old.`;
    }
    
    static createAdult(name) {
        return new Person(name, 18);
    }
}

const utils = {
    formatCurrency: (amount) => `$${amount.toFixed(2)}`,
    validateEmail: (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
};
'''

@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for testing"""
    return '''
# Advanced Software Engineering Project

## Abstract
This project demonstrates advanced software engineering principles through the implementation of a comprehensive web application. The system incorporates modern architectural patterns, robust error handling, and comprehensive testing strategies.

## Introduction
In today's digital landscape, scalable and maintainable software solutions are paramount. This project addresses the challenge of building a production-ready application that can handle concurrent users while maintaining data integrity and performance standards.

## Methodology
We employed an agile development methodology with two-week sprints. The technology stack includes:
- Backend: Node.js with Express framework
- Database: PostgreSQL with Redis for caching
- Frontend: React with TypeScript
- Testing: Jest for unit tests, Cypress for E2E testing

## Implementation
The implementation follows a microservices architecture with the following key components:

### Authentication Service
Handles user authentication and authorization using JWT tokens with refresh token rotation.

### Data Processing Service
Implements complex data transformation algorithms with O(n log n) complexity optimization.

### API Gateway
Provides a unified entry point with rate limiting and request validation.

```python
# Example of data processing algorithm
def process_data(data_points):
    """
    Process data points with optimized algorithm
    Time complexity: O(n log n)
    Space complexity: O(1)
    """
    if not data_points:
        return []
    
    # Sort and process with binary search optimization
    sorted_points = sorted(data_points)
    return [optimize_point(p) for p in sorted_points]
```

## Results
The system successfully handles 10,000 concurrent users with an average response time of 150ms. Key performance metrics:
- Throughput: 5,000 requests/second
- Memory usage: 512MB under load
- CPU utilization: 75% peak
- Error rate: < 0.1%

## Conclusion
This project demonstrates the successful application of advanced software engineering principles. The modular architecture allows for easy maintenance and scaling. Future enhancements include implementing GraphQL API and adding machine learning capabilities for predictive analytics.

## References
1. Martin, R. (2017). "Clean Architecture: A Craftsman's Guide". Pearson Education.
2. Fowler, M. (2018). "Refactoring: Improving the Design of Existing Code". Addison-Wesley.
3. Newman, S. (2021). "Building Microservices: Designing Fine-Grained Systems". O'Reilly Media.
4. Fowler, M. (2003). "Patterns of Enterprise Application Architecture". Addison-Wesley.
5. Gamma, E. et al. (1994). "Design Patterns: Elements of Reusable Object-Oriented Software". Addison-Wesley.
'''
