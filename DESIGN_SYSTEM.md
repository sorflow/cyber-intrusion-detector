# Design System Guidelines
## Smart Home Dashboard Aesthetic for Cybersecurity Intrusion Detection

### Design Philosophy
**Clean, Modern, Functional Minimalism**
- Focus on clarity and usability over decorative elements
- Card-based modular architecture for flexible layouts
- Information hierarchy through typography and spacing
- Professional yet approachable aesthetic suitable for technical dashboards

---

## Color Palette

### Primary Colors
- **Background Primary**: `#FFFFFF` (Pure White)
  - Used for main page background and card backgrounds
- **Background Secondary**: `#F5F5F5` or `#FAFAFA` (Light Gray)
  - Used for list items, inactive states, subtle separations
- **Background Tertiary**: `#E8E8E8` (Medium Gray)
  - Used for hover states, subtle borders

### Accent Colors
- **Primary Accent**: `#FFD700` or `#FFEB3B` (Neon Yellow / Bright Yellow)
  - Used for: User greetings, important highlights, active indicators, icons
  - Creates visual interest and draws attention to key information
- **Secondary Accent**: `#2196F3` or `#42A5F5` (Light Blue)
  - Used for: Active states, progress indicators, temperature dials, interactive elements
  - Conveys trust and technology

### Text Colors
- **Primary Text**: `#000000` or `#212121` (Black / Near Black)
  - Used for: Headings, titles, primary information, device names
- **Secondary Text**: `#757575` or `#9E9E9E` (Medium Gray)
  - Used for: Subtitles, descriptions, metadata, "Daily usage", "Auto cooling"
- **Tertiary Text**: `#BDBDBD` (Light Gray)
  - Used for: Placeholder text, disabled states

### Interactive States
- **Active/On State**: Blue accent (`#2196F3`) with white text
- **Hover State**: Slightly darker background (`#E8E8E8`)
- **Selected State**: Blue accent with white text or yellow highlight

---

## Typography

### Font Hierarchy

**Headings (Bold, Black)**
- **H1 / User Greeting**: Large, bold, black text
  - Example: "Hi, Diana Kemmer"
  - Weight: 700 (Bold)
  - Size: 24-32px
  - Line height: 1.2

**Card Titles (Bold, Black)**
- **H2 / Widget Titles**: Medium, bold, black text
  - Example: "AI Power Analytics", "Air Conditioner"
  - Weight: 600-700 (Semi-bold to Bold)
  - Size: 18-22px
  - Line height: 1.3

**Body Text (Regular, Black/Gray)**
- **Primary Body**: Regular weight, black text
  - Example: Device names, main content
  - Weight: 400 (Regular)
  - Size: 14-16px
  - Line height: 1.5

**Secondary Text (Regular, Gray)**
- **Metadata/Subtitles**: Regular weight, gray text
  - Example: "Daily usage", "Auto cooling", "7 devices active"
  - Weight: 400 (Regular)
  - Size: 12-14px
  - Line height: 1.4
  - Color: `#757575`

**Font Family Recommendations**
- **Primary**: `Inter`, `Roboto`, `SF Pro Display`, or `System UI`
- **Fallback**: `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif`
- **Monospace** (for code/data): `JetBrains Mono`, `Fira Code`, `Consolas`

---

## Layout & Structure

### Grid System
- **Two-Column Layout**: Primary layout pattern
  - Left column: 50-60% width (analytics, lists, data)
  - Right column: 40-50% width (controls, actions, details)
- **Responsive Breakpoints**:
  - Desktop: 2-column layout
  - Tablet: 2-column with adjusted widths
  - Mobile: Single column, stacked

### Card Architecture
- **Card Style**: Rounded rectangles with white background
- **Border Radius**: `12px` to `16px` (moderately rounded, modern)
- **Card Padding**: `20px` to `24px` (generous spacing)
- **Card Shadow**: Subtle shadow for depth
  - `box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08)` or `0 1px 3px rgba(0, 0, 0, 0.12)`
- **Card Spacing**: `16px` to `24px` gap between cards

