describe('collapsible functionality', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <button class="collapsible">Open Collapsible</button>
            <div class="content" style="display: none;">Content</div>
        `;

        document.querySelector('.collapsible').addEventListener('click', function () {
            const content = document.querySelector('.content');
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
        });
    });

    test('should toggle collapsible content on button click', () => {
        document.querySelector('.collapsible').click();
        const content = document.querySelector('.content');
        expect(content.style.display).toBe('block');
    });

    test('should close collapsible content on close button click', () => {
        document.querySelector('.collapsible').click(); // Open first
        document.querySelector('.collapsible').click(); // Close second
        const content = document.querySelector('.content');
        expect(content.style.display).toBe('none');
    });
});
