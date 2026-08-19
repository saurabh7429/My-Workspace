// write a react testing file for a simple component that displays a greeting message
import React from "react";
import { render, screen } from "@testing-library/react";
import Greeting from "./Greeting"; // Assuming the component is in the same directory

test("renders greeting message", () => {
  render(<Greeting name="John" />);
  const greetingElement = screen.getByText(/Hello, John!/i);
  expect(greetingElement).toBeInTheDocument();
});
