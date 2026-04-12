# Nature Nudge Marketing Website

A fun, interactive marketing website for the Sunblock iOS app, built with vanilla HTML, CSS, and JavaScript.

## Features

### Visual Design
- **Dynamic Sky Gradient**: Changes based on time of day (dawn, midday, dusk, night)
- **Glassmorphism Effects**: Modern glass card design matching the iOS app
- **Floating Sun Animation**: Interactive sun with pulsing and floating effects
- **Smooth Animations**: Fade-ins, parallax scrolling, and hover effects
- **Dark Mode Support**: Automatically adapts to system color scheme preferences
- **Responsive Design**: Looks great on all devices

### Interactive Elements
- **3D Card Hover Effects**: Cards tilt based on mouse position
- **Floating Particles**: Ambient light particles float across the screen
- **Animated Progress Bar**: Demonstrates the app's progress tracking
- **Smooth Scrolling**: Navigation links smoothly scroll to sections
- **Easter Egg**: Click the floating sun 5 times for a surprise!
- **Accessibility**: Respects reduced motion preferences

### Content Sections
1. **Hero**: Eye-catching intro with app tagline
2. **How It Works**: 3-step guide with numbered cards
3. **Features**: 4-column grid highlighting key benefits
4. **App Preview**: Phone mockup with animated preview
5. **Download**: Call-to-action for App Store
6. **Privacy Policy**: Placeholder page (customize as needed)

## File Structure

```
website/
├── index.html          # Main landing page
├── privacy.html        # Privacy policy page (placeholder)
├── style.css          # All styles and animations
├── script.js          # Interactive features and animations
└── README.md          # This file
```

## Customization

### Update App Store Link
In `index.html`, find the download button and replace `#` with your actual App Store URL:

```html
<a href="YOUR_APP_STORE_URL_HERE" class="app-store-button glass-button">
```

### Update Contact Email
Replace `support@sunblock.app` and `privacy@sunblock.app` with your actual support email.

### Modify Privacy Policy
Edit `privacy.html` to add your complete privacy policy.

### Change Colors
Edit CSS variables in `style.css`:

```css
:root {
    --orange: #FF9500;    /* Primary accent */
    --yellow: #FFCC00;    /* Sun color */
    --blue: #007AFF;      /* Sky blue */
    /* ... etc */
}
```

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- iOS Safari 12+
- Graceful degradation for older browsers
- Respects system preferences (dark mode, reduced motion)

## Performance
- No external dependencies
- Optimized animations using CSS transforms
- Lazy-loaded animations (only when in viewport)
- Minimal JavaScript (~200 lines)

## Deployment
Simply upload all files to any web hosting service:
- Netlify
- Vercel
- GitHub Pages
- Traditional web hosting

No build process required - it's plain HTML, CSS, and JS!

## Notes
- The website matches the iOS app's design language (sky gradients, glass effects, orange/yellow sun theme)
- All animations respect accessibility preferences
- The privacy policy is currently a placeholder - update it with your actual policy
- The App Store button link needs to be updated with your actual app URL

---

**Go outside!** ☀️
