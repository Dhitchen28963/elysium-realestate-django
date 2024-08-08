const { requestSlotViewing } = require('../../static/js/functions/requestSlotViewing');

global.fetch = require('jest-fetch-mock');

describe('requestSlotViewing', () => {
    beforeEach(() => {
        fetch.resetMocks();
        document.body.innerHTML = `
            <div id="viewingModal" style="display: none;"></div>
            <input type="hidden" name="csrfmiddlewaretoken" value="dummy_csrf_token">
        `;
    });

    test('request slot viewing success', async () => {
        fetch.mockResponseOnce(JSON.stringify({ status: 'ok' }));

        await requestSlotViewing(1);

        expect(fetch).toHaveBeenCalledWith('/real_estate/book_viewing_slot/1/', expect.any(Object));
        const modal = document.getElementById('viewingModal');
        expect(modal.style.display).toBe('block');
    });

    test('request slot viewing error', async () => {
        fetch.mockReject(new Error('Network response was not ok'));

        try {
            await requestSlotViewing(1);
        } catch (e) {
            expect(e.message).toBe('Network response was not ok');
        }

        const modal = document.getElementById('viewingModal');
        expect(modal.style.display).toBe('none');
    });
});
