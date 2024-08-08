module.exports = {
  roots: ['<rootDir>/static'],
  moduleDirectories: ['node_modules', '<rootDir>/static/js/functions'],
  moduleFileExtensions: ['js', 'json', 'jsx', 'node'],
  testEnvironment: 'jest-environment-jsdom',
  testMatch: ['**/__tests__/**/*.test.js'],
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
  },
};
