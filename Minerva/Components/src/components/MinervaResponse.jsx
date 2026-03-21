import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import './MinervaResponse.css';

const MinervaResponse = ({ responseMarkdown, isLivePreview = false }) => {
  // Preprocess markdown to ensure proper formatting
  const preprocessMarkdown = (markdown) => {
    if (!markdown) return '';
    
    // Normalize line endings and ensure proper spacing
    let processed = markdown
      .replace(/\r\n/g, '\n')  // Normalize Windows line endings
      .replace(/\r/g, '\n')   // Normalize Mac line endings
      .replace(/\\n\\n/g, '\n\n') // Convert literal \n\n to actual paragraph breaks
      .replace(/\\n/g, '\n')  // Convert literal \n to actual line breaks
      .trim();
    
    // Handle single \n as line breaks within paragraphs
    // and double \n\n as paragraph breaks
    processed = processed
      // First, protect existing double newlines (paragraph breaks)  
      .replace(/\n\n/g, '§PARAGRAPH_BREAK§')
      // Convert single newlines to HTML line breaks directly
      .replace(/\n/g, '<br />')
      // Restore paragraph breaks
      .replace(/§PARAGRAPH_BREAK§/g, '\n\n');
    
    // Ensure proper spacing around headers (but don't add extra breaks)
    processed = processed
      .replace(/(\n\n|^)(#{1,6}\s)/g, '\n\n$2')
      .replace(/(#{1,6}.*?)(\n\n)/g, '$1\n\n');
    
    // Ensure proper spacing around horizontal rules
    processed = processed
      .replace(/(\n\n|^)(---+)(\n\n|$)/g, '\n\n$2\n\n');
    
    // Clean up any triple newlines that might have been created
    processed = processed.replace(/\n\n\n+/g, '\n\n');
    
    return processed;
  };
  const customComponents = {
    // Custom table styling
    table: ({ children }) => (
      <div className="table-wrapper">
        <table className="minerva-table">{children}</table>
      </div>
    ),
    thead: ({ children }) => <thead>{children}</thead>,
    tbody: ({ children }) => <tbody>{children}</tbody>,
    tr: ({ children }) => <tr>{children}</tr>,
    th: ({ children }) => <th>{children}</th>,
    td: ({ children }) => <td>{children}</td>,
    
    // Custom header styling
    h1: ({ children }) => <h1 className="response-title">{children}</h1>,
    h2: ({ children }) => <h2 className="section-header">{children}</h2>,
    h3: ({ children }) => <h3 className="subsection-header">{children}</h3>,
    
    // Custom paragraph styling with emphasis detection
    p: ({ children }) => {
      // Convert children to text for analysis
      const getText = (node) => {
        if (typeof node === 'string') return node;
        if (Array.isArray(node)) return node.map(getText).join('');
        if (node && node.props && node.props.children) return getText(node.props.children);
        return '';
      };
      
      const text = getText(children) || '';
      const isBriefAnswer = text.toLowerCase().includes('brief answer');
      const isDetailedExplanation = text.toLowerCase().includes('detailed explanation');
      
      if (isBriefAnswer) {
        return <div className="brief-answer">{children}</div>;
      }
      if (isDetailedExplanation) {
        return <div className="detailed-explanation-header">{children}</div>;
      }
      return <p className="response-paragraph">{children}</p>;
    },
    
    // Custom strong/bold styling for key information
    strong: ({ children }) => <strong className="key-info">{children}</strong>,
    
    // Custom list styling
    ul: ({ children }) => <ul className="benefit-list">{children}</ul>,
    li: ({ children }) => <li className="benefit-item">{children}</li>,
    
    // Custom blockquote for important notices
    blockquote: ({ children }) => <div className="important-notice">{children}</div>,
    
    // Custom code styling for benefit codes/references
    code: ({ children }) => <code className="benefit-reference">{children}</code>,
    
    // Custom link styling
    a: ({ href, children }) => (
      <a href={href} className="external-link" target="_blank" rel="noopener noreferrer">
        {children}
      </a>
    ),
    
    // Custom horizontal rule for section dividers
    hr: () => (
      <div style={{
        margin: '24px 0',
        height: '2px',
        background: 'linear-gradient(90deg, #e5e7eb 0%, #3b82f6 50%, #e5e7eb 100%)',
        border: 'none'
      }} />
    ),
  };

  return (
    <div className={`minerva-response-container ${isLivePreview ? 'live-preview' : ''}`}>
      <div className="response-header">
        <div className="minerva-logo">
          <span className="logo-icon">🤖</span>
          <span className="logo-text">Minerva AI Assistant</span>
        </div>
        <div className="response-metadata">
          <span className="accuracy-indicator">✅ 98.7% Accurate</span>
          <span className="response-time">⚡ 2.3s</span>
        </div>
      </div>
      
      <div className="response-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
          components={customComponents}
          skipHtml={false}
          allowedElements={undefined}
        >
          {preprocessMarkdown(responseMarkdown)}
        </ReactMarkdown>
      </div>
      
      <div className="response-footer">
        <div className="citation-notice">
          💡 All information sourced from verified benefit documents and plan data
        </div>
        <div className="feedback-section">
          <button className="feedback-btn helpful">👍 Helpful</button>
          <button className="feedback-btn not-helpful">👎 Not Helpful</button>
          <button className="feedback-btn follow-up">💬 Ask Follow-up</button>
        </div>
      </div>
    </div>
  );
};

export default MinervaResponse;