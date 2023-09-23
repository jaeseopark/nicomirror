import react from "react";
import "./TopNav.scss";
import Search from "./Search";

const TopNav = () => {
  // TODO: replace text with icons
  return (
    <div className="nav">
      <label>Home</label>
      <label>Downloads</label>
      <Search />
    </div>
  );
};

export default TopNav;
