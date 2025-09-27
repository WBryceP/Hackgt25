const BubbleBox = ({ header, content, confidence }) => {
  const confidenceValues = ["low", "medium", "high"];
  return (
    <div className="rounded-md shadow-sm outline-placeholder/10 outline p-2">
      <h1 className="font-bold mb-1">{header}</h1>
      <div className="flex flex-col md:flex-row justify-between">
        <p className={`${confidence !== undefined ? "md:w-1/2 mb-2" : ""}`}>
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
  );
};

export default BubbleBox;
