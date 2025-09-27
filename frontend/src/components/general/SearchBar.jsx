import Button from "./Button";

const SearchBar = () => {
  return (
    <div className="max-w-64 flex flex-row gap-4">
      <input
        type="text"
        name="search"
        id="search"
        className="shadow-sm p-1 w-full rounded-md"
      />
      <Button>Load</Button>
    </div>
  );
};

export default SearchBar;
