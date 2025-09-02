document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const logoutBtn = document.querySelector('.btn-logout');
    const loginBtn = document.querySelector('.btn-login');
    const signupBtn = document.querySelector('.btn-signup');

    // profile drop-down
    const profileImg = document.getElementById('profileImg');
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    // Get modal elements
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    // const loginBtn = document.getElementById('loginBtn');
    // const signupBtn = document.getElementById('signupBtn');
    // const logoutBtn = document.getElementById('logoutBtn');
    // const profileImg = document.getElementById('profileImg');
    const closeLogin = document.getElementById('closeLogin');
    const closeSignup = document.getElementById('closeSignup');
    // const submitLogin = document.getElementById('submitLogin');
    // const submitSignup = document.getElementById('submitSignup');
    const closeButtons = document.querySelectorAll('.close-btn');
    
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

    
    // Show login modal
    loginBtn.addEventListener('click', function() {
        loginModal.style.display = 'flex';
    });
    
    // Show signup modal
    signupBtn.addEventListener('click', function() {
        signupModal.style.display = 'flex';
    });
    
    // Close modals
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            loginModal.style.display = 'none';
            signupModal.style.display = 'none';
        });
    });
    
    closeLogin.addEventListener('click', function() {
        loginModal.style.display = 'none';
    });
    
    closeSignup.addEventListener('click', function() {
        signupModal.style.display = 'none';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (event.target === signupModal) {
            signupModal.style.display = 'none';
        }
    });
    
    // // Form submission
    // submitLogin.addEventListener('click', function() {
    //     const email = document.getElementById('loginEmail').value;
    //     const password = document.getElementById('loginPassword').value;
        
    //     if (email && password) {
    //         // Simulate login success
    //         alert('Login successful! In a real app, this would connect to your backend.');
    //         loginModal.style.display = 'none';
            
    //         // Update UI for logged in state
    //         loginBtn.style.display = 'none';
    //         signupBtn.style.display = 'none';
    //         logoutBtn.style.display = 'block';
    //         profileImg.style.display = 'block';
    //     } else {
    //         alert('Please fill in all fields');
    //     }
    // });
    
    // submitSignup.addEventListener('click', function() {
    //     const name = document.getElementById('signupName').value;
    //     const email = document.getElementById('signupEmail').value;
    //     const password = document.getElementById('signupPassword').value;
    //     const confirmPassword = document.getElementById('signupConfirmPassword').value;
        
    //     if (password !== confirmPassword) {
    //         alert('Passwords do not match');
    //         return;
    //     }
        
    //     if (name && email && password) {
    //         // Simulate signup success
    //         alert('Account created successfully! In a real app, this would connect to your backend.');
    //         signupModal.style.display = 'none';
            
    //         // Update UI for logged in state
    //         loginBtn.style.display = 'none';
    //         signupBtn.style.display = 'none';
    //         logoutBtn.style.display = 'block';
    //         profileImg.style.display = 'block';
    //     } else {
    //         alert('Please fill in all fields');
    //     }
    // });
    
    // // Logout functionality
    // logoutBtn.addEventListener('click', function() {
    //     // Simulate logout
    //     alert('Logged out successfully');
        
    //     // Update UI for logged out state
    //     loginBtn.style.display = 'block';
    //     signupBtn.style.display = 'block';
    //     logoutBtn.style.display = 'none';
    //     profileImg.style.display = 'none';
    // });
    
    // // Social login buttons
    // document.querySelectorAll('.social-btn').forEach(button => {
    //     button.addEventListener('click', function() {
    //         const platform = this.querySelector('i').classList[1];
    //         alert(`In a real app, this would redirect to ${platform} authentication`);
    //     });
    // });
});