import "./App.css";
import TopNav from "./TopNav";
import { ReactNode } from "react";
import { ChakraProvider } from "@chakra-ui/react";

const App = ({ children }: { children?: ReactNode }) => {
  return (
    <ChakraProvider>
      <div className="App">
        <TopNav />
        <div className="content">{children}</div>
      </div>
    </ChakraProvider>
  );
};

export default App;
