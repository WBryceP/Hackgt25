import { useState } from "react";
import SearchBar from "./SearchBar";
import SideBar from "./Sidebar";
import Menu from "./Menu";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const [showSidebar, setShowSidebar] = useState(false);
  const nav = useNavigate();

  return (
    <div className="relative flex justify-between items-center p-3 py-2 bg-primary shadow-sm">
      <div className="" onClick={() => nav("/")}>
        Fact Check
      </div>
      <Menu showSidebar={showSidebar} setShowSidebar={setShowSidebar} />
      <div className="hidden md:flex w-1/2">
        <SearchBar />
      </div>
      <SideBar showSidebar={showSidebar} setShowSidebar={setShowSidebar} />
    </div>
  );
};

export default Header;
