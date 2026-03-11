// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 150);
        }, 5000);
    });
    
    // Video upload preview
    const videoInput = document.querySelector('input[type="file"][name="video_file"]');
    if (videoInput) {
        videoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const fileSize = (file.size / 1024 / 1024).toFixed(2);
                if (fileSize > 100) {
                    alert('File size must be less than 100MB');
                    this.value = '';
                }
            }
        });
    }
});