### Header Section
- **User Greeting Area**: Top of page
  - Profile picture: Circular, `48px` to `64px` diameter
  - Greeting bubble: Rounded rectangle with yellow background
  - Status text: Gray, smaller font below name
  - Menu dots: Top right, three vertical dots

---

## Spacing System

### Base Unit
- **Base Unit**: `4px` or `8px` (8px recommended for consistency)

### Spacing Scale
- **XS**: `4px` - Tight spacing for related elements
- **S**: `8px` - Default spacing for list items
- **M**: `16px` - Standard spacing between elements
- **L**: `24px` - Spacing between cards/sections
- **XL**: `32px` - Major section separation
- **XXL**: `48px` - Page-level spacing

### Padding Guidelines
- **Card Padding**: `20-24px` (internal card spacing)
- **List Item Padding**: `12-16px` vertical, `16px` horizontal
- **Button Padding**: `12px` vertical, `24px` horizontal
- **Icon Spacing**: `8-12px` between icon and text

---

## Component Design Patterns

### List Items (Device List Pattern)
- **Container**: Rounded rectangle, light gray background (`#F5F5F5`)
- **Layout**: Horizontal, icon on left, text in middle, arrow on right
- **Height**: `64px` to `72px` (comfortable touch target)
- **Icon Size**: `24px` to `32px`
- **Text Alignment**: Left-aligned, icon and text vertically centered
- **Interactive**: Right-pointing arrow indicates clickability
- **Hover State**: Slightly darker background or subtle border

### Control Widgets (Air Conditioner Pattern)
- **Header Section**:
  - Icon + Title (left-aligned)
  - Status/Toggle (right-aligned)
  - Subtitle below title (gray text)
- **Main Control**: Large, prominent interactive element
  - Semi-circular dial for temperature/values
  - Current value prominently displayed in center
  - Active range highlighted in accent color (blue)
- **Secondary Controls**: Small buttons below main control

### Scene Cards (Morning/Night Pattern)
- **Small Card Style**: Rounded rectangle
- **Background**: Light blue for active, white for inactive
- **Icon**: Top left, colored (yellow for night, blue for morning)
- **Title**: Bold, black text
- **Metadata**: Gray text below title
- **Menu Dots**: Top right, three vertical dots

### Buttons
- **Primary Button**: 
  - Background: Black (`#000000`) or accent color
  - Text: White
  - Padding: `12px 24px`
  - Border radius: `8px`
  - Height: `40-44px`
- **Secondary Button**:
  - Background: Transparent or light gray
  - Text: Black
  - Border: 1px solid gray (optional)
- **Icon Button**:
  - Circular, `40px` diameter
  - Icon centered, `20px` size
  - Background: Light gray or accent color

---

## Iconography

### Icon Style
- **Style**: Line icons or filled icons with consistent stroke weight
- **Size**: 
  - Small: `16px` (inline with text)
  - Medium: `24px` (list items, buttons)
  - Large: `32px` (featured icons)
  - Extra Large: `48px` (hero icons)
- **Color**: 
  - Default: Black or gray
  - Accent: Yellow or blue for active/important states
- **Spacing**: `8-12px` between icon and text

### Common Icons
- Lightning bolt (analytics/power)
- Snowflake (cooling/AC)
- Sun (morning/day)
- Moon (night)
- Wi-Fi signal
- TV screen
- Water droplets (humidifier)
- Arrow (navigation)
- Plus (add/create)
- Three dots (menu)

---

## Interactive Elements

### Toggle Switches
- **Style**: Modern toggle switch
- **On State**: Blue background (`#2196F3`)
- **Off State**: Gray background (`#E0E0E0`)
- **Size**: `44px` width, `24px` height (standard)
- **Animation**: Smooth transition

### Dials/Sliders
- **Style**: Semi-circular or circular dial
- **Active Range**: Highlighted in accent color (blue)
- **Current Value**: Large, centered display
- **Range Labels**: Small text at extremes
- **Interactive**: Smooth drag interaction

