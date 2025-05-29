from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Manager | Rahul don</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css">
    <style>
        :root {
            --primary: #7c3aed;
            --primary-dark: #5b21b6;
            --primary-light: #8b5cf6;
            --dark: #0f172a;
            --darker: #020617;
            --dark-light: #1e293b;
            --light: #f8fafc;
            --gray: #94a3b8;
            --gray-light: #cbd5e1;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --glass: rgba(15, 23, 42, 0.7);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background-color: var(--darker);
            color: var(--light);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: radial-gradient(circle at 10% 20%, rgba(28, 28, 28, 0.1) 0%, rgba(15, 23, 42, 0.8) 90%);
        }
        
        /* Header */
        .header {
            background-color: var(--glass);
            backdrop-filter: blur(12px);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }
        
        .header-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--light);
            background: linear-gradient(to right, var(--primary), var(--primary-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .menu-toggle {
            width: 40px;
            height: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            gap: 6px;
            transition: all 0.3s ease;
            border-radius: 50%;
        }
        
        .menu-toggle:hover {
            background-color: rgba(148, 163, 184, 0.1);
        }
        
        .menu-toggle span {
            display: block;
            width: 24px;
            height: 2px;
            background-color: var(--light);
            transition: all 0.3s ease;
        }
        
        .menu-toggle.active span:nth-child(1) {
            transform: translateY(8px) rotate(45deg);
        }
        
        .menu-toggle.active span:nth-child(2) {
            opacity: 0;
        }
        
        .menu-toggle.active span:nth-child(3) {
            transform: translateY(-8px) rotate(-45deg);
        }
        
        /* Sidebar */
        .sidebar {
            position: fixed;
            top: 0;
            right: -320px;
            width: 320px;
            height: 100vh;
            background-color: var(--dark);
            z-index: 90;
            transition: right 0.3s ease;
            padding: 1.5rem;
            border-left: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.2);
        }
        
        .sidebar.active {
            right: 0;
        }
        
        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary-light);
        }
        
        .sidebar-close {
            background: none;
            border: none;
            color: var(--gray);
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }
        
        .sidebar-close:hover {
            background-color: rgba(148, 163, 184, 0.1);
            color: var(--light);
        }
        
        .sidebar-menu {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .sidebar-item {
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            color: var(--gray-light);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            transition: all 0.2s ease;
            font-weight: 500;
        }
        
        .sidebar-item i {
            width: 24px;
            text-align: center;
            font-size: 1rem;
        }
        
        .sidebar-item:hover {
            background-color: rgba(148, 163, 184, 0.1);
            color: var(--light);
            transform: translateX(5px);
        }
        
        .sidebar-item.active {
            background-color: var(--primary);
            color: white;
            box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
        }
        
        /* Main Content */
        .main {
            flex: 1;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        /* Cards */
        .card {
            background-color: var(--glass);
            backdrop-filter: blur(12px);
            border-radius: 1rem;
            padding: 2rem;
            width: 100%;
            max-width: 700px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: var(--light);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .card-title i {
            color: var(--primary-light);
        }

        /* Owner Profile Section */
        .owner-profile {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }

        .owner-avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid var(--primary);
            box-shadow: 0 0 0 6px rgba(123, 97, 255, 0.3);
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }

        .owner-avatar:hover {
            transform: scale(1.05);
        }

        .owner-name {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-light);
            margin-bottom: 0.5rem;
        }

        .owner-bio {
            font-size: 0.9375rem;
            color: var(--gray-light);
            line-height: 1.6;
            max-width: 500px;
            margin: 0 auto 1.5rem auto;
        }
        
        /* Form Elements */
        .form-group {
            margin-bottom: 1.25rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
            color: var(--gray-light);
            font-weight: 500;
        }
        
        .form-control {
            width: 100%;
            padding: 0.875rem 1.25rem;
            background-color: rgba(148, 163, 184, 0.05);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 0.75rem;
            color: var(--light);
            font-size: 0.9375rem;
            transition: all 0.3s ease;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(123, 97, 255, 0.2);
            background-color: rgba(123, 97, 255, 0.05);
        }
        
        textarea.form-control {
            min-height: 120px;
            resize: vertical;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.875rem 1.75rem;
            border-radius: 0.75rem;
            font-size: 0.9375rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background-color: var(--primary);
            color: white;
            box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
        }
        
        .btn-primary:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(123, 97, 255, 0.4);
        }
        
        .btn-block {
            display: block;
            width: 100%;
        }
        
        .text-link {
            color: var(--primary-light);
            text-decoration: none;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }
        
        .text-link:hover {
            text-decoration: underline;
            color: var(--primary);
        }
        
        .text-center {
            text-align: center;
        }
        
        .mt-3 {
            margin-top: 1.5rem;
        }

        .mb-1 {
            margin-bottom: 0.5rem;
        }

        .mb-3 {
            margin-bottom: 1.5rem;
        }
        
        /* Command List */
        .command-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.25rem;
            margin-top: 1.5rem;
        }
        
        .command-card {
            background-color: rgba(148, 163, 184, 0.05);
            border-radius: 0.75rem;
            padding: 1.25rem;
            border: 1px solid rgba(148, 163, 184, 0.1);
            transition: all 0.3s ease;
        }
        
        .command-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-color: var(--primary-light);
        }
        
        .command-name {
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--primary-light);
            font-size: 1.0625rem;
        }
        
        .command-description {
            font-size: 0.8125rem;
            color: var(--gray-light);
            margin-bottom: 0.75rem;
            line-height: 1.5;
        }
        
        .command-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }
        
        .command-tag {
            font-size: 0.6875rem;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            background-color: rgba(148, 163, 184, 0.1);
            color: var(--gray-light);
            font-weight: 500;
        }
        
        /* Online Users */
        .user-list {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            margin-top: 1.5rem;
        }
        
        .user-card {
            display: flex;
            align-items: center;
            padding: 1rem;
            background-color: rgba(148, 163, 184, 0.05);
            border-radius: 0.75rem;
            border: 1px solid rgba(148, 163, 184, 0.1);
            transition: all 0.3s ease;
        }
        
        .user-card:hover {
            transform: translateX(5px);
            border-color: var(--primary-light);
        }
        
        .user-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 1.25rem;
            border: 2px solid var(--primary-light);
        }
        
        .user-info {
            flex: 1;
        }
        
        .user-name {
            font-weight: 600;
            font-size: 0.9375rem;
            margin-bottom: 0.25rem;
            color: var(--light);
        }
        
        .user-id {
            font-size: 0.75rem;
            color: var(--gray);
            margin-bottom: 0.25rem;
            word-break: break-all;
        }
        
        .user-uptime {
            font-size: 0.75rem;
            color: var(--success);
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        /* Stats */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .stat-card {
            background-color: rgba(148, 163, 184, 0.05);
            border-radius: 0.75rem;
            padding: 1.25rem;
            border: 1px solid rgba(148, 163, 184, 0.1);
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-light);
            margin-bottom: 0.25rem;
        }
        
        .stat-label {
            font-size: 0.8125rem;
            color: var(--gray-light);
        }
        
        /* Footer */
        .footer {
            background-color: var(--glass);
            backdrop-filter: blur(12px);
            padding: 1.5rem;
            text-align: center;
            border-top: 1px solid rgba(148, 163, 184, 0.1);
            margin-top: auto;
        }
        
        .footer-text {
            color: var(--gray);
            font-size: 0.875rem;
        }
        
        .footer-author {
            color: var(--primary-light);
            font-weight: 600;
            text-decoration: none;
        }
        
        /* Toastr Overrides */
        .toast {
            border-radius: 0.75rem !important;
            padding: 1rem !important;
            font-size: 0.875rem !important;
            backdrop-filter: blur(10px) !important;
            background-color: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(148, 163, 184, 0.1) !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
        }
        
        .toast-success {
            color: var(--success) !important;
        }
        
        .toast-error {
            color: var(--danger) !important;
        }
        
        .toast-info {
            color: var(--primary-light) !important;
        }
        
        .toast-warning {
            color: var(--warning) !important;
        }
        
        .toast-title {
            font-weight: 600 !important;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main {
                padding: 1.5rem;
            }
            
            .sidebar {
                width: 280px;
            }
            
            .command-list {
                grid-template-columns: 1fr;
            }
            
            .stats-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1 class="header-title">Bot Manager</h1>
        <div class="menu-toggle">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </header>
    
    <aside class="sidebar">
        <div class="sidebar-header">
            <h2 class="sidebar-title">Navigation</h2>
            <button class="sidebar-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <nav class="sidebar-menu">
            <a href="#" class="sidebar-item active" onclick="showSection('home')">
                <i class="fas fa-home"></i>
                <span>Home</span>
            </a>
            <a href="#" class="sidebar-item" onclick="showSection('create')">
                <i class="fas fa-plus-circle"></i>
                <span>Create Bot</span>
            </a>
            <a href="#" class="sidebar-item" onclick="showSection('login')">
                <i class="fas fa-sign-in-alt"></i>
                <span>Login</span>
            </a>
            <a href="#" class="sidebar-item" onclick="showSection('commands')">
                <i class="fas fa-code"></i>
                <span>Commands</span>
            </a>
            <a href="#" class="sidebar-item" onclick="showSection('online')">
                <i class="fas fa-users"></i>
                <span>Online Bots</span>
            </a>
        </nav>
    </aside>
    
    <main class="main">
        
        <section id="home-section" class="card">
            <div class="owner-profile">
                <img src="https://github.com/K0J4.png" alt="Rahul DonProfile Picture" class="owner-avatar">
                <h2 class="owner-name">ALi Koja</h2>
                <p class="owner-bio">
                    Hello! I'm ALi Koja, the developer behind Bot Manager. I'm passionate about creating efficient and user-friendly tools to simplify your bot management experience. My goal is to empower users with seamless control over their Facebook bots.
                </p>
            </div>
            
            <h3 class="card-title"><i class="fas fa-info-circle"></i> About Bot Manager</h3>
            <p class="mb-3">Welcome to Bot Manager! This platform is designed to provide a comprehensive and intuitive solution for managing your Facebook bots, ensuring a smooth and powerful experience.</p>
            
            <hr style="border-color: rgba(148, 163, 184, 0.1); margin: 1.5rem 0;">
            
            <h3 class="card-title"><i class="fas fa-paper-plane"></i> Get in Touch</h3>
            <p class="mb-1">If you have any questions, feedback, or need support, feel free to reach out:</p>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 0.5rem;"><i class="fas fa-envelope" style="margin-right: 0.5rem; color: var(--primary-light);"></i> Email: <a href="/cdn-cgi/l/email-protection#d5bcbbb3ba95bebabfb4adb1fbadacaf" class="text-link"><span class="__cf_email__" data-cfemail="90f9fef6ffd0fbfffaf1e8f4bee8e9ea">[email&#160;protected]</span></a></li>
                <li><i class="fab fa-facebook" style="margin-right: 0.5rem; color: var(--primary-light);"></i> Facebook: <a href="https://www.facebook.com/mr.ali.koja.jutt" target="_blank" class="text-link">ALi Koja (Official Profile)</a></li>
            </ul>
        </section>

        <section id="create-section" class="card" style="display: none;">
            <h3 class="card-title"><i class="fas fa-plus-circle"></i> Cre
