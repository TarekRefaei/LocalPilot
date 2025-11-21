module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/__tests__/**/*.test.ts', '**/?(*.)+(spec|test).ts'],
  testPathIgnorePatterns: ['<rootDir>/src/test/'],
  transform: {
    '^.+\\.ts$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.jest.json' }]
  },
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.ts',
    '!**/*.(spec|test).ts',
    '!src/test/**',
    '!src/views/**',
    '!src/services/backend.ts',
    '!src/chat.ts'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'json-summary'],
  coverageThreshold: {
    global: { lines: 60, branches: 50, functions: 60, statements: 60 }
  },
  moduleNameMapper: {
    '^vscode$': '<rootDir>/__mocks__/vscode.ts',
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};
