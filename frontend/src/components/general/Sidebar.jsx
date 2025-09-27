import SearchBar from "./SearchBar";
const SideBar = ({ showSidebar }) => {
  return showSidebar ? (
    <div className="absolute top-full bg-primary w-full left-0 p-4">
      <SearchBar />
    </div>
  ) : null;
};

export default SideBar;
