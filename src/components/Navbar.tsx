import React, { useState } from 'react';
import { AppMode } from '../types';
import {
  ArrowRight,
  Layers,
  GitCompare,
  Server,
  Home,
  Menu,
  X,
} from 'lucide-react';

interface NavbarProps {
  currentView: 'landing' | 'dashboard';
  appMode: AppMode;
  onNavigateHome: () => void;
  onNavigateMode: (mode: AppMode) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  appMode,
  onNavigateHome,
  onNavigateMode,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleModeClick = (mode: AppMode) => {
    onNavigateMode(mode);
    setMobileMenuOpen(false);
  };

  const handleHomeClick = () => {
    onNavigateHome();
    setMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-neutral-200 font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-6">
        {/* Zone 1: Wordmark */}
        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            onClick={handleHomeClick}
            className="flex items-center gap-2 text-sm sm:text-base font-bold tracking-tight text-neutral-900 hover:text-blue-600 transition-colors whitespace-nowrap cursor-pointer text-left"
          >
            <span className="w-2 h-2 rounded-full bg-blue-600" />
            <span>Distributed Load Balancer Simulator</span>
          </button>
        </div>

        {/* Zone 2: Navigation Links */}
        <nav className="hidden md:flex items-center gap-1 lg:gap-2 text-xs font-semibold">
          <button
            type="button"
            onClick={handleHomeClick}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded transition-colors whitespace-nowrap cursor-pointer ${
              currentView === 'landing'
                ? 'bg-neutral-100 text-neutral-900 font-bold'
                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
            }`}
          >
            <Home className="w-3.5 h-3.5" />
            <span>Overview</span>
          </button>

          <button
            type="button"
            onClick={() => handleModeClick('Individual Simulation')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded transition-colors whitespace-nowrap cursor-pointer ${
              currentView === 'dashboard' && appMode === 'Individual Simulation'
                ? 'bg-neutral-100 text-neutral-900 font-bold'
                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Simulation</span>
          </button>

          <button
            type="button"
            onClick={() => handleModeClick('Algorithm Comparison')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded transition-colors whitespace-nowrap cursor-pointer ${
              currentView === 'dashboard' && appMode === 'Algorithm Comparison'
                ? 'bg-neutral-100 text-neutral-900 font-bold'
                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
            }`}
          >
            <GitCompare className="w-3.5 h-3.5" />
            <span>Algorithm Comparison</span>
          </button>

          <button
            type="button"
            onClick={() => handleModeClick('Multi-Node Cluster (Stage 3)')}
            style={{ visibility: 'hidden', pointerEvents: 'none' }}
            tabIndex={-1}
            aria-hidden="true"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded whitespace-nowrap cursor-default ${
              currentView === 'dashboard' && appMode === 'Multi-Node Cluster (Stage 3)'
                ? 'bg-neutral-100 text-neutral-900 font-bold'
                : 'text-neutral-600'
            }`}
          >
            <Server className="w-3.5 h-3.5" />
            <span>Cluster Balancer</span>
          </button>
        </nav>

        {/* Zone 3: Primary CTA */}
        <div className="flex items-center gap-2 shrink-0">
          {currentView === 'landing' ? (
            <button
              type="button"
              onClick={() => handleModeClick('Individual Simulation')}
              className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors whitespace-nowrap shadow-sm cursor-pointer"
            >
              <span>Launch Simulator</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleHomeClick}
              className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-neutral-700 hover:text-neutral-900 bg-neutral-100 hover:bg-neutral-200 border border-neutral-300 rounded transition-colors whitespace-nowrap cursor-pointer"
            >
              <Home className="w-3.5 h-3.5" />
              <span>Back to Overview</span>
            </button>
          )}

          {/* Mobile hamburger button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-1.5 text-neutral-700 hover:text-neutral-900 rounded border border-neutral-300"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-neutral-200 bg-white px-4 py-3 space-y-2">
          <button
            type="button"
            onClick={handleHomeClick}
            className={`w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold rounded text-left ${
              currentView === 'landing' ? 'bg-neutral-100 text-neutral-900' : 'text-neutral-700'
            }`}
          >
            <Home className="w-4 h-4" />
            <span>Overview / Home</span>
          </button>
          <button
            type="button"
            onClick={() => handleModeClick('Individual Simulation')}
            className={`w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold rounded text-left ${
              currentView === 'dashboard' && appMode === 'Individual Simulation'
                ? 'bg-neutral-100 text-neutral-900'
                : 'text-neutral-700'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Simulation</span>
          </button>
          <button
            type="button"
            onClick={() => handleModeClick('Algorithm Comparison')}
            className={`w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold rounded text-left ${
              currentView === 'dashboard' && appMode === 'Algorithm Comparison'
                ? 'bg-neutral-100 text-neutral-900'
                : 'text-neutral-700'
            }`}
          >
            <GitCompare className="w-4 h-4" />
            <span>Algorithm Comparison</span>
          </button>
          <button
            type="button"
            onClick={() => handleModeClick('Multi-Node Cluster (Stage 3)')}
            style={{ visibility: 'hidden', pointerEvents: 'none' }}
            tabIndex={-1}
            aria-hidden="true"
            className={`w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold rounded text-left cursor-default ${
              currentView === 'dashboard' && appMode === 'Multi-Node Cluster (Stage 3)'
                ? 'bg-neutral-100 text-neutral-900'
                : 'text-neutral-700'
            }`}
          >
            <Server className="w-4 h-4" />
            <span>Cluster Balancer</span>
          </button>
        </div>
      )}
    </header>
  );
};
