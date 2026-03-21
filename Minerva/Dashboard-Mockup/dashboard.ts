// Minerva Performance Dashboard - Interactive TypeScript
// Stellarus Brand Compliant Dashboard Implementation

interface KPIData {
  title: string;
  value: string;
  change: string;
  isPositive: boolean;
  status?: string;
}

interface MetricData {
  timestamp: Date;
  value: number;
  category: string;
}

class MinervaPerformanceDashboard {
  private autoRefreshInterval: number | null = null;
  private currentTimeRange: string = '7 Days';
  private isAutoRefreshEnabled: boolean = true;

  constructor() {
    this.initializeEventListeners();
    this.startAutoRefresh();
    this.updateLastRefreshTime();
    console.log('🌟 Stellarus Minerva Dashboard initialized');
  }

  private initializeEventListeners(): void {
    // Time range button handlers
    const timeButtons = document.querySelectorAll('.time-btn');
    timeButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const target = e.target as HTMLButtonElement;
        this.handleTimeRangeChange(target.textContent || '7 Days');
      });
    });

    // Auto refresh toggle
    const autoRefreshBtn = document.querySelector('.auto-refresh') as HTMLButtonElement;
    if (autoRefreshBtn) {
      autoRefreshBtn.addEventListener('click', () => {
        this.toggleAutoRefresh();
      });
    }

    // Settings button
    const settingsBtn = document.querySelector('.settings-btn') as HTMLButtonElement;
    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => {
        this.openSettings();
      });
    }

    // Export data button
    const exportBtn = document.querySelector('.export-btn') as HTMLButtonElement;
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        this.exportDashboardData();
      });
    }

    // KPI card hover effects
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach(card => {
      card.addEventListener('mouseenter', (e) => {
        this.highlightRelatedCharts(e.target as HTMLElement);
      });
    });

    // Action buttons in footer
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const target = e.target as HTMLButtonElement;
        this.handleActionButton(target.textContent || '');
      });
    });
  }

  private handleTimeRangeChange(range: string): void {
    // Update active state
    const timeButtons = document.querySelectorAll('.time-btn');
    timeButtons.forEach(btn => btn.classList.remove('active'));
    
    const selectedButton = Array.from(timeButtons).find(btn => 
      btn.textContent === range
    ) as HTMLButtonElement;
    
    if (selectedButton) {
      selectedButton.classList.add('active');
    }

    this.currentTimeRange = range;
    this.refreshDashboardData();
    
    console.log(`📊 Time range changed to: ${range}`);
    this.showToast(`Dashboard updated for ${range}`, 'info');
  }

  private toggleAutoRefresh(): void {
    this.isAutoRefreshEnabled = !this.isAutoRefreshEnabled;
    const autoRefreshBtn = document.querySelector('.auto-refresh') as HTMLButtonElement;
    
    if (this.isAutoRefreshEnabled) {
      autoRefreshBtn.textContent = 'AUTO-REFRESH: ON';
      autoRefreshBtn.style.background = '#10b981'; // success color
      this.startAutoRefresh();
      this.showToast('Auto-refresh enabled', 'success');
    } else {
      autoRefreshBtn.textContent = 'AUTO-REFRESH: OFF';
      autoRefreshBtn.style.background = '#6b7280'; // gray color
      this.stopAutoRefresh();
      this.showToast('Auto-refresh disabled', 'warning');
    }
  }

  private startAutoRefresh(): void {
    if (this.autoRefreshInterval) {
      clearInterval(this.autoRefreshInterval);
    }
    
    this.autoRefreshInterval = window.setInterval(() => {
      if (this.isAutoRefreshEnabled) {
        this.refreshDashboardData();
        this.updateLastRefreshTime();
      }
    }, 30000); // Refresh every 30 seconds
  }

  private stopAutoRefresh(): void {
    if (this.autoRefreshInterval) {
      clearInterval(this.autoRefreshInterval);
      this.autoRefreshInterval = null;
    }
  }

  private refreshDashboardData(): void {
    console.log('🔄 Refreshing dashboard data...');
    
    // Simulate data refresh with loading states
    this.showLoadingStates();
    
    // Simulate API call delay
    setTimeout(() => {
      this.updateKPIValues();
      this.hideLoadingStates();
      this.updateChartData();
    }, 1000);
  }

  private updateKPIValues(): void {
    // Simulate dynamic KPI updates
    const kpiCards = document.querySelectorAll('.kpi-card');
    
    kpiCards.forEach((card, index) => {
      const valueElement = card.querySelector('.kpi-value') as HTMLElement;
      const changeElement = card.querySelector('.kpi-change') as HTMLElement;
      
      if (valueElement && changeElement) {
        // Add subtle animation to indicate update
        valueElement.style.transform = 'scale(1.05)';
        valueElement.style.transition = 'transform 0.2s ease';
        
        setTimeout(() => {
          valueElement.style.transform = 'scale(1)';
        }, 200);
      }
    });
  }

  private updateChartData(): void {
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
      // Add updated indicator
      container.classList.add('updated');
      setTimeout(() => {
        container.classList.remove('updated');
      }, 2000);
    });
  }

  private showLoadingStates(): void {
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach(card => {
      card.classList.add('loading');
    });
  }

  private hideLoadingStates(): void {
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach(card => {
      card.classList.remove('loading');
    });
  }

  private updateLastRefreshTime(): void {
    const lastUpdatedElement = document.querySelector('.last-updated') as HTMLElement;
    if (lastUpdatedElement) {
      const now = new Date();
      const timeString = now.toLocaleString('en-US', {
        month: 'numeric',
        day: 'numeric',
        year: '2-digit',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
      lastUpdatedElement.textContent = `Last Updated: ${timeString}`;
    }
  }

  private openSettings(): void {
    this.showToast('Settings panel coming soon...', 'info');
    console.log('⚙️ Opening settings panel');
  }

  private exportDashboardData(): void {
    const data = this.generateExportData();
    const blob = new Blob([data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `minerva-dashboard-${this.currentTimeRange.replace(' ', '-')}-${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    window.URL.revokeObjectURL(url);
    this.showToast('Dashboard data exported successfully', 'success');
  }

  private generateExportData(): string {
    const headers = ['Metric', 'Value', 'Change', 'Timestamp'];
    const timestamp = new Date().toISOString();
    
    const data = [
      ['System Status', '99.8% Uptime', '+0.1%', timestamp],
      ['Response Time', '2.3s AVG', '+0.2s', timestamp],
      ['Accuracy Rate', '98.7%', '+0.3%', timestamp],
      ['Total Products', '2,847', '+156', timestamp],
      ['Sessions Today', '1,247', '+15%', timestamp],
      ['API Error Rate', '0.12%', '-0.05%', timestamp]
    ];
    
    return [headers, ...data].map(row => row.join(',')).join('\n');
  }

  private highlightRelatedCharts(kpiCard: HTMLElement): void {
    const titleElement = kpiCard.querySelector('.kpi-title') as HTMLElement;
    const title = titleElement?.textContent || '';
    
    // Add visual feedback
    kpiCard.style.boxShadow = '0 10px 25px rgba(37, 99, 235, 0.2)';
    
    setTimeout(() => {
      kpiCard.style.boxShadow = '';
    }, 2000);
  }

  private handleActionButton(buttonText: string): void {
    switch (buttonText) {
      case 'View All Alerts':
        this.showAllAlerts();
        break;
      case 'Configure Alerts':
        this.configureAlerts();
        break;
      case 'Download Report':
        this.downloadReport();
        break;
      default:
        console.log(`Action: ${buttonText}`);
    }
  }

  private showAllAlerts(): void {
    const alertsData = [
      { type: 'warning', message: 'Response time exceeded 5s threshold', time: '12:30 PM' },
      { type: 'info', message: 'Question volume 25% above normal', time: '1:15 PM' },
      { type: 'success', message: 'System backup completed', time: '11:45 AM' },
      { type: 'warning', message: 'High memory usage detected', time: '10:20 AM' }
    ];
    
    console.log('🔔 All alerts:', alertsData);
    this.showToast(`Showing ${alertsData.length} alerts`, 'info');
  }

  private configureAlerts(): void {
    this.showToast('Alert configuration panel opening...', 'info');
  }

  private downloadReport(): void {
    this.showToast('Generating comprehensive report...', 'info');
    
    setTimeout(() => {
      this.showToast('Report download started', 'success');
    }, 2000);
  }

  private showToast(message: string, type: 'success' | 'warning' | 'error' | 'info'): void {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Style the toast
    Object.assign(toast.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '12px 24px',
      borderRadius: '8px',
      color: 'white',
      fontWeight: '500',
      fontSize: '14px',
      zIndex: '1000',
      opacity: '0',
      transform: 'translateX(100%)',
      transition: 'all 0.3s ease'
    });
    
    // Set background color based on type
    const backgrounds = {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6'
    };
    toast.style.background = backgrounds[type];
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after delay
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 3000);
  }

  // Public methods for external API integration
  public setMetricValue(metricName: string, value: string, change?: string): void {
    const kpiCards = document.querySelectorAll('.kpi-card');
    
    kpiCards.forEach(card => {
      const titleElement = card.querySelector('.kpi-title') as HTMLElement;
      if (titleElement && titleElement.textContent?.includes(metricName.toUpperCase())) {
        const valueElement = card.querySelector('.kpi-value') as HTMLElement;
        const changeElement = card.querySelector('.kpi-change') as HTMLElement;
        
        if (valueElement) valueElement.textContent = value;
        if (changeElement && change) changeElement.textContent = change;
      }
    });
  }

  public addAlert(type: string, message: string): void {
    const alertsList = document.querySelector('.alerts-list') as HTMLElement;
    if (alertsList) {
      const alert = document.createElement('span');
      alert.className = `alert ${type}`;
      alert.textContent = `${type === 'warning' ? '⚠️' : 'ℹ️'} ${message} (${new Date().toLocaleTimeString()})`;
      alertsList.appendChild(alert);
    }
  }
}

// CSS for loading states and animations
const additionalStyles = `
.kpi-card.loading {
  position: relative;
  pointer-events: none;
}

.kpi-card.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-container.updated {
  border-left: 4px solid #10b981;
  transition: all 0.3s ease;
}

.chart-container.updated .chart-header {
  background: #f0fdf4;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.loading {
  animation: pulse 1.5s ease-in-out infinite;
}

/* Chart hover effects */
.chart-container:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new MinervaPerformanceDashboard();
});

// Export for module usage
export { MinervaPerformanceDashboard };