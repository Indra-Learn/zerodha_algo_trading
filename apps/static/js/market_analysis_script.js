document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const overlay = document.getElementById('overlay');
    
    // Toggle sidebar
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('show');
        content.classList.toggle('shifted');
        overlay.classList.toggle('show');
        
        // Toggle hamburger icon
        const icon = this.querySelector('i');
        if (icon.classList.contains('fa-bars')) {
            icon.classList.replace('fa-bars', 'fa-times');
        } else {
            icon.classList.replace('fa-times', 'fa-bars');
        }
    });
    
    // Close sidebar when clicking on overlay
    overlay.addEventListener('click', function() {
        sidebar.classList.remove('show');
        content.classList.remove('shifted');
        overlay.classList.remove('show');
        const icon = sidebarToggle.querySelector('i');
        if (icon.classList.contains('fa-times')) {
            icon.classList.replace('fa-times', 'fa-bars');
        }
    });
    
    // Toggle sidebar submenus
    const sidebarDropdownToggles = document.querySelectorAll('.sidebar-dropdown-toggle');
    sidebarDropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('data-target');
            const submenu = document.getElementById(target);
            submenu.classList.toggle('show');
            
            // Rotate chevron icon
            const chevron = this.querySelector('.fa-chevron-down');
            chevron.classList.toggle('fa-rotate-180');
        });
    });
    
    // Close sidebar when clicking on a link (optional)
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 768 && !this.classList.contains('sidebar-dropdown-toggle')) {
                sidebar.classList.remove('show');
                content.classList.remove('shifted');
                overlay.classList.remove('show');
                const icon = sidebarToggle.querySelector('i');
                if (icon.classList.contains('fa-times')) {
                    icon.classList.replace('fa-times', 'fa-bars');
                }
            }
        });
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            overlay.classList.remove('show');
        } else if (sidebar.classList.contains('show')) {
            overlay.classList.add('show');
        }
    });
});