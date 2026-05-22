document.addEventListener('DOMContentLoaded', () => {
    // Mobile Navigation Toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            // Change icon
            const icon = mobileBtn.querySelector('i');
            if (icon) {
                if (navLinks.classList.contains('active')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }

    // Typing Effect for Hero Section
    const typedElement = document.getElementById('typed');
    const typedStringsContainer = document.getElementById('typed-strings');
    
    if (typedElement && typedStringsContainer) {
        const strings = Array.from(typedStringsContainer.querySelectorAll('span')).map(span => span.textContent);
        let stringIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typeSpeed = 100;
        
        // Hide the original strings container
        typedStringsContainer.style.display = 'none';
        
        function type() {
            const currentString = strings[stringIndex];
            
            if (isDeleting) {
                typedElement.textContent = currentString.substring(0, charIndex - 1);
                charIndex--;
                typeSpeed = 50;
            } else {
                typedElement.textContent = currentString.substring(0, charIndex + 1);
                charIndex++;
                typeSpeed = 100;
            }
            
            if (!isDeleting && charIndex === currentString.length) {
                isDeleting = true;
                typeSpeed = 2000; // Pause at end
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                stringIndex = (stringIndex + 1) % strings.length;
                typeSpeed = 500; // Pause before typing next
            }
            
            setTimeout(type, typeSpeed);
        }
        
        // Start typing after a short delay
        setTimeout(type, 1000);
    }

    // Scroll Reveal Animation
    const revealElements = document.querySelectorAll('.reveal');
    
    function checkReveal() {
        const windowHeight = window.innerHeight;
        const revealPoint = 50;
        
        revealElements.forEach(el => {
            const revealTop = el.getBoundingClientRect().top;
            if (revealTop < windowHeight - revealPoint) {
                el.classList.add('active');
            }
        });
    }
    
    // Initial check
    checkReveal();
    
    // Check on scroll
    window.addEventListener('scroll', checkReveal);

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        // Check local storage for theme
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'light') {
            document.body.classList.add('light-theme');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
        
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            let theme = 'dark';
            if (document.body.classList.contains('light-theme')) {
                theme = 'light';
                themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            }
            localStorage.setItem('theme', theme);
        });
    }

    // Magnetic Buttons
    const magnets = document.querySelectorAll('.magnetic');
    magnets.forEach(magnet => {
        magnet.addEventListener('mousemove', (e) => {
            const position = magnet.getBoundingClientRect();
            // Get mouse position relative to the center of the element
            const x = e.clientX - position.left - position.width / 2;
            const y = e.clientY - position.top - position.height / 2;
            
            magnet.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });
        
        magnet.addEventListener('mouseleave', () => {
            magnet.style.transform = 'translate(0px, 0px)';
        });
    });

    // Terminal Simulator
    const terminalInput = document.getElementById('terminal-input');
    const terminalBody = document.getElementById('terminal-body');
    if (terminalInput && terminalBody) {
        terminalInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const command = this.value.trim().toLowerCase();
                
                // Echo command
                const outputLine = document.createElement('div');
                outputLine.className = 'terminal-line';
                outputLine.innerHTML = `<span class="terminal-prompt">~</span> ${this.value}`;
                terminalBody.insertBefore(outputLine, this.parentNode);
                
                // Response
                const responseLine = document.createElement('div');
                responseLine.className = 'terminal-line';
                
                if (command === 'help') {
                    responseLine.innerHTML = "Available commands: skills, experience, whoami, clear";
                } else if (command === 'skills') {
                    responseLine.innerHTML = "Backend: Java, Python, Spring Boot, FastAPI<br>GenAI: LangChain, Gemini, Claude";
                } else if (command === 'experience') {
                    responseLine.innerHTML = "4+ Years as Systems Engineer at TCS.<br>- Optimized POS systems by 20%<br>- Built Agentic AI solutions.";
                } else if (command === 'whoami') {
                    responseLine.innerHTML = "Soumyajit Das - Backend Developer & GenAI Engineer";
                } else if (command === 'clear') {
                    const lines = terminalBody.querySelectorAll('.terminal-line:not(:last-child)');
                    lines.forEach(line => line.remove());
                    this.value = '';
                    return;
                } else if (command !== '') {
                    responseLine.innerHTML = `Command not found: ${command}. Type 'help' for available commands.`;
                }
                
                if (command !== '') {
                    terminalBody.insertBefore(responseLine, this.parentNode);
                }
                
                this.value = '';
                terminalBody.scrollTop = terminalBody.scrollHeight;
            }
        });
    }
});
