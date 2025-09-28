import { useState } from "react";
import { useRegisterState, useStateBasedMentionProvider } from "cedar-os";

const FlaggedMoments = ({ flaggedMoments, setFlaggedMoments }) => {
  return (
    <div>
      <ul className="mb-2 text-sm flex flex-col gap-2 overflow-scroll">
        {flaggedMoments.map((source, index) => {
          return (
            <li key={source.sourceName + index} className="">
              {source.sourceName}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default FlaggedMoments;
