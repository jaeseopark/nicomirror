import { Link as ChakraLink } from "@chakra-ui/react";
import { Link as ReactRouterLink } from "react-router-dom";

import Search from "./Search";

import "./TopNav.scss";

const TopNav = () => {
  return (
    <div className="nav">
      <ChakraLink as={ReactRouterLink} to="/">
        Home
      </ChakraLink>
      <Search />
      <ChakraLink as={ReactRouterLink} to="/downloads">
        Downloads
      </ChakraLink>
    </div>
  );
};

export default TopNav;
