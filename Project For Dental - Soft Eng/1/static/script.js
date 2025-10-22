// Centralized JavaScript functions for Dental Clinic Inventory System

// Auto-hide flash messages after specified time
function autoHideAlerts(duration = 1000) {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, duration);
    });
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--error-color)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--border-color)';
        }
    });
    
    return isValid;
}

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Search functionality
function setupSearch(searchInputId, clearBtnId, rowSelector, searchAttributes) {
    const searchInput = document.getElementById(searchInputId);
    const clearBtn = document.getElementById(clearBtnId);
    const rows = document.querySelectorAll(rowSelector);

    if (!searchInput || !clearBtn || !rows.length) return;

    searchInput.addEventListener('input', function() {
        const q = this.value.toLowerCase();
        let any = false;
        rows.forEach(function(row) {
            let matches = false;
            searchAttributes.forEach(function(attr) {
                const value = row.getAttribute(attr) || '';
                if (value.toLowerCase().includes(q)) {
                    matches = true;
                }
            });
            
            if (matches) {
                row.style.display = '';
                any = true;
            } else {
                row.style.display = 'none';
            }
        });
        clearBtn.style.display = q.length ? 'block' : 'none';
    });

    clearBtn.addEventListener('click', function() {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
    });
}

// Chart initialization helper
function initializeChart(canvasId, chartType, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    
    const ctx = canvas.getContext('2d');
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false
    };
    
    const finalOptions = Object.assign({}, defaultOptions, options);
    
    return new Chart(ctx, {
        type: chartType,
        data: data,
        options: finalOptions
    });
}

// Export data to CSV
function exportToCSV(data, filename) {
    const blob = new Blob([data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Print functionality
function printPage() {
    window.print();
}

// Initialize common functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts
    autoHideAlerts();
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});
