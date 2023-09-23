import "./TopNav.scss";
import Search from "./Search";
import { useNav } from "./hooks/useNav";

const TopNav = () => {
  const { navRoot, navDownloads } = useNav();
  return (
    <div className="nav">
      <label onClick={navRoot}>Home</label>
      <Search />
      <label onClick={navDownloads}>Downloads</label>
    </div>
  );
};

export default TopNav;
