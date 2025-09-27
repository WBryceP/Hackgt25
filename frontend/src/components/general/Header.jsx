import { useState } from "react";
import SearchBar from "./SearchBar";
import SideBar from "./Sidebar";
import Menu from "./Menu";

const Header = () => {
  const [showSidebar, setShowSidebar] = useState(false);
  return (
    <div className="relative flex justify-between items-center p-3 py-2 bg-primary shadow-sm">
      <div className="">Fact Check</div>
      <Menu showSidebar={showSidebar} setShowSidebar={setShowSidebar} />
      <div className="hidden md:flex w-1/2">
        <SearchBar />
      </div>
      <SideBar showSidebar={showSidebar} />
    </div>
  );
};

export default Header;
