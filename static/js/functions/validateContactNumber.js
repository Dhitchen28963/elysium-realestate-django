function validateContactNumber(contact) {
    const regex = /^(?:0(?:7\d{9}|(?:1|2|3)\d{8,9}))$/;
    return regex.test(contact);
  }
  
  module.exports = validateContactNumber;
  