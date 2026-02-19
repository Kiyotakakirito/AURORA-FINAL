import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Upload, 
  Menu,
  X
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Submit Project', href: '/submit', icon: Upload },
  ];

  const isActive = (href: string) => location.pathname === href;

  return (
    <div className="min-h-screen bg-deep-900 relative overflow-hidden">
      {/* Watermark Background - Multiple Logo Instances */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        {/* Center large watermark */}
        <img 
          src="/aurora-logo.png" 
          alt="" 
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-auto opacity-[0.02]"
        />
        {/* Corner watermarks */}
        <img src="/aurora-logo.png" alt="" className="absolute top-10 left-10 w-[200px] h-auto opacity-[0.015]" />
        <img src="/aurora-logo.png" alt="" className="absolute top-10 right-10 w-[200px] h-auto opacity-[0.015]" />
        <img src="/aurora-logo.png" alt="" className="absolute bottom-10 left-10 w-[200px] h-auto opacity-[0.015]" />
        <img src="/aurora-logo.png" alt="" className="absolute bottom-10 right-10 w-[200px] h-auto opacity-[0.015]" />
        {/* Side watermarks */}
        <img src="/aurora-logo.png" alt="" className="absolute top-1/4 left-5 w-[150px] h-auto opacity-[0.01]" />
        <img src="/aurora-logo.png" alt="" className="absolute top-3/4 left-5 w-[150px] h-auto opacity-[0.01]" />
        <img src="/aurora-logo.png" alt="" className="absolute top-1/4 right-5 w-[150px] h-auto opacity-[0.01]" />
        <img src="/aurora-logo.png" alt="" className="absolute top-3/4 right-5 w-[150px] h-auto opacity-[0.01]" />
      </div>

      {/* Animated Stars Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {/* Twinkling Stars - 30 stars */}
        {[...Array(30)].map((_, i) => (
          <div key={`star-${i}`} className={`star star-${i + 1}`}></div>
        ))}

        {/* Main Floating Particles - 20 particles */}
        {[...Array(20)].map((_, i) => (
          <div key={`particle-${i}`} className={`particle particle-${i + 1}`}></div>
        ))}

        {/* Medium Particles - 15 particles */}
        {[...Array(15)].map((_, i) => (
          <div key={`medium-${i}`} className={`medium-particle mp-${i + 1}`}></div>
        ))}

        {/* Micro Particles - 20 particles */}
        {[...Array(20)].map((_, i) => (
          <div key={`micro-${i}`} className={`micro-particle mp-${i + 1}`}></div>
        ))}

        {/* Aurora Glow Effect */}
        <div className="aurora-glow-bg"></div>
      </div>
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? '' : 'pointer-events-none'}`}>
        <div className={`fixed inset-0 bg-deep-1000/90 backdrop-blur-sm transition-opacity ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`} 
             onClick={() => setSidebarOpen(false)} />
        
        <div className={`relative flex w-64 flex-1 flex-col bg-aurora-800/90 backdrop-blur-md border-r border-aurora-600/30 transform transition-transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
          <div className="flex items-center justify-between p-4 border-b border-aurora-600/30">
            <div className="flex items-center space-x-2">
              <img src="/aurora-logo.png" alt="AURORA" className="h-10 w-auto" />
              <h1 className="text-xl font-bold text-white">AURORA</h1>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-aurora-200 hover:text-glow-cyan transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          
          <nav className="flex-1 p-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-all ${
                    isActive(item.href)
                      ? 'bg-aurora-600/50 text-glow-cyan border border-glow-cyan/30'
                      : 'text-aurora-100 hover:bg-aurora-700/50 hover:text-glow-cyan'
                  }`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
          
          <div className="p-4 border-t border-aurora-600/30">
            <p className="text-xs text-aurora-300 text-center">
              Automated Universal Review<br/>& Objective Rating Analyzer
            </p>
          </div>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-1 flex-col bg-aurora-800/80 backdrop-blur-md border-r border-aurora-600/30">
          <div className="flex items-center p-6 border-b border-aurora-600/30">
            <img src="/aurora-logo.png" alt="AURORA" className="h-12 w-auto mr-3" />
            <div>
              <h1 className="text-2xl font-bold text-white tracking-wider">AURORA</h1>
              <p className="text-xs text-glow-teal">AI Evaluation System</p>
            </div>
          </div>
          
          <nav className="flex-1 p-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all ${
                    isActive(item.href)
                      ? 'bg-aurora-600/50 text-glow-cyan border border-glow-cyan/30'
                      : 'text-aurora-100 hover:bg-aurora-700/50 hover:text-glow-cyan'
                  }`}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
          
          <div className="p-4 border-t border-aurora-600/30">
            <p className="text-xs text-aurora-300 text-center leading-relaxed">
              Automated Universal Review<br/>& Objective Rating Analyzer
            </p>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-40 bg-deep-800/90 backdrop-blur-md border-b border-aurora-600/30">
          <div className="flex items-center justify-between p-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="text-aurora-200 hover:text-glow-cyan lg:hidden transition-colors"
            >
              <Menu className="h-6 w-6" />
            </button>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <img src="/aurora-logo.png" alt="AURORA" className="h-6 w-auto" />
                <span className="text-sm text-aurora-100">
                  AI-Powered Project Evaluation
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
