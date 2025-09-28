import { useState } from "react";
import SearchBar from "./SearchBar";
import SideBar from "./Sidebar";
import Menu from "./Menu";
import { useNavigate } from "react-router-dom";
import Icon from "../../assets/icon.png";

const Header = () => {
  const [showSidebar, setShowSidebar] = useState(false);
  const nav = useNavigate();

  return (
    <div className="relative flex justify-between items-center p-3 py-2 bg-primary shadow-sm">
      <div
        className="cursor-pointer flex flex-row justify-center items-center text-3xl font-semibold"
        onClick={() => nav("/")}
      >
        <img src={Icon} className="w-14" />
        <div className="flex flex-row gap-1">
          <h1 className="text-blueAccent">News</h1>
          <h1 className="text-redAccent">Cap</h1>
        </div>
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
