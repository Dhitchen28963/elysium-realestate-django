function closeSidebar() {
    const sidebar = document.getElementById('my-account-sidebar');
    if (sidebar) {
        sidebar.style.display = 'none';
    }
}

module.exports = { closeSidebar };