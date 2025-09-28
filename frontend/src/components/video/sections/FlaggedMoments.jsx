import { useState } from "react";
import { useRegisterState, useStateBasedMentionProvider } from "cedar-os";
import BubbleBox from "../../general/BubbleBox";

const FlaggedMoments = ({ flaggedMoments, setFlaggedMoments }) => {
  return (
    <div>
      <ul className="mb-2 text-sm flex flex-col gap-2 overflow-scroll">
        {flaggedMoments?.map((moment, index) => {
          return (
            <li key={moment.description + index} className="">
              <BubbleBox header={"Moment"} content={moment.description} />
              <div className="">
                {moment.startSec}s - {moment.endSec}s
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default FlaggedMoments;
