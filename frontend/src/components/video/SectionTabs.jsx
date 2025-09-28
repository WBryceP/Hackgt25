import { useState, useEffect } from "react";
import ClaimAnswer from "./sections/ClaimAnswer";
import DeepSearch from "./sections/DeepSearch";
import Sources from "./sections/Sources";
import FlaggedMoments from "./sections/FlaggedMoments";
import { useRegisterState, useStateBasedMentionProvider } from "cedar-os";

const SectionTabs = () => {
  const [selectedTab, setSelectedTab] = useState(1);
  const [flaggedMoments, setFlaggedMoments] = useState([
    {
      momentName: "USA has the best economy",
      momentContext: "USA es numero uno",
    },
  ]);

  const [claimsAnswers, setClaimsAnswers] = useState([
    {
      claim:
        "This video claims that the Great Barrier Reef has lost over 90% of its coral in the last 5 years.",
      confidence: 0,
      sources: [
        {
          sourceName: "CBO 2024 deficit report",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
        {
          sourceName: "FactCheck.org: Candidate X claim",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
      ],
    },
    {
      claim:
        "This video claims that the Great Barrier Reef has lost over 90% of its coral in the last 5 years.",
      confidence: 0,
      sources: [
        {
          sourceName: "CBO 2024 deficit report",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
        {
          sourceName: "FactCheck.org: Candidate X claim",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
      ],
    },
    {
      claim:
        "This video claims that the Great Barrier Reef has lost over 90% of its coral in the last 5 years.",
      confidence: 0,
      sources: [
        {
          sourceName: "CBO 2024 deficit report",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
        {
          sourceName: "FactCheck.org: Candidate X claim",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
      ],
    },
    {
      claim:
        "This video claims that the Great Barrier Reef has lost over 90% of its coral in the last 5 years.",
      confidence: 0,
      sources: [
        {
          sourceName: "CBO 2024 deficit report",
          sourceURL: "https://gemini.google/students/?hl=en",
        },
      ],
    },
  ]);

  const tabs = [
    { name: "Search", shortened: "Search" },
    { name: "Claim & Answer", shortened: "Claim" },
    { name: "Flagged Moments", shortened: "Moments" },
    // { name: "Sources", shortened: "Sources" },
  ];

  const content = [
    <DeepSearch />,
    <ClaimAnswer
      claimsAnswers={claimsAnswers}
      setClaimAnswers={setClaimsAnswers}
    />,
    <FlaggedMoments
      flaggedMoments={flaggedMoments}
      setFlaggedMoments={setFlaggedMoments}
    />,
    // <Sources sources={sources} setSources={sources} />,
  ];

  // Claims
  useRegisterState({
    key: "claimsAnswers",
    description: "claims made by politicians (that may be true or false)",
    value: claimsAnswers,
  });
  useStateBasedMentionProvider({
    stateKey: "claimsAnswers",
    trigger: "@",
    labelField: "claim",
    order: 10,
    description: "Claims",
    icon: "🔎",
    color: "#b6dc76",
  });

  // Flagged Moments
  useRegisterState({
    key: "flaggedMoments",
    description:
      "important moments where a politican has made a claim (that may either be true or false)",
    value: flaggedMoments,
  });
  useStateBasedMentionProvider({
    stateKey: "flaggedMoments",
    trigger: "@",
    labelField: "momentName",
    order: 10,
    description: "Moments",
    icon: "🔎",
    color: "#eec643",
  });

  // Sources
  // useRegisterState({
  //   key: "sources",
  //   description:
  //     "a list of sources that provide context to claims made by politicians (and whether or not their statements are true)",
  //   value: sources,
  //   setValue: setSources,
  // });
  // useStateBasedMentionProvider({
  //   stateKey: "sources",
  //   trigger: "@",
  //   labelField: "sourceName",
  //   order: 10,
  //   description: "Sources",
  //   icon: "🔎",
  //   color: "#3b82f6",
  // });

  const [windowWidth, setWindowWidth] = useState(0);
  const resizeFunc = () => {
    setWindowWidth(window.innerWidth);
  };

  useEffect(() => {
    setWindowWidth(window.innerWidth);
    window.addEventListener("resize", resizeFunc);

    return () => window.removeEventListener("resize", resizeFunc);
  }, []);

  useEffect(() => {
    setSelectedTab(windowWidth > 768 ? 1 : 0);
  }, [windowWidth]);

  const TabComponents = tabs.map((tab, index) => {
    return (
      <li
        className={`relative flex flex-1  justify-center items-center hover:bg-primaryInvert/20 py-2 cursor-pointer rounded-sm ${
          selectedTab === index ? "bg-body font-semibold" : null
        }`}
        key={index}
        onClick={() => setSelectedTab(index)}
      >
        <h2 className="text-center ">{tab.name}</h2>
        {selectedTab === index ? (
          <hr className="w-full absolute bottom-0 border-1" />
        ) : null}
      </li>
    );
  });

  return (
    <div className="bg-primary shadow-md rounded-md md:w-[50%]">
      {/* Formats */}
      <ul className="md:hidden flex flex-row w-full justify-between">
        {TabComponents}
      </ul>
      <ul className="hidden md:flex flex-row w-full justify-between">
        {TabComponents.slice(1, TabComponents.length)}
      </ul>

      <div className="hidden md:flex p-2 relative   overflow-scroll ">
        {content[selectedTab]}
      </div>
      <div className="flex md:hidden p-2 relative  overflow-scroll">
        {content[selectedTab]}
      </div>
    </div>
  );
};

export default SectionTabs;
