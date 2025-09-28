import SearchBar from "../components/general/SearchBar";
import DebateVideo from "../assets/debate.mp4";
import { useRef } from "react";
import { delay, motion } from "framer-motion";

const Home = () => {
  const videoRef = useRef(null);

  return (
    <div className="flex flex-col">
      <div className="sm:p-4 md:p-8 lg:p-12 flex flex-col md:flex-row gap-8 items-center lg:items-end justify-around">
        <div className="p-4 rounded-md w-fit">
          <div className=" mt-18 flex flex-col justify-center">
            <div className="text-4xl md:text-5xl xl:text-6xl font-bold">
              <div className="flex flex-row gap-2">
                <motion.h1
                  className="text-redAccent"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1, color: "#ed3500" }}
                  transition={{
                    ease: "easeInOut",
                    duration: 0.3,
                  }}
                >
                  Truth
                </motion.h1>
                <motion.h1
                  className="text-blueAccent"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1, color: "#093fb4" }}
                  transition={{
                    delay: 0.4,
                    ease: "easeInOut",
                    duration: 0.5,
                  }}
                >
                  Matters.
                </motion.h1>
              </div>

              <motion.h1
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1, ease: "easeInOut", duration: 0.4 }}
              >
                We check it.
              </motion.h1>
            </div>

            <p className=" mt-8 text-base lg:w-2/3 ">
              Check political claims, uncover the truth, and cut through the
              spin with fact-checking you can trust — all powered by our
              AI-native video player.
            </p>
          </div>
          <div className="max-w-[25rem] mt-8 w-full">
            <SearchBar />
          </div>
        </div>
        <div className="overflow-hidden w-full max-w-156 aspect-video">
          <video autoPlay muted loop ref={videoRef}>
            <source src={DebateVideo} type="video/mp4" />
          </video>
        </div>
      </div>
    </div>
  );
};

export default Home;
