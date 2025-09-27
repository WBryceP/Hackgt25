import { useEffect, useState } from "react";
import SearchBar from "./SearchBar";
const SideBar = ({ showSidebar, setShowSidebar }) => {
  const [windowWidth, setWindowWidth] = useState(0);
  const resizeFunc = () => {
    setWindowWidth(window.innerWidth);
    console.log(window.innerWidth);
  };

  useEffect(() => {
    setWindowWidth(window.innerWidth);
    window.addEventListener("resize", resizeFunc);

    return () => window.removeEventListener("resize", resizeFunc);
  }, []);

  useEffect(() => {
    setShowSidebar(false);
  }, [windowWidth]);

  return showSidebar ? (
    <div className="absolute top-full bg-primary w-full left-0 p-4">
      <SearchBar />
    </div>
  ) : null;
};

export default SideBar;
