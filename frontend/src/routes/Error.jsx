import SearchBar from "../components/general/SearchBar";

const Error = ({ error }) => {
  return (
    <div className="">
      <h1 className="text-redAccent text-4xl font-semibold mx-auto text-center mt-8">
        Error: {error ? error : "your YouTube link was invalid"}
      </h1>
      <div className="mx-auto w-2/3 mt-8">
        <SearchBar />
      </div>
      <div className="mx-auto w-fit mt-4 text-placeholder">
        Make sure your URL follows the format above
      </div>
    </div>
  );
};
export default Error;
