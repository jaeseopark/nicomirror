import { ReactNode } from "react";
import styled from "styled-components";

import TopNav from "./TopNav";

import "./App.css";

const PaddedDiv = styled.div`
  // TopNav has a height of 2em. Apply additional top padding of 2em to make things look balanced.
  padding: 2em;
  padding-top: 4em;
`;

const App = ({ children }: { children?: ReactNode }) => {
  return (
    <div className="App">
      <TopNav />
      <PaddedDiv>{children}</PaddedDiv>
    </div>
  );
};

export default App;
