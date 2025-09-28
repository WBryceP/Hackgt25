import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BranchIcon from "../../assets/branch.png";

const BubbleBox = ({ header, content, sources, confidence }) => {
  const [showSources, setShowSources] = useState(false);

  const confidenceValues = ["low", "medium", "high"];
  return (
    <>
      {" "}
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
                ][confidence]
              }`}
            >
              Confidence: {confidenceValues[confidence]}
            </div>
          ) : null}
        </div>
      </div>
      {showSources ? (
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

              <button className="p-1 rounded-sm outline outline-placeholder/50 text-start">
                {source.sourceName}
              </button>
            </div>
          ))}
        </ul>
      ) : null}
    </>
  );
};

export default BubbleBox;
