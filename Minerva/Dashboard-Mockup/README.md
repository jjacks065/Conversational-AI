# Stellarus Minerva Performance Dashboard

A professional, brand-compliant dashboard mockup for monitoring Minerva AI system performance across customer deployments.

## 🌟 Features

### Dashboard Components
- **Real-time KPI Monitoring**: System status, response times, accuracy rates, and product pipeline metrics
- **Interactive Time Controls**: 7-day, 30-day, 90-day, and custom range selection
- **Customer-Scoped Analytics**: Multi-tenant data filtering for customer vs Stellarus users
- **Responsive Design**: Optimized for desktop, tablet, and mobile viewing
- **Auto-refresh Capability**: Configurable real-time data updates
- **Export Functionality**: CSV download of dashboard metrics
- **Alert Management**: Visual notification system with status indicators

### Brand Compliance
- **Stellarus Color Palette**: Primary blues (#2563eb, #1d4ed8) with accent colors
- **Typography**: Inter font family for professional appearance
- **Component Design**: Consistent border radius, shadows, and spacing
- **Accessibility**: Proper focus states and ARIA compliance
- **Responsive Breakpoints**: Mobile-first responsive design principles

## 🚀 Quick Start

### Option 1: Simple HTTP Server
```bash
# Navigate to the dashboard directory
cd Dashboard-Mockup

# Start a simple HTTP server
python -m http.server 8080
# or
npx serve .

# Open http://localhost:8080 in your browser
```

### Option 2: Development Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Option 3: Live Preview
Simply open `index.html` in your web browser for immediate preview.

## 🎨 Stellarus Brand Guidelines

### Color System
```css
/* Primary Colors */
--stellarus-primary: #2563eb;        /* Primary Blue */
--stellarus-primary-dark: #1d4ed8;   /* Dark Blue */
--stellarus-primary-light: #3b82f6;  /* Light Blue */
--stellarus-secondary: #7c3aed;      /* Purple Accent */
--stellarus-accent: #06b6d4;         /* Cyan Accent */

/* Semantic Colors */
--success: #10b981;    /* Green */
--warning: #f59e0b;    /* Orange */
--error: #ef4444;      /* Red */
--info: #3b82f6;       /* Blue */
```

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Scale**: Modular scale from 0.75rem to 1.875rem

### Layout Principles
- **Grid System**: CSS Grid with auto-fit responsive columns
- **Spacing**: 8px base unit scaling (0.25rem, 0.5rem, 0.75rem, 1rem...)
- **Border Radius**: Consistent rounding (0.375rem to 1rem)
- **Shadows**: Layered depth system for visual hierarchy

## 📊 Dashboard Sections

### 1. Header
- Stellarus logo and branding
- Dashboard title and user context
- Auto-refresh toggle and settings access
- Last updated timestamp

### 2. Time Range Controls
- Interactive time period selection
- Export data functionality
- Responsive button layout

### 3. Key Performance Indicators (KPIs)
- **System Status**: Uptime percentage with online/offline indicator
- **Response Time**: Average response time with trend indicators
- **Accuracy Rate**: AI accuracy percentage with performance trends
- **Total Products**: Customer product count with growth metrics
- **Sessions Today**: Daily session volume with percentage change
- **API Error Rate**: Error percentage with trend indicators

### 4. Analytics Charts
- **Response Time Distribution**: Performance metrics visualization
- **Session Analytics**: Usage patterns and trending
- **Questions Per Session**: Distribution analysis
- **Application Health**: Multi-metric health monitoring
- **Cost Analysis**: Customer-facing cost metrics (if enabled)
- **Product Pipeline Analytics**: Ingestion success/failure rates

### 5. Alert System
- Real-time notification display
- Severity-based color coding
- Action buttons for alert management

## 🔧 Customization

### Brand Color Updates
Update the CSS custom properties in `styles.css`:
```css
:root {
  --stellarus-primary: #your-color;
  /* Update other brand colors as needed */
}
```

### Adding New Metrics
1. Add KPI card HTML structure
2. Update TypeScript interface definitions
3. Implement data binding in dashboard class
4. Add corresponding CSS styles

### API Integration
The dashboard includes methods for external API integration:
```typescript
// Update metric values
dashboard.setMetricValue('RESPONSE TIME', '1.8s', '↓0.5s');

// Add new alerts
dashboard.addAlert('warning', 'High CPU usage detected');
```

## 📱 Responsive Design

The dashboard adapts to different screen sizes:
- **Desktop**: Full feature layout with side-by-side charts
- **Tablet**: Stacked chart layout with maintained functionality  
- **Mobile**: Single-column layout with optimized touch targets

## 🔒 Security Considerations

- No sensitive data in client-side code
- Role-based access control ready for backend integration
- Customer data segregation built into UI design
- HTTPS requirement for production deployment

## 🎯 Future Enhancements

### Phase 2 Features
- Real-time WebSocket data integration
- Advanced filtering and drill-down capabilities
- Custom alert threshold configuration
- Enhanced data visualization with charts library
- PDF report generation
- Dark mode theme support

### Integration Roadmap
- Stellarus authentication system
- Minerva telemetry API connection
- Customer SSO integration
- Multi-tenant data backend
- Real-time notification system

## 📄 File Structure

```
Dashboard-Mockup/
├── index.html              # Main dashboard HTML
├── styles.css             # Stellarus brand CSS
├── dashboard.ts           # TypeScript functionality  
├── package.json           # Project dependencies
└── README.md             # This documentation
```

## 🤝 Contributing

1. Follow Stellarus brand guidelines
2. Maintain responsive design principles
3. Include TypeScript type definitions
4. Test across major browsers
5. Document new features and API changes

## 📞 Support

For questions about this dashboard mockup or Stellarus brand guidelines:
- Engineering Team: engineering@stellarus.com
- Design System: design@stellarus.com
- Product Team: product@stellarus.com

---

**Built with 💙 by the Stellarus Team**

*This mockup demonstrates the proposed Minerva Performance Dashboard design following Stellarus brand guidelines and technical specifications.*