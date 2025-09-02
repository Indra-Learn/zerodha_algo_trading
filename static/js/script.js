document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const logoutBtn = document.querySelector('.btn-logout');
    const loginBtn = document.querySelector('.btn-login');
    const signupBtn = document.querySelector('.btn-signup');
    const profileImg = document.getElementById('profileImg');
    const dropdownMenu = document.getElementById('dropdownMenu');

    // Toggle dropdown when profile image is clicked
    profileImg.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownMenu.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!profileImg.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove('active');
        }
    });
    
    // Close dropdown when a menu item is clicked
    const menuItems = dropdownMenu.querySelectorAll('a');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            dropdownMenu.classList.remove('active');
        });
    });
    
    // Toggle sidebar
    hamburger.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
    
    // Close sidebar when clicking on overlay
    overlay.addEventListener('click', function() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        hamburger.classList.remove('active');
    });
    
    // Toggle submenus
    const submenuParents = document.querySelectorAll('.has-submenu');
    submenuParents.forEach(parent => {
        parent.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                e.preventDefault();
                const submenu = this.querySelector('.submenu');
                this.classList.toggle('active');
                submenu.classList.toggle('active');
            }
        });
    });
    
    // // Simulate login/logout functionality
    // let loggedIn = false;
    
    // function toggleAuth() {
    //     loggedIn = !loggedIn;
        
    //     if (loggedIn) {
    //         loginBtn.style.display = 'none';
    //         signupBtn.style.display = 'none';
    //         logoutBtn.style.display = 'block';
    //     } else {
    //         loginBtn.style.display = 'block';
    //         signupBtn.style.display = 'block';
    //         logoutBtn.style.display = 'none';
    //     }
    // }
    
    // // Add click events to auth buttons
    // if (loginBtn) {
    //     loginBtn.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         toggleAuth();
    //     });
    // }
    
    // if (signupBtn) {
    //     signupBtn.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         toggleAuth();
    //     });
    // }
    
    // if (logoutBtn) {
    //     logoutBtn.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         toggleAuth();
    //     });
    // }
    
    // Initialize ticker if it exists
    const initTicker = () => {
        const ticker = document.querySelector('.ticker');
        if (!ticker) return;
        
        // Duplicate ticker items for seamless scrolling
        const tickerContent = ticker.innerHTML;
        ticker.innerHTML += tickerContent;
    };
    
    initTicker();
});