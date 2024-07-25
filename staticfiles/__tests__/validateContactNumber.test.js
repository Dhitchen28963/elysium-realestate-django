const validateContactNumber = require('../../static/js/functions/validateContactNumber');

describe('validateContactNumber', () => {
  it('should validate correct UK mobile numbers', () => {
    expect(validateContactNumber('07123456789')).toBe(true);
  });

  it('should validate correct UK landline numbers', () => {
    expect(validateContactNumber('01234567890')).toBe(true);
  });

  it('should invalidate incorrect numbers', () => {
    expect(validateContactNumber('12345')).toBe(false);
    expect(validateContactNumber('abcdefg')).toBe(false);
  });
});