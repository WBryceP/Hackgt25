import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BranchIcon from "../../assets/branch.png";
import { motion } from "framer-motion";

const BubbleBox = ({
  header,
  content,
  sources,
  confidence,
  hasSources = true,
}) => {
  const [showSources, setShowSources] = useState(false);

  const confidenceValues = ["low", "medium", "high", "very high"];
  return (
    <>
      <div
        className="rounded-lg shadow-sm outline-placeholder/10 outline p-2 cursor-pointer hover:bg-placeholder/10 transition-colors duration-300"
        onClick={() => setShowSources(!showSources)}
      >
        <h1 className="font-bold mb-1">{header}</h1>
        <div className="flex flex-col justify-between">
          <p className={`${confidence !== undefined ? "mb-2" : ""}`}>
            {content}
          </p>
          {confidence !== undefined ? (
            <div
              className={`border-1 text-center rounded-full w-fit px-3 p-1 flex justify-center items-center h-fit ${
                [
                  "border-lowBorder text-lowText bg-lowBg",
                  "border-mediumBorder text-mediumText bg-mediumBg",
                  "border-highBorder text-highText bg-highBg",
                  "border-highBorder text-highText bg-highBg",
                ][confidence]
              }`}
            >
              Confidence: {confidenceValues[confidence]}
            </div>
          ) : null}
        </div>
      </div>
      {hasSources && showSources ? (
        <ul className="gap-2 flex flex-col">
          {sources.map((source, index) => (
            <div className="flex flex-row relative">
              <div className="">|__</div>
              {index < sources.length - 1 ? (
                <div className="">
                  <div className="absolute top-0 left-0 -translate-x-[0px] translate-y-3">
                    |
                  </div>{" "}
                  <div className="absolute top-0 left-0 -translate-x-[0px] translate-y-6">
                    |
                  </div>
                </div>
              ) : null}

              <motion.a
                className="mx-1 p-1 rounded-sm outline outline-placeholder/50 text-start cursor-pointer"
                whileHover={{ scale: 1.03, translateX: 5 }}
                href={source.url}
                target="_blank"
              >
                {source?.url}
              </motion.a>
            </div>
          ))}
        </ul>
      ) : null}
    </>
  );
};

export default BubbleBox;
