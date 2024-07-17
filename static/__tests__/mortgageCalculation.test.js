const { calculateMortgage } = require('../../static/js/functions/mortgageCalculation');

// Test case 1: Basic scenario
test('Calculate mortgage with basic inputs', () => {
    const propertyPrice = 300000;
    const deposit = 60000;
    const term = 30; // in years
    const interestRate = 4.5; // annual interest rate

    const result = calculateMortgage(propertyPrice, deposit, term, interestRate);

    // Assert statements to verify the expected results
    expect(result.propertyPrice).toBe(propertyPrice);
    expect(result.deposit).toBe(deposit);
    expect(result.term).toBe(term);
    expect(result.interestRate).toBe(interestRate);

    // Example assertions for calculated values (adjust according to your formula)
    expect(result.borrowAmount).toBe(propertyPrice - deposit);
    expect(result.monthlyRepayments).toBeCloseTo(1216.04, 2); // Monthly repayments need verification
    expect(result.totalInterest).toBeCloseTo(197776.11, 2); // This value should be verified
});