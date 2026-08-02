/**
 * main.js
 * ==============================================================================
 * Project: College Student Performance Analytics System
 * Description: Client-side JavaScript interactions, alert handling, and Bootstrap
 *              component initialization.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log("College Student Performance Analytics System loaded successfully.");

    // Auto-dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // Initialize Bootstrap Tooltips if present
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));
});
