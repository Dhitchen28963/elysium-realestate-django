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

    // Example assertions for calculated values (adjust accordingly)
    expect(result.borrowAmount).toBe(propertyPrice - deposit);
    expect(result.monthlyRepayments).toBeCloseTo(1216.04, 2);
    expect(result.totalInterest).toBeCloseTo(197776.11, 2);
    expect(result.totalRepayable).toBeCloseTo(437776.11, 2);
});

// Test case 2: Validation scenario - zero or negative values
test('Calculate mortgage with zero or negative values', () => {
    expect(() => calculateMortgage(0, 0, 30, 4.5)).toThrow('Please ensure all values are greater than zero.');
    expect(() => calculateMortgage(-100000, -20000, 30, 4.5)).toThrow('Please ensure all values are greater than zero.');
});

// Test case 3: Validation scenario - deposit greater than property price
test('Calculate mortgage with deposit greater than property price', () => {
    expect(() => calculateMortgage(100000, 200000, 30, 4.5)).toThrow('Deposit cannot be greater than or equal to the property price.');
});

// Test case 4: Scenario with different valid inputs
test('Calculate mortgage with different valid inputs', () => {
    const propertyPrice = 500000;
    const deposit = 100000;
    const term = 25; // in years
    const interestRate = 3.75; // annual interest rate

    const result = calculateMortgage(propertyPrice, deposit, term, interestRate);

    // Assert statements to verify the expected results
    expect(result.propertyPrice).toBe(propertyPrice);
    expect(result.deposit).toBe(deposit);
    expect(result.term).toBe(term);
    expect(result.interestRate).toBe(interestRate);

    // Example assertions for calculated values (adjust accordingly)
    expect(result.borrowAmount).toBe(propertyPrice - deposit);
    expect(result.monthlyRepayments).toBeCloseTo(2056.52, 2);
    expect(result.totalInterest).toBeCloseTo(216957.44, 2);
    expect(result.totalRepayable).toBeCloseTo(616957.44, 2);
});
