import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { LandingPage } from './pages/LandingPage';
import { Dashboard } from './pages/Dashboard';
import { SubmitProject } from './pages/SubmitProject';
import { EvaluationHistory } from './pages/EvaluationHistory';
import { EvaluationDetail } from './pages/EvaluationDetail';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing page - no sidebar layout */}
        <Route path="/" element={<LandingPage />} />

        {/* App pages - with sidebar layout */}
        <Route
          path="/*"
          element={
            <Layout>
              <Routes>
                <Route path="/dashboard"          element={<Dashboard />} />
                <Route path="/submit"             element={<SubmitProject />} />
                <Route path="/history"            element={<EvaluationHistory />} />
                <Route path="/evaluations/:id"    element={<EvaluationDetail />} />
                <Route path="*"                   element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </Layout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
