import { useState } from "react";
import SearchBar from "./SearchBar";
import Menu from "../../assets/menu.svg?react";

const Header = () => {
  const [showSidebar, setShowSidebar] = useState(false);
  return (
    <div className="flex justify-between items-center p-1 py-4 bg-primary shadow-sm">
      <div className="">Fact Check</div>
      <Menu className="w-6 h-6" />
      <div className=""></div>
      <SearchBar />
    </div>
  );
};

export default Header;
