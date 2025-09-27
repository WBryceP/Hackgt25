import BubbleBox from "../../general/BubbleBox";

const ClaimAnswer = () => {
  return (
    <div className="flex flex-col">
      <h2 className="text-placeholder">NOW REVIEWING</h2>
      <h1 className="my-3 text-base font-bold">Current claim being checked</h1>
      <BubbleBox
        header={"Claim"}
        content={
          "This video claims that the Great Barrier Reef has lost over 90% of its coral in the last 5 years."
        }
        confidence={2}
      />
    </div>
  );
};

export default ClaimAnswer;
