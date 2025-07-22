import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders main title', () => {
  render(<App />);
  const titleElement = screen.getByText(/高考考点分析系统/i);
  expect(titleElement).toBeInTheDocument();
});

test('placeholder test', () => {
  expect(true).toBe(true);
});
