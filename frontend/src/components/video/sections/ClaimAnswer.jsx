import BubbleBox from "../../general/BubbleBox";
import { useState } from "react";
import { useRegisterState } from "cedar-os";

const ClaimAnswer = ({ claimsAnswers, setClaimAnswers }) => {
  return (
    <div className="flex flex-col">
      <h2 className="text-placeholder">NOW REVIEWING</h2>
      <h1 className="my-3 text-base font-bold">Current claims being checked</h1>
      <ul className="flex flex-col gap-2 overflow-scroll p-2">
        {claimsAnswers?.map((claim, index) => {
          return (
            <BubbleBox
              key={claim + "-" + index}
              header={"Claim"}
              content={claim.claim}
              sources={claim.sources}
              confidence={claim.confidence}
            />
          );
        })}
      </ul>
    </div>
  );
};

export default ClaimAnswer;
