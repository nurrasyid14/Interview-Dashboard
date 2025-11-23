/* ============================================
   HIRE-ON PREMIUM UI - JAVASCRIPT
   Interactive Components & Animations
   ============================================ */

   document.addEventListener("DOMContentLoaded", () => {
    initLoginPage()
    initDashboard()
  })
  
  // ============================================
  // LOGIN PAGE FUNCTIONALITY
  // ============================================
  
  function initLoginPage() {
    const loginForm = document.getElementById("loginForm")
    const emailInput = document.getElementById("email")
    const passwordInput = document.getElementById("password")
  
    if (!loginForm) return
  
    // Add input event listeners
    if (emailInput) {
      emailInput.addEventListener("focus", () => {
        emailInput.classList.remove("error")
      })
    }
  
    if (passwordInput) {
      passwordInput.addEventListener("focus", () => {
        passwordInput.classList.remove("error")
      })
    }
  
    // Form submission with validation
    loginForm.addEventListener("submit", handleLoginSubmit)
  
    // Add enter key support
    if (passwordInput) {
      passwordInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          handleLoginSubmit(e)
        }
      })
    }
  }
  
  function handleLoginSubmit(e) {
    e.preventDefault()
  
    const email = document.getElementById("email")
    const password = document.getElementById("password")
    const loginBtn = document.querySelector(".login-btn")
  
    let isValid = true
  
    // Email validation
    if (!email.value || !isValidEmail(email.value)) {
      addErrorShake(email, "Please enter a valid email")
      isValid = false
    }
  
    // Password validation
    if (!password.value || password.value.length < 6) {
      addErrorShake(password, "Password must be at least 6 characters")
      isValid = false
    }
  
    if (isValid) {
      // Button loading state
      const originalText = loginBtn.textContent
      loginBtn.textContent = "🔄 Signing In..."
      loginBtn.disabled = true
  
      // Simulate API call
      setTimeout(() => {
        // Success animation
        loginBtn.textContent = "✓ Success!"
  
        setTimeout(() => {
          // Redirect or navigate
          console.log("Login successful:", { email: email.value })
          // window.location.href = '/dashboard.html';
        }, 1000)
      }, 1500)
    }
  }
  
  function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
  }
  
  function addErrorShake(input, message) {
    input.classList.add("error")
  
    // Show error message
    const errorMsg = document.createElement("div")
    errorMsg.style.cssText = `
      font-size: 12px;
      color: #EF4444;
      margin-top: 4px;
      animation: fadeIn 0.3s ease-out;
    `
    errorMsg.textContent = message
  
    const existingError = input.parentElement.querySelector('[role="alert"]')
    if (existingError) existingError.remove()
  
    errorMsg.setAttribute("role", "alert")
    input.parentElement.appendChild(errorMsg)
  }
  
  // ============================================
  // DASHBOARD FUNCTIONALITY
  // ============================================
  
  function initDashboard() {
    initSidebarNavigation()
    initTabsSystem()
    initDarkMode()
    initCardAnimations()
    initProgressBars()
  }
  
  // Sidebar Navigation
  function initSidebarNavigation() {
    const navItems = document.querySelectorAll(".nav-item")
    const menuToggle = document.querySelector(".menu-toggle")
    const sidebar = document.querySelector(".sidebar")
  
    // Toggle sidebar on mobile
    if (menuToggle) {
      menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("active")
      })
    }
  
    navItems.forEach((item) => {
      item.addEventListener("click", (e) => {
        e.preventDefault()
  
        // Remove active from all items
        navItems.forEach((nav) => nav.classList.remove("active"))
  
        // Add active to clicked item
        item.classList.add("active")
  
        // Close sidebar on mobile
        if (window.innerWidth <= 768) {
          sidebar.classList.remove("active")
        }
  
        // Handle tab switching
        const targetTab = item.getAttribute("data-tab")
        if (targetTab) {
          showTab(targetTab)
        }
  
        // Add smooth scroll
        const tabContent = document.querySelector(`[data-content="${targetTab}"]`)
        if (tabContent) {
          tabContent.scrollIntoView({ behavior: "smooth" })
        }
      })
    })
  }
  
  // Tabs System
  function initTabsSystem() {
    const tabButtons = document.querySelectorAll(".tab-item")
    const tabContents = document.querySelectorAll(".tab-content")
  
    tabButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const targetTab = button.getAttribute("data-tab")
  
        // Remove active class from all
        tabButtons.forEach((btn) => btn.classList.remove("active"))
        tabContents.forEach((content) => content.classList.remove("active"))
  
        // Add active to clicked
        button.classList.add("active")
        const activeContent = document.querySelector(`.tab-content[data-tab="${targetTab}"]`)
        if (activeContent) {
          activeContent.classList.add("active")
        }
      })
    })
  
    // Set first tab as active if exists
    if (tabButtons.length > 0) {
      tabButtons[0].classList.add("active")
      const firstTab = tabButtons[0].getAttribute("data-tab")
      const firstContent = document.querySelector(`.tab-content[data-tab="${firstTab}"]`)
      if (firstContent) {
        firstContent.classList.add("active")
      }
    }
  }
  
  function showTab(tabName) {
    const tabButtons = document.querySelectorAll(".tab-item")
    const tabContents = document.querySelectorAll(".tab-content")
  
    tabButtons.forEach((btn) => btn.classList.remove("active"))
    tabContents.forEach((content) => content.classList.remove("active"))
  
    const activeButton = document.querySelector(`.tab-item[data-tab="${tabName}"]`)
    const activeContent = document.querySelector(`.tab-content[data-tab="${tabName}"]`)
  
    if (activeButton) activeButton.classList.add("active")
    if (activeContent) activeContent.classList.add("active")
  }
  
  // Dark Mode Toggle
  function initDarkMode() {
    const toggleBtn = document.querySelector(".toggle-dark")
    const isDarkMode = localStorage.getItem("dark-mode") === "true"
  
    if (isDarkMode) {
      document.documentElement.setAttribute("data-dark-mode", "true")
      updateDarkModeStyles(true)
    }
  
    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        const isDark = document.documentElement.getAttribute("data-dark-mode") === "true"
        const newState = !isDark
  
        if (newState) {
          document.documentElement.setAttribute("data-dark-mode", "true")
        } else {
          document.documentElement.removeAttribute("data-dark-mode")
        }
  
        localStorage.setItem("dark-mode", newState)
        updateDarkModeStyles(newState)
        toggleBtn.textContent = newState ? "☀️" : "🌙"
      })
  
      toggleBtn.textContent = isDarkMode ? "☀️" : "🌙"
    }
  }
  
  function updateDarkModeStyles(isDark) {
    const root = document.documentElement
  
    if (isDark) {
      root.style.setProperty("--bg-primary", "#0E0E0E")
      root.style.setProperty("--bg-secondary", "#1A1A1A")
      root.style.setProperty("--bg-tertiary", "#252525")
      root.style.setProperty("--text-primary", "#F1F5F9")
      root.style.setProperty("--text-secondary", "#CBD5E1")
      root.style.setProperty("--text-tertiary", "#94A3B8")
      root.style.setProperty("--border-light", "#2D3748")
    } else {
      root.style.setProperty("--bg-primary", "#FFFFFF")
      root.style.setProperty("--bg-secondary", "#F8F9FA")
      root.style.setProperty("--bg-tertiary", "#F3F4F6")
      root.style.setProperty("--text-primary", "#0F172A")
      root.style.setProperty("--text-secondary", "#64748B")
      root.style.setProperty("--text-tertiary", "#94A3B8")
      root.style.setProperty("--border-light", "#E2E8F0")
    }
  }
  
  // Card Hover Animations
  function initCardAnimations() {
    const cards = document.querySelectorAll(".card")
  
    cards.forEach((card) => {
      card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-4px)"
        card.style.boxShadow = "0 20px 25px rgba(16, 185, 129, 0.15)"
      })
  
      card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0)"
        card.style.boxShadow = "0 1px 2px rgba(0, 0, 0, 0.05)"
      })
    })
  }
  
  // Progress Bars Animation
  function initProgressBars() {
    const progressFills = document.querySelectorAll(".progress-fill")
  
    progressFills.forEach((fill) => {
      const width = fill.getAttribute("data-width") || "65"
      fill.style.width = width + "%"
    })
  }
  
  // Utility function to add ripple effect to buttons
  function addRippleEffect(button) {
    button.addEventListener("click", function (e) {
      const ripple = document.createElement("span")
      const rect = this.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const x = e.clientX - rect.left - size / 2
      const y = e.clientY - rect.top - size / 2
  
      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        left: ${x}px;
        top: ${y}px;
        pointer-events: none;
        animation: rippleAnimation 0.6s ease-out;
      `
  
      this.appendChild(ripple)
      setTimeout(() => ripple.remove(), 600)
    })
  }
  
  // Export for external use
  window.HireonUI = {
    showTab,
    addRippleEffect,
  }
  