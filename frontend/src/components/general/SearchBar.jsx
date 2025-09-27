import Button from "./Button";
import SearchIcon from "../../assets/search.svg?react";
import { useState } from "react";

const SearchBar = () => {
  const [value, setValue] = useState("");

  const handleChange = (e) => {
    setValue(e.target.value);
  };
  return (
    <div className="relative flex flex-row gap-4 w-full">
      <SearchIcon
        className={`w-5 h-5 absolute bg-primary top-1/2 -translate-y-1/2 left-1 text-placeholder ${
          value.length > 0 ? "hidden" : "absolute"
        }`}
      />
      <input
        type="text"
        name="search"
        id="search"
        className="shadow-sm p-2 w-full rounded-md bg-primary"
        placeholder="       Search"
        onChange={handleChange}
        value={value}
      />
    </div>
  );
};

export default SearchBar;