### Navigation Arrows
- **Style**: Right-pointing arrow, `16-20px`
- **Color**: Black or gray
- **Indicates**: Clickable, expandable, or navigable

---

## Design Principles

### 1. Clarity First
- Information hierarchy is clear and unambiguous
- No unnecessary decorative elements
- Every element serves a functional purpose

### 2. Consistency
- Reusable component patterns throughout
- Consistent spacing, typography, and colors
- Predictable interactions

### 3. Modularity
- Card-based architecture allows flexible layouts
- Components can be rearranged without breaking design
- Easy to add/remove features

### 4. Visual Hierarchy
- Size, weight, and color create clear information hierarchy
- Most important information is largest and boldest
- Secondary information is smaller and lighter

### 5. Accessibility
- High contrast ratios for text (WCAG AA minimum)
- Touch targets minimum `44px` height
- Clear focus states for keyboard navigation
- Color not the only indicator of state

### 6. Modern Aesthetic
- Rounded corners (not sharp rectangles)
- Subtle shadows for depth
- Generous white space
- Clean, uncluttered layouts

---

## Application to Cybersecurity Dashboard

### Mapping Components
- **User Greeting** → Dashboard header with user info and active alerts count
- **AI Power Analytics** → Attack detection analytics widget
- **Device List** → List of detected attacks/threats
- **Air Conditioner Control** → Real-time prediction controls
- **Scenes** → Predefined monitoring profiles (e.g., "High Security", "Standard")

### Color Adaptation
- **Yellow Accent**: Use for high-priority alerts, critical threats
- **Blue Accent**: Use for active monitoring, real-time data streams
- **Gray Backgrounds**: Use for historical data, inactive states
- **Black Text**: Primary information (attack types, confidence scores)
- **Gray Text**: Metadata (timestamps, device counts, statistics)

### Component Examples
1. **Threat List Card**: Similar to device list, showing detected attacks
2. **Real-time Monitor**: Similar to AC control, showing current prediction confidence
3. **Analytics Dashboard**: Similar to power analytics, showing attack frequency
4. **Alert Scenes**: Similar to morning/night scenes, showing security profiles

---

## Implementation Notes

### CSS Variables (Recommended)
```css
:root {
  /* Colors */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F5F5F5;
  --bg-tertiary: #E8E8E8;
  --accent-yellow: #FFD700;
  --accent-blue: #2196F3;
  --text-primary: #212121;
  --text-secondary: #757575;
  --text-tertiary: #BDBDBD;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-s: 8px;
  --spacing-m: 16px;
  --spacing-l: 24px;
  --spacing-xl: 32px;
  
  /* Typography */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-size-h1: 28px;
  --font-size-h2: 20px;
  --font-size-body: 16px;
  --font-size-small: 14px;
  --font-size-caption: 12px;
  
  /* Borders */
  --border-radius: 12px;
  --border-radius-small: 8px;
  --border-radius-large: 16px;
  
  /* Shadows */
  --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.12);
}
```

### Streamlit Customization
- Use `st.markdown` with custom CSS for styling
- Create custom components using `st.components.v1.html`
- Override Streamlit's default theme with custom CSS
- Use columns (`st.columns`) for two-column layout
- Apply card styling with `st.container()` and custom CSS

---

## Quick Reference Checklist

When implementing components, ensure:
- [ ] Rounded corners (`12-16px` border radius)
- [ ] Generous padding (`20-24px` in cards)
- [ ] Clear typography hierarchy (bold for titles, gray for metadata)
- [ ] Yellow accent for highlights/important info
- [ ] Blue accent for active/interactive states
- [ ] White/light gray backgrounds
- [ ] Subtle shadows for depth
- [ ] Consistent spacing (`8px` base unit)
- [ ] Icon + text alignment (icons `24px`, `8-12px` spacing)
- [ ] Right-pointing arrows for clickable items
- [ ] Touch-friendly sizes (`44px` minimum height)

---

This design system provides comprehensive guidelines for replicating the modern, clean aesthetic of the smart home dashboard in your cybersecurity intrusion detection application.

