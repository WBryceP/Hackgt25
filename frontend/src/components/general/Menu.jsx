import MenuIcon from "../../assets/menu.svg?react";

const Menu = ({ showSidebar, setShowSidebar }) => {
  return (
    <div
      className="hover:bg-primaryInvert/20 p-2 h-10 rounded-sm cursor-pointer"
      onClick={() => setShowSidebar(!showSidebar)}
    >
      <MenuIcon className="w-fit aspect-square h-full md:hidden" />
    </div>
  );
};

export default Menu;
