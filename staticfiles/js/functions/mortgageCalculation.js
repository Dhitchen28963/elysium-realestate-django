function calculateMortgage(propertyPrice, deposit, term, interestRate) {
    // Validation for input values
    if (propertyPrice <= 0 || deposit <= 0 || term <= 0 || interestRate <= 0) {
        throw new Error('Please ensure all values are greater than zero.');
    }

    if (deposit >= propertyPrice) {
        throw new Error('Deposit cannot be greater than or equal to the property price.');
    }

    const borrowAmount = propertyPrice - deposit; // Amount that can be borrowed
    const monthlyInterestRate = (interestRate / 100) / 12;
    const numberOfPayments = term * 12;
    const principal = borrowAmount;

    const monthlyRepayments = (principal * monthlyInterestRate) / (1 - Math.pow((1 + monthlyInterestRate), -numberOfPayments));
    const totalRepayable = monthlyRepayments * numberOfPayments;
    const totalInterest = totalRepayable - principal;

    return {
        propertyPrice,
        deposit,
        term,
        interestRate,
        borrowAmount,
        monthlyRepayments,
        totalInterest,
        totalRepayable
    };
}

module.exports = { calculateMortgage };
