/**
 * Complaint Management System - Interactive Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // ---------------------------------------------------------
    // 1. Auto-dismiss Flash Alerts after 5 seconds
    // ---------------------------------------------------------
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // ---------------------------------------------------------
    // 2. Client-Side Live Table Search Helper
    // ---------------------------------------------------------
    const searchInput = document.getElementById('tableSearchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const filter = searchInput.value.toLowerCase();
            const tableRows = document.querySelectorAll('.filterable-table tbody tr');

            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(filter)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // ---------------------------------------------------------
    // 3. Password Match Validation Helper for Register Form
    // ---------------------------------------------------------
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const pass = document.getElementById('password').value;
            const confirmPass = document.getElementById('confirm_password').value;
            if (pass !== confirmPass) {
                e.preventDefault();
                alert('Passwords do not match. Please verify your passwords.');
            }
        });
    }

    // ---------------------------------------------------------
    // 4. Admin Analytics Charts (Chart.js Integration)
    // ---------------------------------------------------------
    if (document.getElementById('statusChart') && document.getElementById('categoryChart')) {
        loadAdminAnalytics();
    }
});

/**
 * Fetches JSON analytics data from Flask API endpoint and renders Chart.js charts
 */
function loadAdminAnalytics() {
    fetch('/admin/api/analytics')
        .then(response => response.json())
        .then(data => {
            // --- Status Doughnut Chart ---
            const statusCtx = document.getElementById('statusChart').getContext('2d');
            new Chart(statusCtx, {
                type: 'doughnut',
                data: {
                    labels: data.status_labels,
                    datasets: [{
                        data: data.status_data,
                        backgroundColor: [
                            '#f59e0b', // Pending - Amber
                            '#0284c7', // In Progress - Sky Blue
                            '#10b981', // Resolved - Emerald
                            '#ef4444'  # Rejected - Rose Red
                        ],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });

            // --- Category Bar Chart ---
            const categoryCtx = document.getElementById('categoryChart').getContext('2d');
            new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: data.category_labels,
                    datasets: [{
                        label: 'Number of Complaints',
                        data: data.category_data,
                        backgroundColor: '#2563eb',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            // --- Priority Bar Chart (if element exists) ---
            const priorityCanvas = document.getElementById('priorityChart');
            if (priorityCanvas) {
                const priorityCtx = priorityCanvas.getContext('2d');
                new Chart(priorityCtx, {
                    type: 'pie',
                    data: {
                        labels: data.priority_labels,
                        datasets: [{
                            data: data.priority_data,
                            backgroundColor: [
                                '#64748b', // Low - Gray
                                '#2563eb', // Medium - Blue
                                '#dc2626'  // High - Red
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            }
        })
        .catch(error => console.error('Error fetching analytics data:', error));
}
