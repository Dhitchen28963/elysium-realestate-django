function calculateMortgage(propertyPrice, deposit, term, interestRate) {
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

// Export the function to be accessible from other modules
module.exports = { calculateMortgage };