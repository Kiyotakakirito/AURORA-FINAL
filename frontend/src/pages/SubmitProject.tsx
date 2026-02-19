import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';

export const SubmitProject: React.FC = () => {
  const [submissionType, setSubmissionType] = useState<'github'>('github');
  const [formData, setFormData] = useState({
    name: '',
    studentName: '',
    studentEmail: '',
    githubUrl: ''
  });
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [evaluationResult, setEvaluationResult] = useState<any>(null);

  const { getRootProps: getRootPropsPdf, getInputProps: getInputPropsPdf, isDragActive: isDragActivePdf } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setPdfFile(acceptedFiles[0]);
      }
    },
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024 // 10MB limit
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const formatAnalysisData = (data: any) => {
    if (!data || !data.comprehensive_analysis) return null;
    
    const analysis = data.comprehensive_analysis.ultra_detailed_analysis;
    return {
      projectEssence: analysis.project_essence,
      lineByLineAnalysis: analysis.line_by_line_analysis,
      techStackAnalysis: analysis.tech_stack_analysis,
      pdfProjectMatching: analysis.pdf_project_matching,
      strictScoring: analysis.strict_scoring,
      implementationReview: analysis.implementation_review,
      qualityMetrics: analysis.quality_metrics,
      overallScore: data.overall_score || 0,
      analysisTimestamp: data.comprehensive_analysis.analysis_timestamp,
      analysisModel: data.comprehensive_analysis.analysis_model
    };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!pdfFile) {
      setSubmitStatus('error');
      return;
    }

    if (!formData.githubUrl) {
      setSubmitStatus('error');
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus('idle');
    setEvaluationResult(null);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('student_name', formData.studentName);
      formDataToSend.append('student_email', formData.studentEmail);
      formDataToSend.append('submission_type', 'github');
      formDataToSend.append('github_url', formData.githubUrl);
      
      // Always send PDF file (required)
      if (pdfFile) {
        formDataToSend.append('pdf_file', pdfFile);
      }

      // Use faster enhanced endpoint with 5 minute timeout for AI analysis
      const response = await fetch('http://localhost:8000/api/v1/submit-fast/', {
        method: 'POST',
        body: formDataToSend,
        signal: AbortSignal.timeout(300000) // 5 minute timeout for AI analysis with Ollama
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend error:', response.status, errorText);
        throw new Error(`Failed to submit project: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      setEvaluationResult(result);
      setSubmitStatus('success');
    } catch (err: any) {
      console.error('Full submission error:', err);
      console.error('Error name:', err.name);
      console.error('Error message:', err.message);
      if (err.name === 'AbortError' || err.name === 'TimeoutError') {
        console.error('Request timed out - AI analysis is taking longer than expected');
        alert('Analysis is taking longer than expected. Please try again or wait a moment before retrying.');
        setSubmitStatus('error');
      } else {
        console.error('Form data being sent:', {
          name: formData.name,
          student_name: formData.studentName,
          student_email: formData.studentEmail,
          submission_type: 'github',
          github_url: formData.githubUrl,
          pdf_file: pdfFile?.name
        });
        setSubmitStatus('error');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-deep-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="aurora-card rounded-xl p-8 shadow-glow-cyan">
          <div className="flex items-center justify-center mb-8">
            <img src="/aurora-logo.png" alt="AURORA" className="h-10 w-auto mr-3" />
            <h1 className="text-3xl font-bold text-white aurora-text-glow">Submit Your Project</h1>
          </div>
          
          {submitStatus === 'success' && (
            <div className="mb-6 p-4 bg-aurora-800/50 border border-glow-teal/30 rounded-lg">
              <div className="flex items-center">
                <CheckCircle className="text-glow-green mr-2" size={20} />
                <span className="text-glow-green font-medium">Project submitted successfully!</span>
              </div>
            </div>
          )}

          {submitStatus === 'error' && (
            <div className="mb-6 p-4 bg-red-900/30 border border-red-500/30 rounded-lg">
              <div className="flex items-center">
                <AlertCircle className="text-red-400 mr-2" size={20} />
                <span className="text-red-300">Submission failed. Please try again.</span>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-aurora-100 mb-2">
                  Project Name
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 aurora-input rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-aurora-100 mb-2">
                  Student Name
                </label>
                <input
                  type="text"
                  name="studentName"
                  value={formData.studentName}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 aurora-input rounded-lg"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-aurora-100 mb-2">
                Student Email
              </label>
              <input
                type="email"
                name="studentEmail"
                value={formData.studentEmail}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 aurora-input rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-aurora-100 mb-2">
                GitHub Repository URL
              </label>
              <input
                type="url"
                name="githubUrl"
                value={formData.githubUrl}
                onChange={handleInputChange}
                placeholder="https://github.com/username/repository"
                required
                className="w-full px-3 py-2 aurora-input rounded-lg"
              />
              <p className="text-sm text-aurora-300 mt-2">
                Provide the URL to your GitHub repository
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-aurora-100 mb-2">
                PDF Report (Required)
              </label>
              <div
                {...getRootPropsPdf()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
                  isDragActivePdf ? 'border-glow-cyan bg-aurora-800/50' : 'border-aurora-600 hover:border-glow-teal'
                }`}
              >
                <input {...getInputPropsPdf()} />
                <FileText className="mx-auto mb-4 text-glow-cyan" size={48} />
                {isDragActivePdf ? (
                  <p className="text-glow-cyan">Drop the PDF file here...</p>
                ) : (
                  <div>
                    <p className="text-aurora-100">Drag and drop your PDF report here, or click to select</p>
                    <p className="text-sm text-aurora-300 mt-2">Maximum file size: 10MB</p>
                  </div>
                )}
                {pdfFile && (
                  <p className="mt-4 text-sm text-glow-green">
                    Selected: {pdfFile.name}
                  </p>
                )}
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full aurora-button py-3 px-4 rounded-lg"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Project'}
            </button>
          </form>

          {/* Display 5 Key Features Analysis Results */}
          {evaluationResult && evaluationResult.comprehensive_analysis && (
            <div className="mt-12 space-y-8">
              <div className="text-center mb-8">
                <div className="flex items-center justify-center mb-4">
                  <img src="/aurora-logo.png" alt="AURORA" className="h-10 w-auto mr-3" />
                  <h2 className="text-3xl font-bold text-white aurora-text-glow">
                    AI-Powered Project Evaluation
                  </h2>
                </div>
                <p className="text-aurora-300">
                  {evaluationResult.comprehensive_analysis.project_summary}
                </p>
              </div>

              {/* Project Description and Analysis Summary */}
              {evaluationResult.comprehensive_analysis.project_description && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-teal mb-8">
                  <h3 className="text-xl font-bold text-glow-cyan mb-4">📋 Project Analysis Summary</h3>
                  
                  {/* Project Description */}
                  <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30 mb-4">
                    <h4 className="font-bold text-glow-teal mb-2">📁 Project Overview</h4>
                    <p className="text-aurora-100 leading-relaxed">
                      {evaluationResult.comprehensive_analysis.project_description}
                    </p>
                  </div>

                  {/* Project Purpose */}
                  {evaluationResult.comprehensive_analysis.project_purpose && (
                    <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30 mb-4">
                      <h4 className="font-bold text-glow-teal mb-2">🎯 What This Project Does</h4>
                      <p className="text-aurora-200 text-sm leading-relaxed">
                        {evaluationResult.comprehensive_analysis.project_purpose}
                      </p>
                    </div>
                  )}
                  
                  {/* PDF Abstract */}
                  {evaluationResult.comprehensive_analysis.pdf_abstract && (
                    <div className="mt-4 p-4 bg-aurora-800/50 rounded-lg border border-aurora-500/30">
                      <h4 className="font-bold text-glow-green mb-2">📝 PDF Abstract / Summary</h4>
                      <p className="text-aurora-200 text-sm leading-relaxed italic">
                        "{evaluationResult.comprehensive_analysis.pdf_abstract}"
                      </p>
                    </div>
                  )}
                  
                  {/* PDF Content Summary */}
                  {evaluationResult.comprehensive_analysis.pdf_content_summary && (
                    <div className="mt-4 p-4 bg-aurora-900/50 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-teal mb-2">📄 PDF Report Summary</h4>
                      <p className="text-aurora-200 text-sm">
                        {evaluationResult.comprehensive_analysis.pdf_content_summary}
                      </p>
                    </div>
                  )}
                  
                  {/* Main Project Files */}
                  {evaluationResult.comprehensive_analysis.main_project_files && (
                    <div className="mt-4 p-4 bg-aurora-900/50 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-teal mb-2">🗂️ Main Project Files</h4>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                        {evaluationResult.comprehensive_analysis.main_project_files.map((file: string, index: number) => (
                          <div key={index} className="flex items-center space-x-2 p-2 bg-aurora-800/50 rounded border border-aurora-600/30">
                            <span className="text-xs text-aurora-300">#{index + 1}</span>
                            <span className="text-sm font-medium text-aurora-100 truncate">{file}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Real Data Summary from GitHub/PDF Analysis */}
              {evaluationResult.comprehensive_analysis.real_data_summary && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-cyan mb-8">
                  <h3 className="text-xl font-bold text-glow-cyan mb-4">📊 Real Analysis Data from Your Submission</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Code Analysis Summary */}
                    <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-teal mb-2">📝 Code Analysis (GitHub)</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-aurora-200">Files Analyzed:</span>
                          <span className="font-semibold text-glow-cyan">{evaluationResult.comprehensive_analysis.real_data_summary.files_analyzed_count}</span>
                        </div>
                        {evaluationResult.comprehensive_analysis.real_data_summary.code_metrics?.lines_of_code > 0 && (
                          <div className="flex justify-between">
                            <span className="text-aurora-200">Lines of Code:</span>
                            <span className="font-semibold text-glow-cyan">{evaluationResult.comprehensive_analysis.real_data_summary.code_metrics.lines_of_code}</span>
                          </div>
                        )}
                        {evaluationResult.comprehensive_analysis.real_data_summary.code_metrics?.complexity && (
                          <div className="flex justify-between">
                            <span className="text-aurora-200">Complexity:</span>
                            <span className="font-semibold text-glow-teal capitalize">{evaluationResult.comprehensive_analysis.real_data_summary.code_metrics.complexity}</span>
                          </div>
                        )}
                        <div className="mt-3">
                          <span className="text-aurora-200">Technologies Detected:</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {evaluationResult.comprehensive_analysis.real_data_summary.technologies_detected?.map((tech: string, index: number) => (
                              <span key={index} className="px-2 py-1 bg-aurora-700/50 text-glow-cyan rounded text-xs border border-aurora-500/30">{tech}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* PDF Analysis Summary */}
                    {evaluationResult.comprehensive_analysis.real_data_summary.pdf_metrics?.text_extracted && (
                      <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                        <h4 className="font-bold text-glow-teal mb-2">📄 PDF Report Analysis</h4>
                        <div className="space-y-2 text-sm">
                          {evaluationResult.comprehensive_analysis.real_data_summary.pdf_metrics?.page_count > 0 && (
                            <div className="flex justify-between">
                              <span className="text-aurora-200">Pages:</span>
                              <span className="font-semibold text-glow-green">{evaluationResult.comprehensive_analysis.real_data_summary.pdf_metrics.page_count}</span>
                            </div>
                          )}
                          {evaluationResult.comprehensive_analysis.real_data_summary.pdf_metrics?.word_count > 0 && (
                            <div className="flex justify-between">
                              <span className="text-aurora-200">Word Count:</span>
                              <span className="font-semibold text-glow-green">{evaluationResult.comprehensive_analysis.real_data_summary.pdf_metrics.word_count}</span>
                            </div>
                          )}
                          <div className="flex justify-between">
                            <span className="text-aurora-200">Status:</span>
                            <span className="font-semibold text-glow-green">✓ Analyzed</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  {evaluationResult.comprehensive_analysis.real_data_summary.github_url && (
                    <div className="mt-4 p-3 bg-aurora-800/50 rounded text-sm border border-aurora-600/30">
                      <span className="font-medium text-glow-teal">Repository: </span>
                      <a href={evaluationResult.comprehensive_analysis.real_data_summary.github_url} target="_blank" rel="noopener noreferrer" className="text-glow-cyan hover:underline">
                        {evaluationResult.comprehensive_analysis.real_data_summary.github_url}
                      </a>
                    </div>
                  )}
                </div>
              )}

              {/* Feature 1: High-Accuracy Automated Evaluation Engine */}
              {evaluationResult.comprehensive_analysis.features?.["1_high_accuracy_evaluation"] && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-cyan border-t-4 border-feature-1">
                  <h3 className="text-xl font-bold text-feature-1 mb-4">
                    {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].title}
                  </h3>
                  <p className="text-aurora-200 mb-4">
                    {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].description}
                  </p>
                  {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].detailed_explanation && (
                    <div className="mt-3 p-3 bg-aurora-900/50 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-cyan mb-2">🔍 How It Works</h4>
                      <p className="text-aurora-200 text-sm leading-relaxed">
                        {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].detailed_explanation}
                      </p>
                    </div>
                  )}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div className="bg-aurora-800/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-2xl font-bold text-feature-1">
                        {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].accuracy_metrics?.overall_correlation}%
                      </div>
                      <div className="text-sm text-aurora-300">Overall Correlation</div>
                    </div>
                    <div className="bg-aurora-800/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-2xl font-bold text-glow-green">
                        {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].accuracy_metrics?.code_quality_correlation}%
                      </div>
                      <div className="text-sm text-aurora-300">Code Quality</div>
                    </div>
                    <div className="bg-aurora-800/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-2xl font-bold text-purple-400">
                        {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].accuracy_metrics?.documentation_correlation}%
                      </div>
                      <div className="text-sm text-aurora-300">Documentation</div>
                    </div>
                    <div className="bg-aurora-800/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-2xl font-bold text-orange-400">
                        {evaluationResult.comprehensive_analysis.features["1_high_accuracy_evaluation"].accuracy_metrics?.functionality_correlation}%
                      </div>
                      <div className="text-sm text-aurora-300">Functionality</div>
                    </div>
                  </div>
                </div>
              )}

              {/* Feature 2: Evaluation Time Reduction */}
              {evaluationResult.comprehensive_analysis.features?.["2_evaluation_time_reduction"] && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-teal border-t-4 border-feature-2">
                  <h3 className="text-xl font-bold text-feature-2 mb-4">
                    {evaluationResult.comprehensive_analysis.features["2_evaluation_time_reduction"].title}
                  </h3>
                  <p className="text-aurora-200 mb-4">
                    {evaluationResult.comprehensive_analysis.features["2_evaluation_time_reduction"].description}
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="bg-aurora-800/50 p-4 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-3xl font-bold text-feature-2">
                        {evaluationResult.comprehensive_analysis.features["2_evaluation_time_reduction"].time_saved_percentage}%
                      </div>
                      <div className="text-sm text-aurora-300">Time Saved</div>
                    </div>
                    <div className="bg-aurora-800/50 p-4 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-lg font-bold text-aurora-100">
                        {evaluationResult.comprehensive_analysis.features["2_evaluation_time_reduction"].traditional_evaluation_time}
                      </div>
                      <div className="text-sm text-aurora-300">Traditional Time</div>
                    </div>
                    <div className="bg-aurora-800/50 p-4 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-lg font-bold text-glow-green">
                        {evaluationResult.comprehensive_analysis.features["2_evaluation_time_reduction"].ai_evaluation_time}
                      </div>
                      <div className="text-sm text-aurora-300">AI Evaluation Time</div>
                    </div>
                  </div>
                </div>
              )}

              {/* Feature 3: Explainable Rubric Dashboard */}
              {evaluationResult.comprehensive_analysis.features?.["3_explainable_rubric_dashboard"] && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-cyan border-t-4 border-feature-3">
                  <h3 className="text-xl font-bold text-feature-3 mb-4">
                    {evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].title}
                  </h3>
                  <p className="text-aurora-200 mb-4">
                    {evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].description}
                  </p>
                  
                  {/* Weight Explanation */}
                  <div className="mb-4 p-3 bg-aurora-900/50 rounded-lg border border-aurora-600/30">
                    <h4 className="font-bold text-glow-cyan mb-1">ℹ️ What does "Weight" mean?</h4>
                    <p className="text-aurora-200 text-sm">
                      <strong>Weight</strong> shows how much each category contributes to your final score. 
                      Each category (Code Quality, Functionality, Documentation, Innovation) has a 25% weight, 
                      meaning they all count equally toward your total score. For example: if you score 80 in Code Quality 
                      (weight 25%), it contributes 20 points (80 × 0.25) to your final score.
                    </p>
                  </div>
                  
                  {/* Overall Score */}
                  <div className="bg-aurora-800/50 p-4 rounded-lg mb-4 border border-aurora-600/30">
                    <div className="text-center">
                      <span className="text-aurora-300">Overall Score</span>
                      <div className="text-4xl font-bold text-feature-3">
                        {Math.round(evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].overall_score)} / {evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].max_score}
                      </div>
                    </div>
                  </div>

                  {/* Score Breakdown */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].score_breakdown || {}).map(([key, value]: [string, any]) => (
                      <div key={key} className="bg-aurora-900/50 p-3 rounded-lg border border-aurora-600/30">
                        <div className="text-lg font-bold text-feature-3 capitalize">{key.replace('_', ' ')}</div>
                        <div className="text-2xl font-bold text-aurora-100">{Math.round(value.score)}</div>
                        <div className="text-sm text-aurora-300">Weight: {value.weight}</div>
                      </div>
                    ))}
                  </div>

                  {/* Improvement Suggestions */}
                  {evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].improvement_suggestions && (
                    <div className="mt-4 bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-teal mb-2">💡 Improvement Suggestions</h4>
                      <ul className="space-y-1">
                        {evaluationResult.comprehensive_analysis.features["3_explainable_rubric_dashboard"].improvement_suggestions.map((suggestion: string, index: number) => (
                          <li key={index} className="text-aurora-200 text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Feature 4: Plagiarism & AI Detection */}
              {evaluationResult.comprehensive_analysis.features?.["4_plagiarism_detection"] && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-cyan border-t-4 border-feature-4">
                  <h3 className="text-xl font-bold text-feature-4 mb-4">
                    {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].title}
                  </h3>
                  <p className="text-aurora-200 mb-4">
                    {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].description}
                  </p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Code Plagiarism */}
                    <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-cyan mb-2">📝 Code Plagiarism Check</h4>
                      <div className="text-2xl font-bold text-glow-green">
                        {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].code_plagiarism_check?.similarity_score}%
                      </div>
                      <div className="text-sm text-aurora-300">Similarity Score</div>
                      <div className="mt-2 text-sm text-glow-green font-medium">
                        {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].code_plagiarism_check?.result}
                      </div>
                      {/* Explanation */}
                      {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].code_plagiarism_check?.explanation && (
                        <div className="mt-3 p-3 bg-aurora-800/50 rounded-lg border border-aurora-600/30">
                          <h5 className="font-bold text-glow-cyan text-xs mb-1">ℹ️ Why this score?</h5>
                          <p className="text-aurora-200 text-xs leading-relaxed">
                            {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].code_plagiarism_check?.explanation}
                          </p>
                        </div>
                      )}
                      {/* Additional Stats */}
                      <div className="mt-2 text-xs text-aurora-400">
                        Files checked: {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].code_plagiarism_check?.files_checked} | 
                        Lines: {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].code_plagiarism_check?.total_lines_analyzed}
                      </div>
                    </div>

                    {/* Report Plagiarism */}
                    <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-cyan mb-2">📄 Report Plagiarism Check</h4>
                      <div className="text-2xl font-bold text-glow-green">
                        {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].report_plagiarism_check?.similarity_score}%
                      </div>
                      <div className="text-sm text-aurora-300">Similarity Score</div>
                      <div className="mt-2 text-sm text-glow-green font-medium">
                        {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].report_plagiarism_check?.result}
                      </div>
                      {/* Explanation */}
                      {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].report_plagiarism_check?.explanation && (
                        <div className="mt-3 p-3 bg-aurora-800/50 rounded-lg border border-aurora-600/30">
                          <h5 className="font-bold text-glow-cyan text-xs mb-1">ℹ️ Why this score?</h5>
                          <p className="text-aurora-200 text-xs leading-relaxed">
                            {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].report_plagiarism_check?.explanation}
                          </p>
                        </div>
                      )}
                      {/* Additional Stats */}
                      <div className="mt-2 text-xs text-aurora-400">
                        Pages: {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].report_plagiarism_check?.pages_analyzed} | 
                        Words: {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].report_plagiarism_check?.word_count}
                      </div>
                    </div>

                    {/* AI Detection */}
                    <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-cyan mb-2">🤖 AI Content Detection</h4>
                      <div className="text-2xl font-bold text-feature-4">
                        {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].ai_generated_detection?.ai_probability}%
                      </div>
                      <div className="text-sm text-aurora-300">AI Probability</div>
                      <div className="mt-2 text-sm text-glow-green font-medium">
                        {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].ai_generated_detection?.result}
                      </div>
                      {/* Explanation */}
                      {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].ai_generated_detection?.explanation && (
                        <div className="mt-3 p-3 bg-aurora-800/50 rounded-lg border border-aurora-600/30">
                          <h5 className="font-bold text-glow-cyan text-xs mb-1">ℹ️ Why this score?</h5>
                          <p className="text-aurora-200 text-xs leading-relaxed">
                            {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].ai_generated_detection?.explanation}
                          </p>
                        </div>
                      )}
                      {/* Indicators */}
                      {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].ai_generated_detection?.indicators && (
                        <div className="mt-2">
                          <h5 className="font-bold text-aurora-300 text-xs mb-1">📊 Indicators:</h5>
                          <ul className="text-xs text-aurora-400 space-y-1">
                            {evaluationResult.comprehensive_analysis.features["4_plagiarism_detection"].ai_generated_detection?.indicators?.slice(0, 3).map((indicator: string, idx: number) => (
                              <li key={idx} className="flex items-center">
                                <span className="text-glow-green mr-1">✓</span> {indicator}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Feature 5: Scalable Prototype */}
              {evaluationResult.comprehensive_analysis.features?.["5_scalable_prototype"] && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-cyan border-t-4 border-feature-5">
                  <h3 className="text-xl font-bold text-feature-5 mb-4">
                    {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].title}
                  </h3>
                  <p className="text-aurora-200 mb-4">
                    {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].description}
                  </p>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div className="bg-aurora-900/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-xl font-bold text-glow-teal">Backend</div>
                      <div className="text-sm text-aurora-300">
                        {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].architecture?.backend}
                      </div>
                    </div>
                    <div className="bg-aurora-900/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-xl font-bold text-glow-teal">Frontend</div>
                      <div className="text-sm text-aurora-300">
                        {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].architecture?.frontend}
                      </div>
                    </div>
                    <div className="bg-aurora-900/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-xl font-bold text-glow-teal">Database</div>
                      <div className="text-sm text-aurora-300">
                        {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].architecture?.database}
                      </div>
                    </div>
                    <div className="bg-aurora-900/50 p-3 rounded-lg text-center border border-aurora-600/30">
                      <div className="text-xl font-bold text-glow-teal">AI Engine</div>
                      <div className="text-sm text-aurora-300">
                        {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].architecture?.ai_engine}
                      </div>
                    </div>
                  </div>

                  {/* Pilot Validation */}
                  {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].pilot_validation && (
                    <div className="bg-aurora-900/50 p-4 rounded-lg border border-aurora-600/30">
                      <h4 className="font-bold text-glow-teal mb-2">📊 Pilot Validation Results</h4>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-glow-cyan">
                            {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].pilot_validation.test_projects}
                          </div>
                          <div className="text-sm text-aurora-300">Test Projects</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-glow-cyan">
                            {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].pilot_validation.success_rate}%
                          </div>
                          <div className="text-sm text-aurora-300">Success Rate</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-glow-cyan">
                            {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].pilot_validation.faculty_satisfaction}
                          </div>
                          <div className="text-sm text-aurora-300">Faculty Satisfaction</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-glow-cyan">
                            {evaluationResult.comprehensive_analysis.features["5_scalable_prototype"].pilot_validation.departments?.length}
                          </div>
                          <div className="text-sm text-aurora-300">Departments</div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Submission Details */}
              {evaluationResult.comprehensive_analysis.submission_details && (
                <div className="aurora-card rounded-xl p-6 shadow-glow-cyan">
                  <h3 className="text-lg font-bold text-glow-cyan mb-4">📋 Submission Details</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-aurora-300">Project:</span>
                      <p className="text-aurora-100">{evaluationResult.comprehensive_analysis.submission_details.project_name}</p>
                    </div>
                    <div>
                      <span className="font-medium text-aurora-300">Student:</span>
                      <p className="text-aurora-100">{evaluationResult.comprehensive_analysis.submission_details.student_name}</p>
                    </div>
                    <div>
                      <span className="font-medium text-aurora-300">Type:</span>
                      <p className="text-aurora-100">{evaluationResult.comprehensive_analysis.submission_details.submission_type}</p>
                    </div>
                    <div>
                      <span className="font-medium text-aurora-300">Evaluation Time:</span>
                      <p className="text-aurora-100">{evaluationResult.comprehensive_analysis.evaluation_time_seconds}s</p>
                    </div>
                    <div>
                      <span className="font-medium text-aurora-300">Date:</span>
                      <p className="text-aurora-100">{new Date(evaluationResult.comprehensive_analysis.submission_details.evaluation_date).toLocaleString()}</p>
                    </div>
                    <div>
                      <span className="font-medium text-aurora-300">PDF Processed:</span>
                      <p className="text-aurora-100">{evaluationResult.comprehensive_analysis.submission_details.pdf_processed ? 'Yes' : 'No'}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
