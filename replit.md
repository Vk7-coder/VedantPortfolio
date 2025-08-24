# Overview

This is a personal portfolio website for Vedant Kulkarni, a Business and Data Analyst. The site is designed to showcase professional experience, projects, and skills to impress tech recruiters and hiring managers. It features a modern, dark-themed design with vibrant gradients and smooth animations, built as a responsive web application.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-side rendered approach with Flask templating. The frontend is built with:
- **HTML5 templates** using Jinja2 templating engine
- **CSS3 with modern features** including Flexbox, Grid, and custom properties for consistent theming
- **Vanilla JavaScript** for interactive features like smooth scrolling, mobile menu, and scroll-based animations
- **Responsive design** using mobile-first approach with CSS media queries

## Backend Architecture
The backend follows a simple Flask application structure:
- **Single-file Flask app** (`app.py`) with minimal routing
- **Static file serving** for CSS, JavaScript, and resume PDF downloads
- **Template rendering** for the main portfolio page
- **Environment-based configuration** for session secrets

## Design System
The application implements a cohesive design system featuring:
- **Dark theme** with gradient backgrounds (#0F172A to #1E293B)
- **Emerald green accent color** (#10B981) for interactive elements
- **Inter font family** from Google Fonts for consistent typography
- **Animation system** using Intersection Observer API for scroll-triggered fade-ins

## File Organization
- **Templates**: HTML files stored in `/templates/` directory
- **Static assets**: CSS, JavaScript, and resume files organized in `/static/` subdirectories
- **Main application**: Entry point through both `app.py` and `main.py` for deployment flexibility

# External Dependencies

## Frontend Libraries
- **Google Fonts**: Inter font family for typography
- **Font Awesome 6.0.0**: Icon library for UI elements via CDN

## Python Dependencies
- **Flask**: Web framework for routing and template rendering
- **Standard library modules**: `os` for environment variables, `logging` for debugging

## Hosting Requirements
- **Static file serving**: Required for CSS, JavaScript, and PDF resume downloads
- **Environment variables**: `SESSION_SECRET` for Flask session management
- **Port configuration**: Application runs on port 5000 with host binding to 0.0.0.0