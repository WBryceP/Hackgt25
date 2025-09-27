import { Search } from "lucide-react";
import { SendHorizonal } from "lucide-react";
import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const re =
  /(^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|v\/|shorts\/)|youtu\.be\/)([A-Za-z0-9_-]{11})(?=[^A-Za-z0-9_-]|$))/i;

const SearchBar = () => {
  const [value, setValue] = useState("");
  const [error, setError] = useState("");
  const nav = useNavigate();

  const handleSubmit = () => {
    setError("");
    if (value.length === 0) {
      setError("URL must not be empty");

      return;
    }
    const id = value.match(re)?.[2];
    if (!id) {
      setError(
        "URL must be a valid youtube link e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ"
      );

      return;
    }
    setValue("");

    nav("/v/" + id);
    console.log(value);
  };

  const handleChange = (e) => {
    setValue(e.target.value);
  };

  return (
    <div className="relative flex flex-row gap-4 w-full">
      <Search
        className={`w-5 h-5 bg-primary top-1/2 -translate-y-1/2 left-1 text-placeholder ${
          value.length > 0 ? "hidden" : "absolute"
        }`}
      />

      <input
        type="text"
        name="search"
        id="search"
        className="shadow-sm p-2 w-full rounded-md bg-primary"
        placeholder="       https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        onChange={handleChange}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSubmit();
        }}
        value={value}
      />
      <AnimatePresence>
        {value.length > 0 ? (
          <motion.div
            className="absolute right-0  top-1/2 -translate-y-1/2 cursor-pointer  p-2 rounded-md hover:bg-primaryInvert/20"
            initial={{ translateX: -4, opacity: 0 }}
            animate={{ translateX: 0, opacity: 1 }}
            exit={{ translateX: -2, opacity: 0 }}
            onClick={handleSubmit}
          >
            <SendHorizonal className={`w-5 h-5text-primaryInvert`} />
          </motion.div>
        ) : (
          ""
        )}
      </AnimatePresence>
      {error.length > 0 ? (
        <div
          className="outline-lowBorder outline-2 bg-lowBg text-lowText absolute top-[110%] p-1 rounded-md z-10 transate-y-5 cursor-pointer w-2/3 right-0"
          onClick={() => setError("")}
        >
          {error}
        </div>
      ) : null}
    </div>
  );
};

export default SearchBar;
