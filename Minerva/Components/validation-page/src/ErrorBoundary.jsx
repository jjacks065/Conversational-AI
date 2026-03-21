import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '20px', 
          backgroundColor: '#ffebee', 
          border: '1px solid #f44336',
          margin: '20px'
        }}>
          <h2 style={{color: '#d32f2f'}}>Something went wrong!</h2>
          <details>
            <summary>Error details</summary>
            <pre style={{color: '#666', fontSize: '14px'}}>
              {this.state.error && this.state.error.toString()}
            </pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;